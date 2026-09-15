import os
import glob
import json
import argparse
from pathlib import Path

import pandas as pd
import numpy as np

# Adjust sys.path to allow imports from project root
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.predict import predict, load_models

try:
    from src.config import WEIGHTS_DIR, ATTRIBUTION_CLASSES, DEVICE
except ImportError:
    WEIGHTS_DIR = "weights"
    ATTRIBUTION_CLASSES = ["Midjourney", "DALL-E 3", "Stable Diffusion", "Real"]
    DEVICE = "cuda"

try:
    from src.utils.metrics import (
        compute_all_metrics, compute_ece, plot_confusion_matrix, plot_roc_curve
    )
except ImportError:
    # Dummy fallbacks for metrics if not implemented
    def compute_all_metrics(*args, **kwargs): return {"auc": 0.0, "f1": 0.0, "accuracy": 0.0, "fpr": 0.0}
    def compute_ece(*args, **kwargs): return 0.0
    def plot_confusion_matrix(*args, **kwargs): pass
    def plot_roc_curve(*args, **kwargs): pass

def get_ground_truth(file_name: str) -> int:
    """Heuristics to determine ground truth from file name or directory."""
    if "real" in file_name.lower():
        return 0
    return 1

def main():
    global DEVICE, WEIGHTS_DIR
    parser = argparse.ArgumentParser(description="Evaluate SignalScope Models")
    parser.add_argument("--test_dir", required=True, type=str, help="Directory containing test images")
    parser.add_argument("--output_dir", required=True, type=str, help="Output directory for reports")
    parser.add_argument("--weights_dir", type=str, default=WEIGHTS_DIR, help="Directory with model weights")
    parser.add_argument("--device", type=str, default=DEVICE, help="Device to use")
    parser.add_argument("--max_samples", type=int, default=None, help="Max test images to evaluate (balanced)")
    parser.add_argument("--use_tta", action="store_true", help="Enable test-time augmentation (4x slower)")
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Override globals if provided
    DEVICE = args.device
    WEIGHTS_DIR = args.weights_dir
    
    image_paths = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp"):
        image_paths.extend(glob.glob(os.path.join(args.test_dir, "**", ext), recursive=True))
        image_paths.extend(glob.glob(os.path.join(args.test_dir, "**", ext.upper()), recursive=True))
        
    if not image_paths:
        print(f"No images found in {args.test_dir}")
        return
        
    print(f"Found {len(image_paths)} total images in {args.test_dir}.")
    
    if args.max_samples is not None and len(image_paths) > args.max_samples:
        real_paths = [p for p in image_paths if "real" in p.lower()]
        fake_paths = [p for p in image_paths if "real" not in p.lower()]
        per_class = args.max_samples // 2
        image_paths = real_paths[:per_class] + fake_paths[:per_class]
        print(f"Subsampled {len(image_paths)} balanced test images ({min(per_class, len(real_paths))} Real, {min(per_class, len(fake_paths))} Fake).")
        
    # Pre-load models
    load_models(DEVICE)
    
    y_true = []
    y_pred_probs = []
    y_pred_labels = []
    y_attr_true = []
    y_attr_pred = []
    
    from tqdm import tqdm
    # Evaluate over images
    for img_path in tqdm(image_paths, desc="Evaluating"):
        label = get_ground_truth(img_path)
        y_true.append(label)
        
        res = predict(img_path, explain=False, use_tta=args.use_tta)
        if "error" in res:
            print(f"Failed prediction on {img_path}: {res['error']}")
            prob = 0.5
            attr = "Unknown"
        else:
            prob = res.get("ai_probability", res.get("confidence", 0.5))
            attr = res.get("attribution", "Unknown")
            
        y_pred_probs.append(prob)
        y_pred_labels.append(1 if prob > 0.5 else 0)
        
        if label == 1:
            y_attr_true.append(0)
            if attr in ATTRIBUTION_CLASSES:
                y_attr_pred.append(ATTRIBUTION_CLASSES.index(attr))
            else:
                y_attr_pred.append(-1)
                
    # Calculate metrics
    y_true_np = np.array(y_true)
    y_pred_probs_np = np.array(y_pred_probs)
    y_pred_labels_np = np.array(y_pred_labels)
    
    metrics = compute_all_metrics(y_true_np, y_pred_probs_np)
    metrics["ece"] = compute_ece(y_true_np, y_pred_probs_np)
    
    print("\n" + "="*40)
    print("       SignalScope Evaluation Metrics       ")
    print("="*40)
    for k, v in metrics.items():
        if isinstance(v, (int, float, np.floating, np.integer)):
            print(f"  {k.upper():<20}: {v:.4f}")
        elif isinstance(v, np.ndarray):
            print(f"  {k.upper():<20}:\n{v}")
            
    # Save plots
    cm_path = os.path.join(args.output_dir, "confusion_matrix.png")
    plot_confusion_matrix(y_true_np, y_pred_labels_np, classes=["Real", "AI"], save_path=cm_path)
    
    roc_path = os.path.join(args.output_dir, "roc_curve.png")
    plot_roc_curve(y_true_np, y_pred_probs_np, save_path=roc_path)
    
    # Save metrics JSON (converting numpy ndarrays and numbers)
    def to_serializable(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.float32, np.float64, np.floating)):
            return float(obj)
        if isinstance(obj, (np.int32, np.int64, np.integer)):
            return int(obj)
        if isinstance(obj, dict):
            return {k: to_serializable(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [to_serializable(v) for v in obj]
        return obj

    metrics_path = os.path.join(args.output_dir, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(to_serializable(metrics), f, indent=4)
        
    print(f"\nEvaluation complete. Reports and plots saved to {args.output_dir}")

if __name__ == "__main__":
    main()
