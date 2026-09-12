import torch
import torch.nn as nn
import torch.nn.functional as F

class BayerDetectionFeatures(nn.Module):
    """
    Extracts Bayer/CFA demosaicing traces from an image.
    Outputs a 2-dimensional feature vector per image.
    """
    def __init__(self, patch_size: int = 128):
        super(BayerDetectionFeatures, self).__init__()
        self.patch_size = patch_size
        
        # High-pass filter to expose noise residuals
        hp_filter = torch.tensor([[ -1.,  2., -1.],
                                  [  2., -4.,  2.],
                                  [ -1.,  2., -1.]]) / 4.0
        
        # Shape (1, 1, 3, 3)
        self.register_buffer('hp_kernel', hp_filter.view(1, 1, 3, 3))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Extract Bayer trace features.
        Args:
            x (torch.Tensor): Image batch, shape (B, C, H, W).
        Returns:
            torch.Tensor: Feature vector of shape (B, 2).
        """
        B, C, H, W = x.shape
        device = x.device
        
        # 1. Convert to grayscale if necessary
        if C == 3:
            # Luminance
            x_gray = 0.299 * x[:, 0:1, :, :] + 0.587 * x[:, 1:2, :, :] + 0.114 * x[:, 2:3, :, :]
        else:
            x_gray = x.mean(dim=1, keepdim=True)
            
        # 2. Extract central patch (handle small images)
        p_size = min(self.patch_size, H, W)
        if p_size < 4:
            # Image is pathologically small, return zeros
            return torch.zeros(B, 2, device=device)
            
        start_y = (H - p_size) // 2
        start_x = (W - p_size) // 2
        
        patch = x_gray[:, :, start_y:start_y+p_size, start_x:start_x+p_size]
        
        # 3. High-pass residual
        # Use reflection padding to preserve size without edge artifacts
        patch_padded = F.pad(patch, (1, 1, 1, 1), mode='reflect')
        residual = F.conv2d(patch_padded, self.hp_kernel)
        
        # Zero-mean the residual patch
        residual = residual - residual.mean(dim=(-2, -1), keepdim=True)
        
        # 4. Autocorrelation via FFT
        # padding to avoid circular convolution wrapping
        pad_size = p_size // 2
        res_padded = F.pad(residual, (pad_size, pad_size, pad_size, pad_size))
        
        fft_res = torch.fft.fft2(res_padded)
        power_spec = torch.abs(fft_res) ** 2
        autocorr = torch.fft.ifft2(power_spec).real
        
        # Shift zero-lag to center
        autocorr = torch.fft.fftshift(autocorr, dim=(-2, -1))
        
        # Normalize autocorrelation by the variance (center peak)
        cy, cx = autocorr.shape[-2] // 2, autocorr.shape[-1] // 2
        center_peak = autocorr[:, :, cy, cx].unsqueeze(-1).unsqueeze(-1)
        # Avoid division by zero
        center_peak = torch.clamp(center_peak, min=1e-8)
        
        autocorr_norm = autocorr / center_peak
        
        # 5. Extract periodic structural features
        # A common Bayer trace appears at lags (0,2), (2,0), (1,1) etc.
        # We extract two summary statistics representing periodic confidence:
        # F1: Average of (0,2) and (2,0) lags
        # F2: (1,1) lag
        
        # Since cy, cx is the (0,0) lag:
        # lag (0,2) is cy, cx+2
        # lag (2,0) is cy+2, cx
        # lag (1,1) is cy+1, cx+1
        
        f1 = (autocorr_norm[:, 0, cy, cx+2] + autocorr_norm[:, 0, cy+2, cx]) / 2.0
        f2 = autocorr_norm[:, 0, cy+1, cx+1]
        
        # Stack into (B, 2)
        features = torch.stack([f1, f2], dim=1)
        
        return features

