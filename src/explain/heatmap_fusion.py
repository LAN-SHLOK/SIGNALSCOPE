"""
Module A: Dual-Stream Heatmap Fusion.
Fuses DINOv2 foundation semantic saliency with SpectralCNN forensic noise
activations to produce a unified, faithful heatmap of image anomalies.
"""

import numpy as np
import cv2
from typing import Tuple


def fuse_heatmaps(attn_map: np.ndarray, gcam_map: np.ndarray, weights: Tuple[float, float] = (0.6, 0.4)) -> np.ndarray:
    """
    Fuses semantic attention rollout with forensic spectral Grad-CAM.

    Args:
        attn_map: (H, W) float32 in [0, 1] from DINOv2.
        gcam_map: (H, W) float32 in [0, 1] from SpectralCNN.
        weights: (w_attn, w_gcam) weighting coefficients summing to 1.0.

    Returns:
        (H, W) float32 fused heatmap in [0, 1].
    """
    if attn_map is None and gcam_map is None:
        return np.zeros((518, 518), dtype=np.float32)
    if attn_map is None:
        return gcam_map
    if gcam_map is None:
        return attn_map

    # Ensure identical shape
    h, w = attn_map.shape[:2]
    if gcam_map.shape[:2] != (h, w):
        gcam_map = cv2.resize(gcam_map, (w, h), interpolation=cv2.INTER_LINEAR)

    w_attn, w_gcam = weights
    total_w = w_attn + w_gcam
    w_attn /= total_w
    w_gcam /= total_w

    fused = w_attn * attn_map + w_gcam * gcam_map
    
    # Enhance contrast: stretch min/max to highlight focal anomalies
    p_min, p_max = np.percentile(fused, 2), np.percentile(fused, 98)
    if p_max > p_min:
        fused = np.clip((fused - p_min) / (p_max - p_min), 0.0, 1.0)
        
    return fused.astype(np.float32)
