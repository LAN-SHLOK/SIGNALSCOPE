import cv2
import numpy as np
import copy
from typing import Callable, List, Dict, Any, Tuple
from sklearn.metrics import roc_auc_score

# Degradation conditions planned:
# JPEG: 10, 20, 30, 50, 70, 90
# Resize: 0.25, 0.5, 0.75
# Blur: 1, 3, 5, 7
# Screenshot, SaltAndPepper

def degrade_image(image: np.ndarray, degradation: str, severity: Any = None, seed: int = None) -> np.ndarray:
    """
    Apply a specific degradation to an image.
    Args:
        image (np.ndarray): Input image in RGB format (H, W, 3), dtype uint8.
        degradation (str): Name of the degradation (e.g., 'jpeg', 'resize', 'blur', 'screenshot', 'salt_pepper').
        severity (Any): Parameter for the degradation (e.g., quality level, scale factor, sigma).
        seed (int): Optional random seed for deterministic noise.
    Returns:
        np.ndarray: Degraded image.
    """
    if seed is not None:
        np.random.seed(seed)
        
    img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) if len(image.shape) == 3 and image.shape[2] == 3 else image
        
    if degradation == 'jpeg':
        quality = int(severity)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, encimg = cv2.imencode('.jpg', img_bgr, encode_param)
        decimg = cv2.imdecode(encimg, cv2.IMREAD_UNCHANGED)
        result_bgr = decimg
        
    elif degradation == 'resize':
        scale = float(severity)
        h, w = img_bgr.shape[:2]
        new_h, new_w = max(1, int(h * scale)), max(1, int(w * scale))
        # Downscale
        small = cv2.resize(img_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
        # Upscale back to original size for model input compatibility
        result_bgr = cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)
        
    elif degradation == 'blur':
        sigma = float(severity)
        # kernel size should be roughly 3*sigma or 4*sigma, odd
        ksize = int(2 * np.ceil(2 * sigma) + 1)
        result_bgr = cv2.GaussianBlur(img_bgr, (ksize, ksize), sigma)
        
    elif degradation == 'screenshot':
        # Simulate screenshot by reducing color depth (e.g., posterization) and adding slight JPEG compression
        # This is a common heuristic for screenshot artifacts
        reduced_depth = (img_bgr // 16) * 16
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
        _, encimg = cv2.imencode('.jpg', reduced_depth, encode_param)
        result_bgr = cv2.imdecode(encimg, cv2.IMREAD_UNCHANGED)
        
    elif degradation == 'salt_pepper':
        prob = severity if severity is not None else 0.02
        noise = np.random.rand(*img_bgr.shape[:2])
        result_bgr = img_bgr.copy()
        # Salt
        result_bgr[noise < (prob / 2)] = 255
        # Pepper
        result_bgr[noise > 1 - (prob / 2)] = 0
        
    else:
        # Unknown degradation, return original
        result_bgr = img_bgr

    # Convert back to RGB
    if len(result_bgr.shape) == 3 and result_bgr.shape[2] == 3:
        return cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)
    return result_bgr


def get_planned_degradations() -> List[Dict[str, Any]]:
    """
    Returns the list of 15+ planned degradation conditions.
    """
    return [
        {'degradation': 'clean', 'severity': None},
        {'degradation': 'jpeg', 'severity': 90},
        {'degradation': 'jpeg', 'severity': 70},
        {'degradation': 'jpeg', 'severity': 50},
        {'degradation': 'jpeg', 'severity': 30},
        {'degradation': 'jpeg', 'severity': 20},
        {'degradation': 'jpeg', 'severity': 10},
        {'degradation': 'resize', 'severity': 0.75},
        {'degradation': 'resize', 'severity': 0.50},
        {'degradation': 'resize', 'severity': 0.25},
        {'degradation': 'blur', 'severity': 1},
        {'degradation': 'blur', 'severity': 3},
        {'degradation': 'blur', 'severity': 5},
        {'degradation': 'blur', 'severity': 7},
        {'degradation': 'screenshot', 'severity': None},
        {'degradation': 'salt_pepper', 'severity': 0.05}
    ]


def run_degradation_suite(
    eval_func: Callable[[List[np.ndarray]], np.ndarray],
    images: List[np.ndarray],
    labels: np.ndarray,
    seed: int = 42
) -> List[Dict[str, Any]]:
    """
    Runs a suite of degradations and computes the resulting performance.
    Args:
        eval_func: A callable that takes a list of images and returns a 1D array of prediction probabilities.
        images: List of clean original images.
        labels: 1D array of ground truth labels (0=Real, 1=AI).
        seed: Random seed for deterministic degradation.
    Returns:
        List of dictionaries containing evaluation metrics per degradation.
    """
    results = []
    conditions = get_planned_degradations()
    
    for condition in conditions:
        deg_name = condition['degradation']
        severity = condition['severity']
        
        if deg_name == 'clean':
            degraded_images = images
        else:
            degraded_images = [
                degrade_image(img, deg_name, severity, seed=seed+i if seed else None) 
                for i, img in enumerate(images)
            ]
            
        # Get predictions
        try:
            preds = eval_func(degraded_images)
            
            # Calculate metrics
            # Note: roc_auc_score requires both positive and negative classes in y_true
            if len(np.unique(labels)) > 1:
                auc = roc_auc_score(labels, preds)
            else:
                auc = float('nan') # Cannot compute AUC with only one class
                
            results.append({
                'degradation': deg_name,
                'severity': severity,
                'metric': 'roc_auc',
                'value': auc,
                'n_samples': len(labels)
            })
        except Exception as e:
            results.append({
                'degradation': deg_name,
                'severity': severity,
                'metric': 'roc_auc',
                'value': float('nan'),
                'n_samples': len(labels),
                'error': str(e)
            })
            
    return results


def evaluate_degradation_curve(results: List[Dict[str, Any]], degradation_type: str) -> List[Tuple[Any, float]]:
    """
    Extracts the performance curve for a specific degradation type from the results list.
    Args:
        results: The output from run_degradation_suite.
        degradation_type: The degradation to filter by (e.g., 'jpeg', 'blur').
    Returns:
        A list of tuples (severity, auc_value) sorted by severity (ascending if numeric).
    """
    curve = []
    for r in results:
        if r['degradation'] == degradation_type:
            curve.append((r['severity'], r['value']))
            
    # Attempt to sort if severities are comparable (numeric)
    try:
        curve = sorted(curve, key=lambda x: x[0] if x[0] is not None else 0)
    except TypeError:
        pass
        
    return curve
