import torch
import torch.nn.functional as F

try:
    from src.config import PATCH_SIM_NUM_SAMPLES
except ImportError:
    # Fallback to default if not present
    PATCH_SIM_NUM_SAMPLES = 200

def compute_patch_statistics(patch_tokens: torch.Tensor) -> torch.Tensor:
    """
    Compute spatial statistics over DINOv2 patch tokens.
    
    Args:
        patch_tokens (torch.Tensor): Input patch tokens of shape (B, 1369, 1024)
        
    Returns:
        torch.Tensor: Statistics tensor of shape (B, 3073).
                      Contains mean(1024) + std(1024) + max(1024) + avg_sim(1)
    """
    B, N, C = patch_tokens.shape
    
    # 1. Mean over spatial dimension (B, 1024)
    mean_feat = patch_tokens.mean(dim=1)
    
    # 2. Standard deviation over spatial dimension (B, 1024)
    std_feat = patch_tokens.std(dim=1, unbiased=False)
    
    # 3. Max pooling over spatial dimension (B, 1024)
    max_feat, _ = patch_tokens.max(dim=1)
    
    # 4. Average Cosine Similarity over random patch pairs (B, 1)
    # Using random sampling to avoid O(N^2) memory footprint
    idx1 = torch.randint(0, N, (PATCH_SIM_NUM_SAMPLES,), device=patch_tokens.device)
    idx2 = torch.randint(0, N, (PATCH_SIM_NUM_SAMPLES,), device=patch_tokens.device)
    
    # Extract the sampled patch tokens
    # Shape: (B, PATCH_SIM_NUM_SAMPLES, C)
    patches1 = patch_tokens[:, idx1, :]
    patches2 = patch_tokens[:, idx2, :]
    
    # Compute cosine similarity along feature dimension
    # Output shape: (B, PATCH_SIM_NUM_SAMPLES)
    cos_sim = F.cosine_similarity(patches1, patches2, dim=2)
    
    # Average the similarities over the samples -> (B, 1)
    avg_sim = cos_sim.mean(dim=1, keepdim=True)
    
    # Concatenate all statistical features
    # (B, 1024) + (B, 1024) + (B, 1024) + (B, 1) -> (B, 3073)
    stats = torch.cat([mean_feat, std_feat, max_feat, avg_sim], dim=1)
    
    return stats
