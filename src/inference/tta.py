"""
Test-Time Augmentation — +1–3% AUC at inference time.
Averages predictions across 5 augmented views of the image.
"""
import torch
import torch.nn.functional as F
import numpy as np
from typing import Dict, Optional

from src.config import TTA_NUM_VIEWS, DINO_INPUT_SIZE


def predict_with_tta(
    model: torch.nn.Module,
    feature_pipeline,
    image_rgb_np: np.ndarray,
    image_tensor_518: torch.Tensor,
    device: str = 'cuda'
) -> float:
    """
    Run TTA: predict on multiple augmented views and average.

    Args:
        model: SignalScopeDetector instance (eval mode)
        feature_pipeline: FeaturePipeline instance
        image_rgb_np: (H, W, 3) uint8 numpy array — original image
        image_tensor_518: (3, 518, 518) normalized tensor
        device: compute device

    Returns:
        float: averaged probability (0 = real, 1 = AI-generated)
    """
    import cv2

    predictions = []

    # View 1: Original
    predictions.append(_predict_single(model, feature_pipeline, image_rgb_np, image_tensor_518, device))

    # View 2: Horizontal flip
    flipped_np = np.ascontiguousarray(image_rgb_np[:, ::-1, :])
    flipped_tensor = torch.flip(image_tensor_518, dims=[2])
    predictions.append(_predict_single(model, feature_pipeline, flipped_np, flipped_tensor, device))

    # View 3: Vertical flip
    vflipped_np = np.ascontiguousarray(image_rgb_np[::-1, :, :])
    vflipped_tensor = torch.flip(image_tensor_518, dims=[1])
    predictions.append(_predict_single(model, feature_pipeline, vflipped_np, vflipped_tensor, device))

    # View 4: Center crop (90%) — resize back to 518×518
    h, w = image_rgb_np.shape[:2]
    margin_h, margin_w = int(h * 0.05), int(w * 0.05)
    cropped_np = image_rgb_np[margin_h:h - margin_h, margin_w:w - margin_w]
    cropped_np = cv2.resize(cropped_np, (w, h))
    # Resize tensor back to 518×518
    cropped_tensor = image_tensor_518[:, 26:-26, 26:-26]  # ~466×466
    cropped_tensor = F.interpolate(
        cropped_tensor.unsqueeze(0), size=(DINO_INPUT_SIZE, DINO_INPUT_SIZE),
        mode='bilinear', align_corners=False
    ).squeeze(0)
    predictions.append(_predict_single(model, feature_pipeline, cropped_np, cropped_tensor, device))

    # View 5: Slight brightness adjustment
    bright_np = np.clip(image_rgb_np.astype(np.float32) * 1.05, 0, 255).astype(np.uint8)
    # Use same tensor (brightness is in pixel space, DINOv2 input is normalized)
    predictions.append(_predict_single(model, feature_pipeline, bright_np, image_tensor_518, device))

    return float(np.mean(predictions))


def _predict_single(
    model: torch.nn.Module,
    feature_pipeline,
    image_rgb_np: np.ndarray,
    image_tensor_518: torch.Tensor,
    device: str
) -> float:
    """Run a single prediction and return binary probability."""
    flat_feat = feature_pipeline.extract_and_flatten(image_rgb_np, image_tensor_518)
    flat_t = torch.from_numpy(flat_feat).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(flat_features=flat_t)

    return output['binary_prob'].cpu().item()
