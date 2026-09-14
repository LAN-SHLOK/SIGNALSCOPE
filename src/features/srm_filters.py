import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiColorspaceSRM(nn.Module):
    """
    Multi-colorspace SRM (Spatial Rich Model) high-pass filters.
    Applies 3 SRM filters (1st-order, 2nd-order, 3rd-order) to 3 color channels,
    yielding 9 channels. We do this for 3 color spaces and average the results.
    """
    def __init__(self):
        super().__init__()
        
        # 1st-order edge
        filter1 = [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, -1, 1, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]]
                   
        # 2nd-order Laplacian (3x3 Laplacian padded to 5x5)
        filter2 = [[0, 0, 0, 0, 0],
                   [0, 0, 1, 0, 0],
                   [0, 1, -4, 1, 0],
                   [0, 0, 1, 0, 0],
                   [0, 0, 0, 0, 0]]
                   
        # 3rd-order SQUARE
        filter3 = [[-1, 2, -2, 2, -1],
                   [2, -6, 8, -6, 2],
                   [-2, 8, -12, 8, -2],
                   [2, -6, 8, -6, 2],
                   [-1, 2, -2, 2, -1]]
                   
        # Normalize weights
        f1 = torch.tensor(filter1, dtype=torch.float32) / 2.0
        f2 = torch.tensor(filter2, dtype=torch.float32) / 4.0
        f3 = torch.tensor(filter3, dtype=torch.float32) / 12.0
        
        # shape: (3, 1, 5, 5) for conv2d
        filters = torch.stack([f1, f2, f3]).unsqueeze(1)
        self.register_buffer('filters', filters)
        
    def apply_srm_single(self, image_tensor: torch.Tensor) -> torch.Tensor:
        """
        Apply 3 SRM filters to each of 3 channels independently.
        Input: (B, 3, H, W)
        Output: (B, 9, H, W)
        """
        B, C, H, W = image_tensor.shape
        residuals = []
        for c in range(C):
            channel = image_tensor[:, c:c+1, :, :]  # (B, 1, H, W)
            filtered = F.conv2d(channel, self.filters, padding=2) # (B, 3, H, W)
            residuals.append(filtered)
            
        # Concatenate channels to get 9 channels
        return torch.cat(residuals, dim=1) # (B, 9, H, W)
        
    @torch.no_grad()
    def forward(self, image_rgb: torch.Tensor, image_ycbcr: torch.Tensor, image_hsv: torch.Tensor) -> torch.Tensor:
        """
        Apply SRM to all 3 color spaces.
        Each input: (B, 3, H, W)
        Output: (B, 9, H, W)
        """
        srm_rgb = self.apply_srm_single(image_rgb)
        srm_ycbcr = self.apply_srm_single(image_ycbcr)
        srm_hsv = self.apply_srm_single(image_hsv)
        
        # Average the residuals from all 3 color spaces
        return (srm_rgb + srm_ycbcr + srm_hsv) / 3.0
