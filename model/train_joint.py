import os
import sys
import glob
import time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DEVICE, WEIGHTS_DIR
from src.models.fusion_detector import SignalScopeDetector
from src.models.calibration import TemperatureScaling
from src.models.stacking import StackingEnsemble

def load_all_joint_data(cache_dir="cache"):
    print("Loading all datasets for joint training...")
    all_feats = []
    all_labels = []
    sources = []

    # 1. CIFAKE Cache (2000 samples)
    real_cifake_paths = glob.glob(os.path.join(cache_dir, "train", "REAL", "*.npy"))
    fake_cifake_paths = glob.glob(os.path.join(cache_dir, "train", "FAKE", "*.npy"))
    
    print(f"Found {len(real_cifake_paths)} CIFAKE Real and {len(fake_cifake_paths)} CIFAKE Fake samples.")
    for p in real_cifake_paths:
        all_feats.append(np.load(p))
        all_labels.append(0)
        sources.append("cifake_real")
    for p in fake_cifake_paths:
        all_feats.append(np.load(p))
        all_labels.append(1)
        sources.append("cifake_ai")

    # 2. Multi-Domain Cache (Smartphone + Hemg + Modern AI)
    # Oversampled 4x to give strong weight to authentic camera photos
    md_feats_p = os.path.join(cache_dir, "true_multidomain_feats.npy")
    md_labels_p = os.path.join(cache_dir, "true_multidomain_labels.npy")
    if os.path.exists(md_feats_p) and os.path.exists(md_labels_p):
        md_feats = np.load(md_feats_p)
        md_labels = np.load(md_labels_p)
        print(f"Found Multi-Domain Cache: {len(md_feats)} samples. Oversampling 4x...")
        for _ in range(4):
            for f, l in zip(md_feats, md_labels):
                all_feats.append(f)
                all_labels.append(int(l))
                sources.append("smartphone_multidomain")

    # 3. Defactify / MS COCOAI Cache
    defact_feats_p = os.path.join(cache_dir, "defactify_feats.npy")
    defact_labels_p = os.path.join(cache_dir, "defactify_labels_a.npy")
    if os.path.exists(defact_feats_p) and os.path.exists(defact_labels_p):
        defact_feats = np.load(defact_feats_p)
        defact_labels = np.load(defact_labels_p)
        print(f"Found Defactify MS COCOAI Cache: {len(defact_feats)} samples.")
        for f, l in zip(defact_feats, defact_labels):
            all_feats.append(f)
            all_labels.append(int(l))
            sources.append("defactify_mscocoai")

    X = np.array(all_feats, dtype=np.float32)
    y = np.array(all_labels, dtype=np.int64)

    print(f"\nTotal Joint Dataset Size: {X.shape[0]} samples, {X.shape[1]} features")
    unique, counts = np.unique(y, return_counts=True)
    for u, c in zip(unique, counts):
        name = "Real" if u == 0 else "AI-generated"
        print(f"  Class {u} ({name}): {c} samples ({c/len(y)*100:.1f}%)")

    return X, y

def train_joint(epochs: int = 12, lr: float = 2e-5, batch_size: int = 32):
    X, y = load_all_joint_data()
    device = torch.device(DEVICE)

    # Train / Val Split (stratified)
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    print(f"Train split: {len(X_train)} samples | Val split: {len(X_val)} samples")

    train_ds = TensorDataset(torch.from_numpy(X_train), torch.from_numpy(y_train).float())
    val_ds = TensorDataset(torch.from_numpy(X_val), torch.from_numpy(y_val).float())

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    # Warm-start detector
    detector = SignalScopeDetector().to(device)
    detector_path = os.path.join(WEIGHTS_DIR, "detector.pth")
    if os.path.exists(detector_path):
        print(f"Warm-starting from existing weights: {detector_path}")
        ckpt = torch.load(detector_path, map_location=device)
        state_dict = ckpt.get("model_state_dict", ckpt) if isinstance(ckpt, dict) and "model_state_dict" in ckpt else ckpt
        detector.load_state_dict(state_dict)
    else:
        print("Warning: No checkpoint found, initializing from scratch.")

    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(detector.fusion_mlp.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)

    print(f"\nStarting joint fine-tuning for {epochs} epochs (micro-lr={lr})...")
    best_val_auc = 0.0

    for epoch in range(1, epochs + 1):
        detector.train()
        train_loss = 0.0
        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device).unsqueeze(1)

            optimizer.zero_grad()
            out = detector(flat_features=batch_x)
            logits = out['binary_logit']
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * len(batch_x)

        scheduler.step()
        train_loss /= len(X_train)

        # Validation
        detector.eval()
        val_logits = []
        with torch.no_grad():
            for batch_x, _ in val_loader:
                batch_x = batch_x.to(device)
                out = detector(flat_features=batch_x)
                val_logits.append(out['binary_logit'].cpu().numpy())

        val_logits = np.concatenate(val_logits).flatten()
        val_probs = 1.0 / (1.0 + np.exp(-val_logits))
        val_preds = (val_probs > 0.5).astype(int)

        val_acc = accuracy_score(y_val, val_preds)
        val_auc = roc_auc_score(y_val, val_probs)
        val_f1 = f1_score(y_val, val_preds)

        print(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {train_loss:.4f} | Val Acc: {val_acc:.4f} | Val AUC: {val_auc:.4f} | Val F1: {val_f1:.4f}")

    # Save fine-tuned detector
    torch.save({"model_state_dict": detector.state_dict()}, detector_path)
    print(f"\nSaved fine-tuned detector to {detector_path}")

    # ── 2. Re-fit Temperature Scaling ──────────────────────────────────────────
    print("\nFitting Temperature Scaling calibrator...")
    detector.eval()
    with torch.no_grad():
        all_val_x = torch.from_numpy(X_val).to(device)
        val_out = detector(flat_features=all_val_x)
        raw_val_logits = val_out['binary_logit'].squeeze(-1)

    calibrator = TemperatureScaling().to(device)
    fitted_temp = calibrator.fit(raw_val_logits, torch.from_numpy(y_val).float().to(device))
    calibrator_path = os.path.join(WEIGHTS_DIR, "calibrator.pth")
    torch.save(calibrator.state_dict(), calibrator_path)
    print(f"Fitted temperature: {fitted_temp:.4f}, saved to {calibrator_path}")

    # ── 3. Retrain Stacking Ensemble ────────────────────────────────────────────
    print("\nRetraining Stacking Ensemble (HistGradientBoosting + Meta-Learner)...")
    detector.eval()
    with torch.no_grad():
        all_train_x = torch.from_numpy(X_train).to(device)
        train_out = detector(flat_features=all_train_x)
        mlp_train_preds = calibrator(train_out['binary_logit'].squeeze(-1)).cpu().numpy()

        all_val_x = torch.from_numpy(X_val).to(device)
        val_out = detector(flat_features=all_val_x)
        mlp_val_preds = calibrator(val_out['binary_logit'].squeeze(-1)).cpu().numpy()

    stacker = StackingEnsemble()
    stacker.fit(X_train, y_train, mlp_train_preds)
    stacker_path = os.path.join(WEIGHTS_DIR, "stacker.joblib")
    stacker.save(stacker_path)

    # Evaluate stacked model
    stacked_val_preds = stacker.predict(X_val, mlp_val_preds)
    stacked_auc = roc_auc_score(y_val, stacked_val_preds)
    stacked_acc = accuracy_score(y_val, (stacked_val_preds > 0.5).astype(int))
    print(f"Stacked Val AUC: {stacked_auc:.4f} | Stacked Val Accuracy: {stacked_acc:.4f}")
    print("Joint training complete!")

if __name__ == "__main__":
    train_joint()
