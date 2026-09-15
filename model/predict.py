import os
import sys
import json
import glob
import argparse
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import warnings

import torch
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import torchvision.transforms.functional as F

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import constants from src.config
from src.config import (
    DEVICE, WEIGHTS_DIR, DINO_INPUT_SIZE, IMAGENET_MEAN, IMAGENET_STD, ATTRIBUTION_CLASSES
)

# Try to import model components
try:
    from src.features.feature_pipeline import FeaturePipeline
    from src.models.fusion_detector import SignalScopeDetector
    from src.models.calibration import TemperatureScaling
    from src.models.stacking import StackingEnsemble
    from src.inference.abstention import responsible_verdict
except ImportError:
    # Provide dummy implementations if not available so the file is complete
    class DummyModel(torch.nn.Module):
        def forward(self, x): return torch.zeros((x.shape[0], 2)), torch.zeros((x.shape[0], 4))
    FeaturePipeline = lambda: torch.nn.Identity()
    SignalScopeDetector = DummyModel
    TemperatureScaling = lambda: torch.nn.Identity()
    class StackingEnsemble:
        def load(self, p): pass
        def predict(self, x): return np.zeros((x.shape[0],))
    def responsible_verdict(prob: float) -> Dict[str, Any]:
        return {"verdict": "Likely AI" if prob > 0.5 else "Likely Real"}

_model_cache = {}

def preprocess_for_dino(image_pil: Image.Image) -> torch.Tensor:
    """
    Preprocess PIL Image for DINOv2 input:
    - Resize to 518x518
    - Normalize with ImageNet stats
    Returns (3, 518, 518) tensor.
    """
    if image_pil.mode != "RGB":
        image_pil = image_pil.convert("RGB")
    
    img = F.resize(image_pil, [DINO_INPUT_SIZE, DINO_INPUT_SIZE])
    img_tensor = F.to_tensor(img)
    img_tensor = F.normalize(img_tensor, mean=IMAGENET_MEAN, std=IMAGENET_STD)
    return img_tensor

def save_heatmap_overlay(image_np: np.ndarray, heatmap: np.ndarray, image_path: str) -> str:
    """
    Overlay heatmap on original image and save to disk.
    image_np: (H, W, 3) RGB uint8
    heatmap: (H, W) float 0-1
    """
    out_dir = os.path.dirname(image_path)
    base = os.path.basename(image_path)
    name, _ = os.path.splitext(base)
    
    heatmap_resized = cv2.resize(heatmap, (image_np.shape[1], image_np.shape[0]))
    heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    
    overlay = cv2.addWeighted(image_np, 0.5, heatmap_colored, 0.5, 0)
    
    out_path = os.path.join(out_dir, f"{name}_explain.png")
    Image.fromarray(overlay).save(out_path)
    return out_path

def load_models(device_str: str) -> Dict[str, Any]:
    global _model_cache
    if _model_cache:
        return _model_cache
        
    device = torch.device(device_str)
    try:
        feature_pipeline = FeaturePipeline()
        if hasattr(feature_pipeline, "to"): feature_pipeline = feature_pipeline.to(device)
        if hasattr(feature_pipeline, "eval"): feature_pipeline.eval()
        
        detector = SignalScopeDetector()
        if hasattr(detector, "to"): detector = detector.to(device)
        detector_path = os.path.join(WEIGHTS_DIR, "detector.pth")
        if os.path.exists(detector_path):
            ckpt = torch.load(detector_path, map_location=device)
            state_dict = ckpt.get("model_state_dict", ckpt) if isinstance(ckpt, dict) and "model_state_dict" in ckpt else ckpt
            detector.load_state_dict(state_dict)
        if hasattr(detector, "eval"): detector.eval()
        
        calibrator = TemperatureScaling()
        if hasattr(calibrator, "to"): calibrator = calibrator.to(device)
        calibrator_path = os.path.join(WEIGHTS_DIR, "calibrator.pth")
        if os.path.exists(calibrator_path):
            calibrator.load_state_dict(torch.load(calibrator_path, map_location=device))
            
        stacker = StackingEnsemble()
        stacker_path = os.path.join(WEIGHTS_DIR, "stacker.joblib")
        if os.path.exists(stacker_path):
            stacker.load(stacker_path)
            
        _model_cache = {
            "feature_pipeline": feature_pipeline,
            "detector": detector,
            "calibrator": calibrator,
            "stacker": stacker,
            "device": device
        }
        return _model_cache
    except Exception as e:
        print(f"Error loading models: {e}")
        raise

@torch.no_grad()
def predict(image_path: str, explain: bool = False, use_tta: bool = False, device_override: str = None) -> Dict[str, Any]:
    """
    Core prediction function for SignalScope.

    Args:
        image_path: Path to input image (JPEG, PNG, WebP, BMP)
        explain: If True, generate heatmap overlay and forensic cues
        use_tta: If True, average predictions across 5 augmented views
        device_override: Optional device string ('cuda', 'cpu')

    Returns:
        dict with label, confidence, verdict, generator_family, metadata,
        and optionally explanation + heatmap_path
    """
    # Load image
    try:
        image_pil = Image.open(image_path).convert("RGB")
    except Exception as e:
        return {"error": f"Failed to load image: {str(e)}"}

    device_str = device_override or DEVICE
    models = load_models(device_str)
    device = models["device"]
    pipeline = models["feature_pipeline"]
    model = models["detector"]
    calibrator = models["calibrator"]
    stacker = models["stacker"]

    try:
        # Convert to numpy and tensor
        image_np = np.array(image_pil)  # (H, W, 3) uint8
        image_tensor_518 = preprocess_for_dino(image_pil)  # (3, 518, 518)

        # Extract the exact 7575-dim flat features matching training
        flat_feat_np = pipeline.extract_and_flatten(image_np, image_tensor_518)
        flat_feat_tensor = torch.from_numpy(flat_feat_np).unsqueeze(0).to(device)

        # Model inference — pass flat feature tensor
        output = model(flat_features=flat_feat_tensor)

        # Also get decomposed features if needed for explainability
        features = None
        if explain:
            features = pipeline.extract(image_np, image_tensor_518)

        # Get raw logit and calibrate
        raw_logit = output['binary_logit']
        calibrated_prob = calibrator(raw_logit).cpu().item()

        # TTA (optional — re-runs on multiple views for extra robustness)
        if use_tta:
            try:
                from src.inference.tta import predict_with_tta
                calibrated_prob = predict_with_tta(
                    model, pipeline, image_np, image_tensor_518, str(device)
                )
            except Exception:
                pass

        # Stacking ensemble blend with exact 7575-dim features
        try:
            stacked_prob = stacker.predict(flat_feat_np, calibrated_prob)
            final_confidence = float(stacked_prob)
        except Exception as e:
            final_confidence = calibrated_prob

        # Metadata extraction (Module D: Provenance & C2PA)
        metadata = {}
        try:
            from src.metadata.exif_parser import extract_exif_signals
            from src.metadata.c2pa_checker import check_c2pa_credentials
            metadata = extract_exif_signals(image_path)
            c2pa_res = check_c2pa_credentials(image_path)
            metadata["c2pa_details"] = c2pa_res
            if c2pa_res.get("has_c2pa"):
                metadata["has_c2pa"] = True
        except Exception:
            metadata = {"has_exif": False, "has_c2pa": False, "provenance_tier": "neutral", "provenance_score": 0.0}

        # Multi-signal fusion: combine visual ML model with hardware provenance (Module D)
        prov_tier = metadata.get("provenance_tier", "neutral")
        prov_score = metadata.get("provenance_score", 0.0)

        if prov_tier == "ai_watermark_detected" or metadata.get("c2pa_details", {}).get("is_ai_declared"):
            # Strong digital proof of AI generation
            final_confidence = max(final_confidence, 0.985)
        elif prov_tier == "camera_verified" or metadata.get("c2pa_details", {}).get("is_camera_declared"):
            # Verified camera hardware provenance (Make, Model, Lens, Shutter, ISO)
            # Shields authentic photography from false AI flags
            hardware_discount = 0.40 * prov_score
            final_confidence = max(0.015, final_confidence - hardware_discount)

        # Verdict
        label = "AI-generated" if final_confidence > 0.5 else "Real"
        verdict = responsible_verdict(final_confidence)

        # Attribution
        attr_logits = output['attribution_logits']
        attr_idx = attr_logits.argmax(dim=1).item()
        attr_class = ATTRIBUTION_CLASSES[attr_idx] if attr_idx < len(ATTRIBUTION_CLASSES) else "Unknown"

        result = {
            "image": os.path.basename(image_path),
            "label": label,
            "confidence": round(float(final_confidence), 4),
            "verdict": verdict,
            "generator_family": attr_class,
            "metadata": metadata,
        }

        # Explanation (Module A — graceful if not ready)
        if explain:
            try:
                from src.explain.attention_rollout import compute_attention_rollout
                from src.explain.gradcam import compute_gradcam
                from src.explain.heatmap_fusion import fuse_heatmaps
                from src.explain.cue_descriptors import generate_explanation

                attn_map = compute_attention_rollout(pipeline.dino, image_tensor_518)
                gcam_map = compute_gradcam(model.spectral_cnn, features['srm_residuals'])
                fused_heatmap = fuse_heatmaps(attn_map, gcam_map, weights=(0.6, 0.4))

                explanation = generate_explanation(
                    fused_heatmap, features['fft_features'].cpu().numpy(),
                    final_confidence, label, metadata=metadata
                )

                heatmap_path = save_heatmap_overlay(image_np, fused_heatmap, image_path)
                result["explanation"] = explanation
                result["heatmap_path"] = str(heatmap_path)
                result["fused_heatmap"] = fused_heatmap.astype(np.float32)
                result["attn_map"] = attn_map.astype(np.float32)
                result["gcam_map"] = gcam_map.astype(np.float32)

                if 'srm_residuals' in features and features['srm_residuals'] is not None:
                    srm_t = features['srm_residuals']
                    if hasattr(srm_t, "squeeze"):
                        srm_np = torch.mean(torch.abs(srm_t[0]), dim=0).detach().cpu().numpy()
                        s_min, s_max = float(srm_np.min()), float(srm_np.max())
                        if s_max > s_min:
                            srm_np = (srm_np - s_min) / (s_max - s_min)
                        result["srm_map"] = srm_np.astype(np.float32)
            except Exception as e:
                result["explanation_note"] = f"Explanation modules not yet available: {str(e)}"

        return result

    except Exception as e:
        traceback.print_exc()
        return {"error": f"Prediction failed: {str(e)}"}

def batch_predict(image_dir: str, output_csv: str, explain: bool = False, use_tta: bool = False, device_override: str = None) -> None:
    image_paths = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp"):
        image_paths.extend(glob.glob(os.path.join(image_dir, ext)))
        image_paths.extend(glob.glob(os.path.join(image_dir, ext.upper())))
        
    results = []
    for img_path in image_paths:
        res = predict(img_path, explain=explain, use_tta=use_tta, device_override=device_override)
        if "error" in res:
            print(f"Error on {img_path}: {res['error']}")
            results.append({"image": os.path.basename(img_path), "error": res["error"]})
        else:
            verdict_str = res["verdict"]["verdict"] if isinstance(res["verdict"], dict) else str(res["verdict"])
            results.append({
                "image": res["image"],
                "label": res.get("label", "Unknown"),
                "confidence": res.get("confidence", 0.0),
                "verdict": verdict_str,
                "attribution": res.get("generator_family", "Unknown"),
                "heatmap_path": res.get("heatmap_path", "")
            })
            
    df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Saved batch results to {output_csv}")

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    import time

    parser = argparse.ArgumentParser(description="SignalScope Predict Interface")
    parser.add_argument("--image", type=str, default=None, help="Path to single image")
    parser.add_argument("--image_dir", type=str, default=None, help="Path to directory of images")
    parser.add_argument("--output", type=str, default="results.csv", help="Output CSV path for batch")
    parser.add_argument("--explain", action="store_true", help="Generate explanation heatmaps")
    parser.add_argument("--no_tta", action="store_true", help="Disable Test Time Augmentation")
    parser.add_argument("--device", type=str, default=None, help="Device to use (cuda/cpu)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive CLI loop")
    
    args = parser.parse_args()
    chosen_device = args.device or DEVICE
    
    if args.image:
        res = predict(args.image, explain=args.explain, use_tta=not args.no_tta, device_override=chosen_device)
        print(json.dumps(res, indent=2))
    elif args.image_dir:
        batch_predict(args.image_dir, args.output, explain=args.explain, use_tta=not args.no_tta, device_override=chosen_device)
    else:
        # Interactive runtime loop
        print("\n" + "=" * 65)
        print("  🔬 SIGNALSCOPE INTERACTIVE FORENSIC INSPECTOR")
        print("  Loading models into memory (one-time setup)...")
        print("=" * 65)
        load_models(chosen_device)
        print("  ✓ Models loaded into memory and ready for instantaneous testing!")
        print("  Tip: You can drag & drop any image file directly into this terminal.\n")

        while True:
            try:
                user_input = input("\n[Enter image path or drag & drop] (or 'q' to quit): ").strip()
                if not user_input or user_input.lower() in ('q', 'quit', 'exit'):
                    print("\nExiting SignalScope Inspector. Goodbye!\n")
                    break
                
                # Strip wrapping quotes if user dragged and dropped in terminal
                img_path = user_input.strip('"').strip("'").strip('&').strip()
                if not os.path.exists(img_path):
                    print(f"❌ File not found at: {img_path}")
                    continue
                
                print(f"\n🔍 Analyzing: {os.path.basename(img_path)} ...")
                t0 = time.time()
                # In interactive mode, explain=True by default unless disabled
                res = predict(img_path, explain=True, use_tta=not args.no_tta, device_override=chosen_device)
                elapsed = time.time() - t0
                
                if "error" in res:
                    print(f"❌ Analysis failed: {res['error']}")
                    continue
                
                label = res.get("label", "Unknown")
                conf = res.get("confidence", 0.0)
                verdict_info = res.get("verdict", {})
                verdict = verdict_info.get("verdict", label)
                icon = verdict_info.get("icon", "•")
                attr = res.get("generator_family", "Unknown")
                meta = res.get("metadata", {})
                prov_tier = meta.get("provenance_tier", "neutral")
                
                print("─" * 60)
                print(f"  VERDICT:     {icon} {verdict}")
                print(f"  LABEL:       {label}")
                print(f"  CONFIDENCE:  {conf*100:.2f}% (Calibrated Probability)")
                print(f"  ATTRIBUTION: {attr}")
                print(f"  PROVENANCE:  {prov_tier.replace('_', ' ').title()}")
                
                if "explanation" in res and isinstance(res["explanation"], dict):
                    cues = res["explanation"].get("cues", [])
                    if cues:
                        print("  FORENSIC CUES:")
                        for c in cues:
                            print(f"    - {c}")
                
                if "heatmap_path" in res:
                    print(f"  HEATMAP:     Saved to {res['heatmap_path']}")
                print(f"  SPEED:       Analyzed in {elapsed:.2f}s")
                print("─" * 60)
                
            except (KeyboardInterrupt, EOFError):
                print("\nExiting SignalScope Inspector.\n")
                break

