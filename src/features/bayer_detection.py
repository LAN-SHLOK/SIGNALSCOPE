import numpy as np
from scipy.signal import convolve2d

def bayer_autocorrelation_features(image_gray: np.ndarray) -> np.ndarray:
    """
    Detect Bayer CFA traces using autocorrelation on high-pass filtered center patch.
    
    Args:
        image_gray: (H, W) grayscale numpy array.
        
    Returns:
        (2,) float32 array: [has_bayer_trace, confidence]
    """
    H, W = image_gray.shape
    features = np.zeros(2, dtype=np.float32)
    
    if H < 64 or W < 64:
        return features
        
    # Get center 64x64 patch
    cy, cx = H // 2, W // 2
    patch = image_gray[cy-32:cy+32, cx-32:cx+32].astype(np.float32)
    
    # High-pass filter (Laplacian-like)
    kernel = np.array([[ 0, -1,  0],
                       [-1,  4, -1],
                       [ 0, -1,  0]], dtype=np.float32)
                       
    residual = convolve2d(patch, kernel, mode='same', boundary='symm')
    
    # Autocorrelation via FFT
    f = np.fft.fft2(residual)
    p = np.abs(f)**2
    autocorr = np.fft.ifft2(p)
    autocorr = np.fft.fftshift(np.real(autocorr))
    
    # Normalize autocorrelation
    center_val = autocorr[32, 32]
    if center_val > 0:
        autocorr /= center_val
        
    # Check for 2-pixel periodicity (peaks at (32, 30), (32, 34), (30, 32), (34, 32))
    # We examine the neighboring pixels
    
    # A simple metric: average of peaks at lag 2 vs lag 1
    lag2_val = (autocorr[32, 30] + autocorr[32, 34] + autocorr[30, 32] + autocorr[34, 32]) / 4.0
    lag1_val = (autocorr[32, 31] + autocorr[32, 33] + autocorr[31, 32] + autocorr[33, 32]) / 4.0
    
    if lag2_val > lag1_val:
        features[0] = 1.0 # has bayer trace
        features[1] = float(lag2_val - lag1_val) # confidence
    else:
        features[0] = 0.0
        features[1] = 0.0
        
    return features
