import torch
import torch.nn as nn
import torch.nn.functional as F


def rgb_to_ycbcr(image: torch.Tensor) -> torch.Tensor:
    """
    Convert RGB image to YCbCr color space.
    Expects input shape (B, 3, H, W) and values in [0, 1].
    Outputs (B, 3, H, W) with YCbCr values.
    """
    # BT.601 conversion
    r = image[:, 0, :, :]
    g = image[:, 1, :, :]
    b = image[:, 2, :, :]
    
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 0.5
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 0.5
    
    return torch.stack([y, cb, cr], dim=1)


def rgb_to_hsv(image: torch.Tensor) -> torch.Tensor:
    """
    Convert RGB image to HSV color space.
    Expects input shape (B, 3, H, W) and values in [0, 1].
    Outputs (B, 3, H, W) where H, S, V are in [0, 1].
    """
    r, g, b = image[:, 0, :, :], image[:, 1, :, :], image[:, 2, :, :]
    max_c, argmax_c = image.max(dim=1)
    min_c, _ = image.min(dim=1)
    
    v = max_c
    delta = max_c - min_c
    
    s = torch.zeros_like(v)
    mask_s = max_c > 0.0
    s[mask_s] = delta[mask_s] / max_c[mask_s]
    
    h = torch.zeros_like(v)
    mask_h = delta > 0.0
    
    # Calculate H
    r_eq_max = (argmax_c == 0) & mask_h
    g_eq_max = (argmax_c == 1) & mask_h
    b_eq_max = (argmax_c == 2) & mask_h
    
    h[r_eq_max] = ((g[r_eq_max] - b[r_eq_max]) / delta[r_eq_max]) % 6.0
    h[g_eq_max] = ((b[g_eq_max] - r[g_eq_max]) / delta[g_eq_max]) + 2.0
    h[b_eq_max] = ((r[b_eq_max] - g[b_eq_max]) / delta[b_eq_max]) + 4.0
    
    h = h / 6.0  # Normalize to [0, 1]
    
    return torch.stack([h, s, v], dim=1)


class SRMFilters(nn.Module):
    """
    Spatial Rich Model (SRM) fixed high-pass filters.
    Applies 3 filters (1st-order, 2nd-order, 3rd-order) across 
    3 color spaces (RGB, YCbCr, HSV) to produce a 9-channel residual map.
    """
    def __init__(self):
        super(SRMFilters, self).__init__()
        
        # Define SRM filters (3x3)
        # 1. First-order
        f1 = torch.tensor([[ 0.,  0.,  0.],
                           [ 0., -1.,  0.],
                           [ 0.,  1.,  0.]])
        # 2. Second-order (Laplacian)
        f2 = torch.tensor([[ 0.,  1.,  0.],
                           [ 1., -4.,  1.],
                           [ 0.,  1.,  0.]])
        # 3. Third-order
        f3 = torch.tensor([[-1.,  2., -1.],
                           [ 2., -4.,  2.],
                           [-1.,  2., -1.]])
        
        # Normalize filters
        f1 = f1 / 1.0
        f2 = f2 / 4.0
        f3 = f3 / 4.0
        
        # We have 3 filters. We want to extract 3 channels per color space.
        # This implies we collapse the 3 channels of each color space to 1 channel before filtering
        # because 3 filters * 3 color spaces = 9 channels output.
        # Let's stack filters: (3, 1, 3, 3)
        kernels = torch.stack([f1, f2, f3], dim=0).unsqueeze(1)
        
        # Register the filters as a fixed buffer
        self.register_buffer('weight', kernels)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Extract SRM residuals.
        Args:
            x (torch.Tensor): RGB image batch, shape (B, 3, H, W).
        Returns:
            torch.Tensor: Residual map, shape (B, 9, H, W).
        """
        # Ensure values are float and roughly [0, 1]
        if x.max() > 2.0:
            x = x / 255.0
            
        # Color space conversions
        x_rgb = x
        x_ycbcr = rgb_to_ycbcr(x)
        x_hsv = rgb_to_hsv(x)
        
        # Reduce each color space to 1 channel (e.g., luminance or V channel)
        # For RGB: mean across channels
        # For YCbCr: Y channel
        # For HSV: V channel
        c_rgb = x_rgb.mean(dim=1, keepdim=True)
        c_ycbcr = x_ycbcr[:, 0:1, :, :]
        c_hsv = x_hsv[:, 2:3, :, :]
        
        # Apply filters (conv2d with padding=1 keeps spatial dims)
        res_rgb = F.conv2d(c_rgb, self.weight, padding=1)
        res_ycbcr = F.conv2d(c_ycbcr, self.weight, padding=1)
        res_hsv = F.conv2d(c_hsv, self.weight, padding=1)
        
        # Concatenate residuals along channel dimension -> (B, 9, H, W)
        residuals = torch.cat([res_rgb, res_ycbcr, res_hsv], dim=1)
        
        return residuals
