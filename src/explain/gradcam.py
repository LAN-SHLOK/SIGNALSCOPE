"""
Module A: Grad-CAM and Activation Mapping on SpectralCNN.
Extracts spatial activations from high-pass SRM noise residuals to highlight
manipulation boundaries, high-frequency anomalies, and synthetic textures.
"""

import torch
import numpy as np
import cv2


def compute_gradcam(spectral_cnn, srm_residuals: torch.Tensor) -> np.ndarray:
    """
    Computes spatial activation map on the SpectralCNN convolutional layers.

    Args:
        spectral_cnn: The SpectralCNN module from SignalScopeDetector.
        srm_residuals: (1, 9, H, W) tensor of SRM noise residuals.

    Returns:
        (H, W) float32 heatmap normalized to [0, 1].
    """
    if srm_residuals is None:
        return np.zeros((518, 518), dtype=np.float32)

    device = next(spectral_cnn.parameters()).device if hasattr(spectral_cnn, "parameters") else torch.device("cuda")
    residuals = srm_residuals.to(device)

    try:
        # Forward pass through SpectralCNN feature layers
        x = residuals
        features = spectral_cnn.features
        
        # Forward through layers to obtain last feature map
        feat_map = features(x) # (1, 256, H', W')
        
        # Average across channel activations
        cam = torch.mean(feat_map, dim=1).squeeze(0) # (H', W')
        cam = torch.relu(cam).detach().cpu().numpy()
        
        # Normalize to 0-1
        if cam.max() > cam.min():
            cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        else:
            cam = np.zeros_like(cam)
            
        # Resize to match input residual dimensions
        h_in, w_in = srm_residuals.shape[2], srm_residuals.shape[3]
        cam_resized = cv2.resize(cam.astype(np.float32), (w_in, h_in), interpolation=cv2.INTER_CUBIC)
        return np.clip(cam_resized, 0.0, 1.0)

    except Exception:
        h_in = srm_residuals.shape[2] if srm_residuals.ndim == 4 else 518
        w_in = srm_residuals.shape[3] if srm_residuals.ndim == 4 else 518
        return np.zeros((h_in, w_in), dtype=np.float32)
