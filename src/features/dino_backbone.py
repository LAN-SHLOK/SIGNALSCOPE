import os
import torch
import torch.nn as nn
from typing import Tuple

# If CUDA is not available, xformers CPU kernel is unsupported in DINOv2; disable it to use standard PyTorch SDPA
if not torch.cuda.is_available():
    os.environ["XFORMERS_DISABLED"] = "1"

try:
    from src.config import DINO_INPUT_SIZE, DINO_EMBED_DIM
except ImportError:
    pass

class DINOv2MultiLayerExtractor(nn.Module):
    """
    DINOv2-reg ViT-L/14 multi-layer feature extractor.
    Extracts features from layers [8, 16, 20, 24].
    Frozen — zero trainable parameters.
    """
    def __init__(self, model_name: str = 'dinov2_vitl14_reg'):
        super().__init__()
        
        # Ensure xformers is disabled on CPU before hub load
        if not torch.cuda.is_available():
            os.environ["XFORMERS_DISABLED"] = "1"
        
        try:
            self.backbone = torch.hub.load('facebookresearch/dinov2', model_name)
        except Exception as e:
            print(f"Warning: Failed to load {model_name}, falling back to dinov2_vitb14_reg. Error: {e}")
            self.backbone = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14_reg')
            
        # Freeze all parameters
        for param in self.backbone.parameters():
            param.requires_grad = False
            
        self.backbone.eval()
        
        # Layers 8, 16, 20, 24 map to 0-indexed indices 7, 15, 19, 23
        self.target_layers = [7, 15, 19, 23]
        
        self._features = {}
        
        def get_hook(name):
            def hook(module, input, output):
                self._features[name] = output
            return hook
            
        # Register forward hooks on the specified layers
        for layer_idx in self.target_layers:
            if layer_idx < len(self.backbone.blocks):
                self.backbone.blocks[layer_idx].register_forward_hook(get_hook(str(layer_idx)))
            
    @torch.no_grad()
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass for DINOv2 extractor.
        
        Args:
            x (torch.Tensor): Input image tensor of shape (B, 3, 518, 518)
            
        Returns:
            Tuple[torch.Tensor, torch.Tensor]:
                - cls_multi: (B, 4096) — CLS tokens from 4 layers concatenated
                - patch_tokens: (B, 1369, 1024) — patch tokens from last layer
        """
        self.backbone.eval()
        self._features.clear()
        
        # Forward pass through the network (hooks will populate self._features)
        out = self.backbone.forward_features(x)
        
        # Extract CLS tokens from hooked outputs (first token is CLS)
        cls_tokens = []
        for layer_idx in self.target_layers:
            if str(layer_idx) in self._features:
                layer_out = self._features[str(layer_idx)]
                cls_tokens.append(layer_out[:, 0, :])
                
        if cls_tokens:
            cls_multi = torch.cat(cls_tokens, dim=1)
        else:
            # Fallback if no hooks executed for some reason
            cls_multi = out['x_norm_clstoken'].repeat(1, 4)
            
        patch_tokens = out['x_norm_patchtokens']
        
        return cls_multi, patch_tokens
