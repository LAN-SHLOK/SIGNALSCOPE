"""
Optimal threshold selection — separate from training.
Finds max-F1 and conservative (FPR < 5%) thresholds.
"""
import numpy as np
from sklearn.metrics import roc_curve, f1_score
from typing import Dict

from src.config import MAX_FPR_CONSERVATIVE


def find_optimal_thresholds(y_true: np.ndarray, y_probs: np.ndarray) -> Dict[str, float]:
    """
    Find two thresholds:
    1. Max-F1 threshold: best balanced performance
    2. Conservative threshold: FPR < 5% (don't wrongly accuse real photos)

    Args:
        y_true: (N,) binary ground truth labels
        y_probs: (N,) predicted probabilities

    Returns:
        dict with max_f1_threshold, max_f1_score,
              conservative_threshold, conservative_tpr
    """
    y_true = np.asarray(y_true, dtype=int)
    y_probs = np.asarray(y_probs, dtype=float)

    # --- Max F1 threshold ---
    thresholds = np.arange(0.01, 1.0, 0.01)
    f1_scores = []
    for t in thresholds:
        preds = (y_probs > t).astype(int)
        # Handle edge case where all predictions are same class
        if len(np.unique(preds)) == 1:
            f1_scores.append(0.0)
        else:
            f1_scores.append(f1_score(y_true, preds, zero_division=0))

    f1_scores = np.array(f1_scores)
    max_f1_idx = np.argmax(f1_scores)
    max_f1_thresh = float(thresholds[max_f1_idx])
    max_f1_val = float(f1_scores[max_f1_idx])

    # --- Conservative threshold (FPR < MAX_FPR_CONSERVATIVE) ---
    fpr, tpr, roc_thresholds = roc_curve(y_true, y_probs)
    conservative_idx = np.where(fpr <= MAX_FPR_CONSERVATIVE)[0]

    if len(conservative_idx) > 0:
        best_conservative = conservative_idx[-1]
        conservative_thresh = float(roc_thresholds[best_conservative])
        conservative_tpr_val = float(tpr[best_conservative])
    else:
        conservative_thresh = 0.95
        conservative_tpr_val = 0.0

    return {
        'max_f1_threshold': max_f1_thresh,
        'max_f1_score': max_f1_val,
        'conservative_threshold': conservative_thresh,
        'conservative_tpr': conservative_tpr_val,
    }
