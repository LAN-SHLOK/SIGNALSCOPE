import torch
import torch.nn as nn
from typing import Dict
from src.config import TOTAL_FEATURE_DIM, SPECTRAL_CNN_OUT_DIM

class SpectralCNN(nn.Module):
    """
    9ch input -> 4 conv layers (32->64->128->256) with BN+ReLU -> AdaptiveAvgPool -> (B, 256)
    """
    def __init__(self):
        super(SpectralCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(9, 32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            
            nn.Conv2d(128, 256, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True)
        )
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: (B, 9, H, W)
        Returns: (B, 256)
        """
        x = self.features(x)
        x = self.pool(x)
        x = torch.flatten(x, 1)
        return x

class SpectralMLP(nn.Module):
    """
    128-dim input -> 256 -> 128 with ReLU + Dropout(0.2)
    """
    def __init__(self):
        super(SpectralMLP, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(128, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2)
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: (B, 128)
        Returns: (B, 128)
        """
        return self.net(x)

class SignalScopeDetector(nn.Module):
    """
    Dual-stream fusion detector for SignalScope.
    """
    def __init__(self):
        super(SignalScopeDetector, self).__init__()
        self.spectral_cnn = SpectralCNN()
        self.spectral_mlp = SpectralMLP()
        
        self.fusion_mlp = nn.Sequential(
            nn.Linear(TOTAL_FEATURE_DIM, 1024),
            nn.BatchNorm1d(1024),
            nn.GELU(),
            nn.Dropout(0.4),
            nn.Linear(1024, 256),
            nn.BatchNorm1d(256),
            nn.GELU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.GELU()
        )
        
        self.binary_head = nn.Linear(128, 1)
        self.attribution_head = nn.Linear(128, 4)
        
    def forward(self, cls_multi: torch.Tensor = None, patch_stats: torch.Tensor = None, 
                srm_residuals: torch.Tensor = None, fft_features: torch.Tensor = None, 
                jpeg_features: torch.Tensor = None, bayer_features: torch.Tensor = None,
                flat_features: torch.Tensor = None, **kwargs) -> Dict[str, torch.Tensor]:
        """
        Forward pass for the SignalScope detector.
        Supports both raw decomposed features and pre-cached (B, 7575) flat vectors.
        """
        if flat_features is not None:
            shared_features = self.fusion_mlp(flat_features)
        elif cls_multi is not None and cls_multi.ndim == 2 and cls_multi.shape[1] == TOTAL_FEATURE_DIM:
            shared_features = self.fusion_mlp(cls_multi)
        else:
            srm_features = self.spectral_cnn(srm_residuals)
            fft_processed = self.spectral_mlp(fft_features)
            
            combined_features = torch.cat([
                cls_multi, patch_stats, srm_features, fft_processed, jpeg_features, bayer_features
            ], dim=1)
            shared_features = self.fusion_mlp(combined_features)
        
        binary_logit = self.binary_head(shared_features)
        binary_prob = torch.sigmoid(binary_logit)
        attribution_logits = self.attribution_head(shared_features)
        
        return {
            'binary_logit': binary_logit,
            'binary_prob': binary_prob,
            'attribution_logits': attribution_logits,
            'shared_features': shared_features
        }
