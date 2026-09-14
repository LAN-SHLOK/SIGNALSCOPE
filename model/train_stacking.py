import os
import sys
import argparse
import logging
from pathlib import Path
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import roc_auc_score

from src.models.stacking import StackingEnsemble
from src.data.dataset import CachedFeatureDataset
from src.models.fusion_detector import SignalScopeDetector
from src.models.calibration import TemperatureScaling
from src.config import WEIGHTS_DIR, DEVICE, CACHE_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@torch.no_grad()
def get_features_and_logits(dataset, model, device):
    """
    Extracts features and model logits for the given dataset.
    
    Args:
        dataset (CachedFeatureDataset): Dataset returning features and labels.
        model (SignalScopeDetector): Trained MLP detector model.
        device (torch.device): Device to run inference on.
        
    Returns:
        tuple: (features_array, logits_array, labels_array)
    """
    dataloader = DataLoader(dataset, batch_size=256, shuffle=False, num_workers=0)
    all_features = []
    all_logits = []
    all_labels = []
    
    for batch in dataloader:
        features = batch["features"].to(device)
        labels = batch["label"]
        
        # Forward pass through detector using pre-extracted features
        outputs = model(flat_features=features)
        
        if isinstance(outputs, dict):
            logits = outputs["binary_logit"]
        elif isinstance(outputs, tuple):
            logits = outputs[0]
        else:
            logits = outputs
            
        # ensure shape is (batch_size,) if it's (batch_size, 1)
        if len(logits.shape) > 1 and logits.shape[1] == 1:
            logits = logits.squeeze(1)
            
        all_features.append(features.cpu().numpy())
        all_logits.append(logits.cpu().numpy())
        all_labels.append(labels.numpy())
        
    return np.vstack(all_features), np.concatenate(all_logits), np.concatenate(all_labels)

def train_stacking(cache_dir: Path, weights_dir: Path):
    """
    Trains LightGBM stacking on cached features and MLP predictions.
    Also fits TemperatureScaling on validation logits.
    
    Args:
        cache_dir (Path): Path to cached features directory.
        weights_dir (Path): Path to load detector weights and save stacker/calibrator.
    """
    device = torch.device(DEVICE if torch.cuda.is_available() else "cpu")
    logging.info(f"Using device: {device}")
    
    # Load model
    model_path = weights_dir / "detector.pth"
    if not model_path.exists():
        raise FileNotFoundError(f"MLP weights not found at {model_path}")
        
    detector = SignalScopeDetector().to(device)
    ckpt = torch.load(model_path, map_location=device)
    state_dict = ckpt.get("model_state_dict", ckpt) if isinstance(ckpt, dict) and "model_state_dict" in ckpt else ckpt
    detector.load_state_dict(state_dict)
    detector.eval()
    
    # Load Datasets
    logging.info("Loading cached features datasets...")
    train_dataset = CachedFeatureDataset(str(cache_dir), split="train")
    val_dataset = CachedFeatureDataset(str(cache_dir), split="val")
    if len(val_dataset) == 0:
        logging.info("Validation set not found or empty, using test set for validation/calibration...")
        val_dataset = CachedFeatureDataset(str(cache_dir), split="test")
    
    logging.info(f"Loaded {len(train_dataset)} train samples, {len(val_dataset)} val/test samples.")
    
    logging.info("Extracting logits for training set...")
    train_feat, train_logits, train_labels = get_features_and_logits(train_dataset, detector, device)
    
    logging.info("Extracting logits for validation set...")
    val_feat, val_logits, val_labels = get_features_and_logits(val_dataset, detector, device)
    
    # Apply sigmoid for probabilities
    train_mlp_probs = torch.sigmoid(torch.tensor(train_logits)).numpy()
    val_mlp_probs = torch.sigmoid(torch.tensor(val_logits)).numpy()
    
    # Train Stacking: fit(features, labels, mlp_preds)
    logging.info("Training LightGBM Stacker...")
    stacker = StackingEnsemble()
    stacker.fit(train_feat, train_labels, train_mlp_probs)
    
    train_stacked_probs = stacker.predict(train_feat, train_mlp_probs)
    val_stacked_probs = stacker.predict(val_feat, val_mlp_probs)
    
    train_mlp_auc = roc_auc_score(train_labels, train_mlp_probs)
    val_mlp_auc = roc_auc_score(val_labels, val_mlp_probs)
    
    train_stack_auc = roc_auc_score(train_labels, train_stacked_probs)
    val_stack_auc = roc_auc_score(val_labels, val_stacked_probs)
    
    logging.info(f"MLP AUC -> Train: {train_mlp_auc:.4f}, Val: {val_mlp_auc:.4f}")
    logging.info(f"Stack AUC -> Train: {train_stack_auc:.4f}, Val: {val_stack_auc:.4f}")
    
    # Train Calibrator
    logging.info("Fitting Temperature Scaling...")
    calibrator = TemperatureScaling()
    calibrator.fit(torch.tensor(val_logits), torch.tensor(val_labels))
    
    # Save Stacker & Calibrator
    weights_dir.mkdir(parents=True, exist_ok=True)
    stacker.save(str(weights_dir / "stacker.joblib"))
    torch.save(calibrator.state_dict(), weights_dir / "calibrator.pth")
    
    logging.info(f"Saved stacker to {weights_dir / 'stacker.joblib'}")
    logging.info(f"Saved calibrator to {weights_dir / 'calibrator.pth'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train LightGBM Stacking on cached features.")
    parser.add_argument("--cache_dir", type=str, default=str(CACHE_DIR), help="Directory of cached features.")
    parser.add_argument("--weights_dir", type=str, default=str(WEIGHTS_DIR), help="Directory to load/save weights.")
    
    args = parser.parse_args()
    
    train_stacking(Path(args.cache_dir), Path(args.weights_dir))
