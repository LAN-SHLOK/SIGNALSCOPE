import torch
import torch.nn as nn
import numpy as np

class FrequencyFeatures(nn.Module):
    """
    Extracts frequency-domain features using 2D FFT and radial averaging.
    Produces exactly 128-dimensional feature vector.
    """
    def __init__(self, num_bins: int = 128):
        super(FrequencyFeatures, self).__init__()
        self.num_bins = num_bins

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Extract FFT radial features.
        Args:
            x (torch.Tensor): Image batch, shape (B, C, H, W)
        Returns:
            torch.Tensor: Frequency features, shape (B, 128)
        """
        B, C, H, W = x.shape
        
        # 1. Convert to grayscale if necessary
        if C == 3:
            # Luminance formulation
            x_gray = 0.299 * x[:, 0, :, :] + 0.587 * x[:, 1, :, :] + 0.114 * x[:, 2, :, :]
        else:
            x_gray = x.mean(dim=1)
            
        # 2. 2D FFT
        # Compute 2D FFT, we use norm='ortho' to ensure stable magnitudes
        fft2d = torch.fft.fft2(x_gray, norm='ortho')
        
        # 3. fftshift (shift zero frequency to center)
        fft2d_shifted = torch.fft.fftshift(fft2d, dim=(-2, -1))
        
        # 4. Power spectrum
        power_spectrum = torch.abs(fft2d_shifted) ** 2
        
        # 5. Log stabilization
        # Add epsilon to prevent log(0)
        power_spectrum_log = torch.log(power_spectrum + 1e-8)
        
        # 6. Radial averaging
        # Create a grid of distances from the center
        center_y, center_x = H // 2, W // 2
        
        # Create coordinate grids
        y_coords = torch.arange(H, device=x.device, dtype=torch.float32) - center_y
        x_coords = torch.arange(W, device=x.device, dtype=torch.float32) - center_x
        
        y_grid, x_grid = torch.meshgrid(y_coords, x_coords, indexing='ij')
        
        # Calculate radial distance
        r_grid = torch.sqrt(y_grid**2 + x_grid**2)
        
        # Max radius is the distance to the corner
        max_r = float(torch.max(r_grid).item())
        
        # Quantize radii into num_bins
        # Avoid division by zero by setting max_r to a small value if 0 (e.g. flat image of size 1x1)
        max_r = max(max_r, 1e-5)
        r_bins = (r_grid * (self.num_bins / max_r)).long()
        
        # Clamp to [0, num_bins - 1] to be safe
        r_bins = torch.clamp(r_bins, 0, self.num_bins - 1)
        
        # Flatten for scatter_add
        # r_bins shape: (H, W) -> (H * W)
        r_bins_flat = r_bins.flatten()
        # power_spectrum_log shape: (B, H, W) -> (B, H * W)
        ps_flat = power_spectrum_log.view(B, -1)
        
        # Initialize output tensor
        radial_profile = torch.zeros(B, self.num_bins, device=x.device, dtype=torch.float32)
        # Initialize count tensor
        counts = torch.zeros(self.num_bins, device=x.device, dtype=torch.float32)
        
        # Expand bins for scatter_add
        # shape: (B, H * W)
        r_bins_expanded = r_bins_flat.unsqueeze(0).expand(B, -1)
        
        # Accumulate sums
        radial_profile.scatter_add_(1, r_bins_expanded, ps_flat)
        
        # Accumulate counts
        # counts is just based on the grid, so we can do it once for the batch
        counts.scatter_add_(0, r_bins_flat, torch.ones_like(r_bins_flat, dtype=torch.float32))
        
        # Average
        counts = counts.unsqueeze(0).expand(B, -1)
        # Avoid division by zero
        radial_profile = radial_profile / torch.clamp(counts, min=1.0)
        
        # If any bin had 0 counts (which might happen depending on geometry), 
        # it remains 0.0, which is safe.
        
        return radial_profile

