import numpy as np
import cv2
from src.config import FFT_BINS, DINO_INPUT_SIZE

def azimuthal_power_spectrum(image_gray: np.ndarray, n_bins: int = FFT_BINS) -> np.ndarray:
    """
    Compute the FFT azimuthal (radially averaged) power spectrum.
    
    Standardized to a scale-invariant 518x518 grid with orthonormal FFT normalization
    so that 12MP camera photos, standard web photos, and small thumbnails produce 
    comparable, resolution-invariant spectral distributions.
    
    Args:
        image_gray: (H, W) numpy array, grayscale image.
        n_bins: number of frequency bins for radial average.
        
    Returns:
        (n_bins,) float32 feature vector.
    """
    if len(image_gray.shape) != 2:
        raise ValueError("Input image must be grayscale (H, W).")
        
    H, W = image_gray.shape
    
    # Standardize spatial dimensions to eliminate resolution bias
    if (H, W) != (DINO_INPUT_SIZE, DINO_INPUT_SIZE):
        interp = cv2.INTER_AREA if (H > DINO_INPUT_SIZE or W > DINO_INPUT_SIZE) else cv2.INTER_CUBIC
        image_gray = cv2.resize(image_gray, (DINO_INPUT_SIZE, DINO_INPUT_SIZE), interpolation=interp)
        H, W = DINO_INPUT_SIZE, DINO_INPUT_SIZE
    
    # Orthonormal FFT (divided by sqrt(H*W) to preserve Parseval energy)
    f_transform = np.fft.fft2(image_gray, norm="ortho")
    f_shift = np.fft.fftshift(f_transform)
    
    # Power spectrum (log magnitude)
    magnitude_spectrum = np.log1p(np.abs(f_shift))
    
    # Calculate radial distance for each pixel
    Y, X = np.indices((H, W))
    center = (H // 2, W // 2)
    distances = np.sqrt((Y - center[0])**2 + (X - center[1])**2)
    
    # Max distance from center to corner
    max_dist = np.max(distances)
    
    # Create radial bins
    bins = np.linspace(0, max_dist, n_bins + 1)
    
    # Calculate radial average
    radial_prof = np.zeros(n_bins, dtype=np.float32)
    for i in range(n_bins):
        mask = (distances >= bins[i]) & (distances < bins[i+1])
        if np.any(mask):
            radial_prof[i] = np.mean(magnitude_spectrum[mask])
            
    return radial_prof
