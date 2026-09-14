import cv2
import numpy as np
from src.config import JPEG_QUALITY_RANGE

def jpeg_ghost_features(image_bgr: np.ndarray, quality_range=None) -> np.ndarray:
    """
    Extract JPEG ghost features by re-compressing at different qualities.
    
    Args:
        image_bgr: (H, W, 3) numpy array in BGR format.
        quality_range: List of JPEG qualities to test. Default from config.
        
    Returns:
        (2 * len(quality_range),) float32 vector containing mean and std differences.
        Usually (20,) if quality_range has 10 values.
    """
    if quality_range is None:
        quality_range = JPEG_QUALITY_RANGE
        
    n_features = len(quality_range) * 2
    features = np.zeros(n_features, dtype=np.float32)
    
    if len(image_bgr.shape) != 3 or image_bgr.shape[2] != 3:
        return features
        
    if image_bgr.shape[0] < 16 or image_bgr.shape[1] < 16:
        return features
        
    image_float = image_bgr.astype(np.float32)
    
    for i, q in enumerate(quality_range):
        # Re-compress
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), q]
        success, encoded = cv2.imencode('.jpg', image_bgr, encode_param)
        
        if not success:
            continue
            
        decoded = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
        if decoded is None or decoded.shape != image_bgr.shape:
            continue
            
        # Calculate diff
        decoded_float = decoded.astype(np.float32)
        diff = np.abs(image_float - decoded_float)
        
        # We can sum across channels and calculate mean/std spatially
        diff_sum = np.sum(diff, axis=2)
        features[i * 2] = float(np.mean(diff_sum))
        features[i * 2 + 1] = float(np.std(diff_sum))
        
    return features
