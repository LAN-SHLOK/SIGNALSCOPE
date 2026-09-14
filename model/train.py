import os
import json
import math
import argparse
import logging
from pathlib import Path
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import numpy as np
import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import config
from src.data.dataset import create_dataloaders
from src.data.augmentations import get_train_transform, get_val_transform
from src.features.feature_pipeline import FeaturePipeline
from src.models.fusion_detector import SignalScopeDetector
from src.utils.metrics import compute_all_metrics

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_lr_scheduler(optimizer, warmup_steps, total_steps):
    """
    Creates a learning rate scheduler with linear warmup and cosine annealing.
    """
    def lr_lambda(current_step):
        if current_step < warmup_steps:
            return float(current_step) / float(max(1, warmup_steps))
        progress = float(current_step - warmup_steps) / float(max(1, total_steps - warmup_steps))
        return 0.5 * (1.0 + math.cos(math.pi * progress))
    return optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

def train_epoch(model, feature_pipeline, dataloader, optimizer, scheduler, scaler, device, args):
    """
    Trains the model for one epoch.
    """
    model.train()
    if feature_pipeline is not None:
        feature_pipeline.eval() # Ensure frozen feature extractors remain frozen
        
    bce_criterion = nn.BCEWithLogitsLoss()
    ce_criterion = nn.CrossEntropyLoss()
    
    total_loss = 0.0
    all_bin_preds = []
    all_bin_targets = []
    all_attr_preds = []
    all_attr_targets = []
    
    optimizer.zero_grad()
    
    pbar = tqdm(dataloader, desc="Training", leave=False)
    for step, batch in enumerate(pbar):
        labels = batch["label"].to(device).float()
        attr_labels = batch.get("attribution_label", torch.zeros_like(labels)).to(device).long()
        
        is_cuda = device.type == "cuda"
        with torch.autocast(device_type=device.type, enabled=is_cuda):
            if "features" in batch:
                flat_features = batch["features"].to(device)
                outputs = model(flat_features=flat_features)
            elif "image_tensor" in batch:
                img_t = batch["image_tensor"].to(device)
                img_nps = batch["image_rgb_np"]
                if isinstance(img_nps, torch.Tensor):
                    img_nps = img_nps.cpu().numpy()
                with torch.no_grad():
                    features = feature_pipeline.extract_batch(list(img_nps), [img_t[i] for i in range(img_t.shape[0])])
                outputs = model(**features)
            else:
                features = {k: v.to(device) for k, v in batch.items() if k not in ["label", "attribution_label"]}
                outputs = model(**features)
                
            # Label smoothing for binary classification
            smoothed_labels = labels * (1.0 - config.LABEL_SMOOTHING) + 0.5 * config.LABEL_SMOOTHING
            
            # Binary Real/AI loss
            loss_bin = bce_criterion(outputs["binary_logit"].squeeze(-1), smoothed_labels)
            
            # 4-class attribution loss
            loss_attr = ce_criterion(outputs["attribution_logits"], attr_labels)
            
            # Combined multi-task loss
            loss = config.BINARY_LOSS_WEIGHT * loss_bin + config.ATTRIBUTION_LOSS_WEIGHT * loss_attr
            loss = loss / config.GRADIENT_ACCUMULATION_STEPS
            
        # Backward pass with gradient scaling
        scaler.scale(loss).backward()
        
        if (step + 1) % config.GRADIENT_ACCUMULATION_STEPS == 0 or (step + 1) == len(dataloader):
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad()
            scheduler.step()
            
        total_loss += loss.item() * config.GRADIENT_ACCUMULATION_STEPS
        
        # Save predictions for metrics
        with torch.no_grad():
            bin_preds = torch.sigmoid(outputs["binary_logit"].squeeze(-1)).cpu().numpy()
            attr_preds = torch.argmax(outputs["attribution_logits"], dim=1).cpu().numpy()
            
            all_bin_preds.extend(bin_preds)
            all_bin_targets.extend(labels.cpu().numpy())
            all_attr_preds.extend(attr_preds)
            all_attr_targets.extend(attr_labels.cpu().numpy())
            
        pbar.set_postfix({"loss": f"{loss.item() * config.GRADIENT_ACCUMULATION_STEPS:.4f}"})
        
    avg_loss = total_loss / len(dataloader)
    metrics = compute_all_metrics(all_bin_targets, all_bin_preds, all_attr_targets, all_attr_preds)
    metrics["loss"] = avg_loss
    
    return metrics

@torch.no_grad()
def evaluate_epoch(model, feature_pipeline, dataloader, device):
    """
    Evaluates the model on validation data.
    """
    model.eval()
    if feature_pipeline is not None:
        feature_pipeline.eval()
        
    bce_criterion = nn.BCEWithLogitsLoss()
    ce_criterion = nn.CrossEntropyLoss()
    
    total_loss = 0.0
    all_bin_preds = []
    all_bin_targets = []
    all_attr_preds = []
    all_attr_targets = []
    
    pbar = tqdm(dataloader, desc="Evaluating", leave=False)
    for batch in pbar:
        if "features" in batch:
            flat_features = batch["features"].to(device)
            labels = batch["label"].to(device).float()
            attr_labels = batch.get("attribution_label", torch.zeros_like(labels)).to(device).long()
            
            is_cuda = device.type == "cuda"
            with torch.autocast(device_type=device.type, enabled=is_cuda):
                outputs = model(flat_features=flat_features)
        elif "image_tensor" in batch:
            img_t = batch["image_tensor"].to(device)
            img_nps = batch["image_rgb_np"]
            if isinstance(img_nps, torch.Tensor):
                img_nps = img_nps.cpu().numpy()
            features = feature_pipeline.extract_batch(list(img_nps), [img_t[i] for i in range(img_t.shape[0])])
            labels = batch["label"].to(device).float()
            attr_labels = batch.get("attribution_label", torch.zeros_like(labels)).to(device).long()
            
            is_cuda = device.type == "cuda"
            with torch.autocast(device_type=device.type, enabled=is_cuda):
                outputs = model(**features)
        else:
            features = {k: v.to(device) for k, v in batch.items() if k not in ["label", "attribution_label"]}
            labels = batch["label"].to(device).float()
            attr_labels = batch.get("attribution_label", torch.zeros_like(labels)).to(device).long()
            
            is_cuda = device.type == "cuda"
            with torch.autocast(device_type=device.type, enabled=is_cuda):
                outputs = model(**features)
            
        loss_bin = bce_criterion(outputs["binary_logit"].squeeze(-1), labels)
        loss_attr = ce_criterion(outputs["attribution_logits"], attr_labels)
        loss = config.BINARY_LOSS_WEIGHT * loss_bin + config.ATTRIBUTION_LOSS_WEIGHT * loss_attr
            
        total_loss += loss.item()
        
        bin_preds = torch.sigmoid(outputs["binary_logit"].squeeze(-1)).cpu().numpy()
        attr_preds = torch.argmax(outputs["attribution_logits"], dim=1).cpu().numpy()
        
        all_bin_preds.extend(bin_preds)
        all_bin_targets.extend(labels.cpu().numpy())
        all_attr_preds.extend(attr_preds)
        all_attr_targets.extend(attr_labels.cpu().numpy())
        
    avg_loss = total_loss / len(dataloader)
    metrics = compute_all_metrics(all_bin_targets, all_bin_preds, all_attr_targets, all_attr_preds)
    metrics["loss"] = avg_loss
    
    return metrics

def main():
    parser = argparse.ArgumentParser(description="Train SignalScope Dual-Stream Detector")
    parser.add_argument("--data_dir", type=str, default=".", help="Path to dataset directory")
    parser.add_argument("--cache_dir", type=str, default=None, help="Path to pre-cached features directory")
    parser.add_argument("--epochs", type=int, default=config.EPOCHS, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=config.BATCH_SIZE, help="Batch size")
    parser.add_argument("--lr", type=float, default=config.LEARNING_RATE, help="Learning rate")
    parser.add_argument("--device", type=str, default=config.DEVICE, help="Device (cuda/cpu/mps)")
    parser.add_argument("--resume", type=str, default=None, help="Path to checkpoint to resume from")
    args = parser.parse_args()
    
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    # Prepare directories
    weights_dir = Path(config.WEIGHTS_DIR)
    weights_dir.mkdir(parents=True, exist_ok=True)
    
    # Dataloaders
    if args.cache_dir and os.path.exists(args.cache_dir):
        from src.data.dataset import CachedFeatureDataset
        logger.info(f"Loading pre-cached features from {args.cache_dir}...")
        train_ds = CachedFeatureDataset(args.cache_dir, split="train")
        val_ds = CachedFeatureDataset(args.cache_dir, split="val")
        if len(val_ds) == 0:
            val_ds = CachedFeatureDataset(args.cache_dir, split="test")
        train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, drop_last=True)
        val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)
        feature_pipeline = None
    else:
        train_transform = get_train_transform()
        val_transform = get_val_transform()
        
        logger.info("Initializing dataloaders from raw images...")
        dataloaders = create_dataloaders(
            data_dir=args.data_dir,
            batch_size=args.batch_size,
            train_transform=train_transform,
            val_transform=val_transform,
            num_workers=config.NUM_WORKERS
        )
        train_loader = dataloaders["train"]
        val_loader = dataloaders["val"]
        
        # Feature Pipeline
        logger.info("Initializing feature pipeline...")
        feature_pipeline = FeaturePipeline().to(device)
        feature_pipeline.eval()
    
    model = SignalScopeDetector().to(device)
    
    # Optimizer and Scheduler
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=config.WEIGHT_DECAY)
    
    total_steps = len(train_loader) * args.epochs // config.GRADIENT_ACCUMULATION_STEPS
    scheduler = get_lr_scheduler(optimizer, warmup_steps=config.WARMUP_STEPS, total_steps=total_steps)
    
    scaler = torch.cuda.amp.GradScaler(enabled=(device.type == "cuda"))
    
    start_epoch = 0
    best_val_auc = 0.0
    patience_counter = 0
    history = {"train": [], "val": []}
    
    # Resume from checkpoint
    if args.resume:
        logger.info(f"Resuming from {args.resume}")
        checkpoint = torch.load(args.resume, map_location=device)
        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
        scaler.load_state_dict(checkpoint["scaler_state_dict"])
        start_epoch = checkpoint["epoch"] + 1
        best_val_auc = checkpoint["best_val_auc"]
        history = checkpoint.get("history", history)
        
    logger.info(f"Starting training for {args.epochs} epochs")
    for epoch in range(start_epoch, args.epochs):
        logger.info(f"Epoch {epoch+1}/{args.epochs}")
        
        # Train
        train_metrics = train_epoch(
            model, feature_pipeline, train_loader, optimizer, scheduler, scaler, device, args
        )
        history["train"].append(train_metrics)
        logger.info(
            f"Train | Loss: {train_metrics['loss']:.4f} | "
            f"Binary AUC: {train_metrics.get('binary_auc', 0):.4f} | "
            f"Binary F1: {train_metrics.get('binary_f1', 0):.4f} | "
            f"Attr Acc: {train_metrics.get('attr_accuracy', 0):.4f}"
        )
        
        # Evaluate
        val_metrics = evaluate_epoch(model, feature_pipeline, val_loader, device)
        history["val"].append(val_metrics)
        logger.info(
            f"Val   | Loss: {val_metrics['loss']:.4f} | "
            f"Binary AUC: {val_metrics.get('binary_auc', 0):.4f} | "
            f"Binary F1: {val_metrics.get('binary_f1', 0):.4f} | "
            f"Attr Acc: {val_metrics.get('attr_accuracy', 0):.4f}"
        )
        
        # Save history safely (handling numpy types)
        def to_serializable(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, (np.float32, np.float64)):
                return float(obj)
            if isinstance(obj, (np.int32, np.int64)):
                return int(obj)
            if isinstance(obj, dict):
                return {k: to_serializable(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [to_serializable(v) for v in obj]
            return obj

        with open(weights_dir / "training_history.json", "w") as f:
            json.dump(to_serializable(history), f, indent=4)
            
        # Checkpoint logic
        val_auc = val_metrics.get("binary_auc", 0)
        is_best = val_auc > best_val_auc
        if is_best:
            best_val_auc = val_auc
            patience_counter = 0
            logger.info(f"New best validation AUC: {best_val_auc:.4f}. Saving model...")
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "scheduler_state_dict": scheduler.state_dict(),
                "scaler_state_dict": scaler.state_dict(),
                "best_val_auc": best_val_auc,
                "history": to_serializable(history)
            }, weights_dir / "detector.pth")
        else:
            patience_counter += 1
            logger.info(f"No improvement in validation AUC. Patience: {patience_counter}/{config.EARLY_STOPPING_PATIENCE}")
            
        if patience_counter >= config.EARLY_STOPPING_PATIENCE:
            logger.info(f"Early stopping triggered after {epoch+1} epochs.")
            break
            
    logger.info("Training complete.")

if __name__ == "__main__":
    main()
