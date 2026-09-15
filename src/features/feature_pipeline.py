import torch
import numpy as np
import cv2
from typing import Dict, List, Any

from src.config import *
from src.features.dino_backbone import DINOv2MultiLayerExtractor
from src.features.patch_statistics import compute_patch_statistics
from src.features.srm_filters import MultiColorspaceSRM
from src.features.frequency import azimuthal_power_spectrum
from src.features.jpeg_ghost import jpeg_ghost_features
from src.features.bayer_detection import bayer_autocorrelation_features


class FeaturePipeline:
    """
    Master feature pipeline that orchestrates all feature extractors into a single structure.
    Extracts DINOv2 features, SRM residuals, and classical features (FFT, JPEG ghost, Bayer).
    """

    def __init__(self, device: str = 'cuda'):
        """
        Initializes the feature pipeline, loading models to the specified device.
        """
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        
        # Initialize DINOv2 backbone
        self.dino = DINOv2MultiLayerExtractor().to(self.device)
        self.dino.eval()
        
        # Initialize SRM filters
        self.srm = MultiColorspaceSRM().to(self.device)
        self.srm.eval()

    def to(self, device):
        self.device = torch.device(device)
        if hasattr(self, 'dino'):
            self.dino.to(self.device)
        if hasattr(self, 'srm'):
            self.srm.to(self.device)
        return self

    def eval(self):
        if hasattr(self, 'dino'):
            self.dino.eval()
        if hasattr(self, 'srm'):
            self.srm.eval()
        return self

    @torch.no_grad()
    def extract(self, image_rgb_np: np.ndarray, image_tensor_518: torch.Tensor) -> Dict[str, Any]:
        """
        Extracts all features for a single image.

        Args:
            image_rgb_np: (H, W, 3) uint8 numpy array in RGB format.
            image_tensor_518: (3, 518, 518) normalized float tensor for DINOv2.

        Returns:
            Dictionary containing:
                - cls_multi: (1, 4096) tensor
                - patch_stats: (1, 3073) tensor
                - patch_tokens: (1, 1369, 1024) tensor
                - srm_residuals: (1, 9, H, W) tensor
                - fft_features: (1, 128) numpy array
                - jpeg_features: (1, 20) numpy array
                - bayer_features: (1, 2) numpy array
        """
        if image_rgb_np is None or image_rgb_np.size == 0 or image_tensor_518 is None:
            raise ValueError("Corrupt or empty image input provided to FeaturePipeline.")
            
        try:
            # 1. DINOv2 Features
            img_t = image_tensor_518.unsqueeze(0).to(self.device)
            cls_multi, patch_tokens = self.dino(img_t)
            patch_stats = compute_patch_statistics(patch_tokens)
            
            # 2. Colorspace conversions for SRM (standardized to 518x518 for resolution invariance)
            if image_rgb_np.shape[:2] != (DINO_INPUT_SIZE, DINO_INPUT_SIZE):
                interp = cv2.INTER_AREA if (image_rgb_np.shape[0] > DINO_INPUT_SIZE) else cv2.INTER_CUBIC
                img_srm_rgb = cv2.resize(image_rgb_np, (DINO_INPUT_SIZE, DINO_INPUT_SIZE), interpolation=interp)
            else:
                img_srm_rgb = image_rgb_np

            img_ycrcb = cv2.cvtColor(img_srm_rgb, cv2.COLOR_RGB2YCrCb)
            img_hsv = cv2.cvtColor(img_srm_rgb, cv2.COLOR_RGB2HSV)
            
            def to_tensor(img: np.ndarray) -> torch.Tensor:
                t = torch.from_numpy(img).permute(2, 0, 1).float().unsqueeze(0) / 255.0
                return t.to(self.device)
            
            rgb_t = to_tensor(img_srm_rgb)
            ycrcb_t = to_tensor(img_ycrcb)
            hsv_t = to_tensor(img_hsv)
            
            # Extract SRM residuals (B, 9, 518, 518)
            srm_residuals = self.srm(rgb_t, ycrcb_t, hsv_t)
            
            # 3. Classical Features
            gray = cv2.cvtColor(image_rgb_np, cv2.COLOR_RGB2GRAY)
            bgr = cv2.cvtColor(image_rgb_np, cv2.COLOR_RGB2BGR)
            
            fft_feat = azimuthal_power_spectrum(gray)
            jpeg_feat = jpeg_ghost_features(bgr)
            bayer_feat = bayer_autocorrelation_features(gray)
            
            return {
                "cls_multi": cls_multi,
                "patch_stats": patch_stats,
                "patch_tokens": patch_tokens,
                "srm_residuals": srm_residuals,
                "fft_features": torch.from_numpy(fft_feat).float().unsqueeze(0).to(self.device),
                "jpeg_features": torch.from_numpy(jpeg_feat).float().unsqueeze(0).to(self.device),
                "bayer_features": torch.from_numpy(bayer_feat).float().unsqueeze(0).to(self.device)
            }
        except Exception as e:
            raise RuntimeError(f"Error during feature extraction: {str(e)}") from e

    def extract_batch(self, image_list: List[np.ndarray], tensor_list: List[torch.Tensor]) -> Dict[str, Any]:
        """
        Extracts features for a batch of images.
        """
        if not image_list or not tensor_list or len(image_list) != len(tensor_list):
            raise ValueError("Invalid batch inputs. Lists must be non-empty and of equal length.")

        batch_res = {}
        for img_np, img_t in zip(image_list, tensor_list):
            res = self.extract(img_np, img_t)
            for k, v in res.items():
                if k not in batch_res:
                    batch_res[k] = []
                batch_res[k].append(v)
                
        # Concatenate results along batch dimension
        for k in batch_res:
            if isinstance(batch_res[k][0], torch.Tensor):
                batch_res[k] = torch.cat(batch_res[k], dim=0)
            else:
                batch_res[k] = np.concatenate(batch_res[k], axis=0)
                
        return batch_res

    def extract_and_flatten(self, image_rgb_np: np.ndarray, image_tensor_518: torch.Tensor) -> np.ndarray:
        """
        Extracts all features and returns a single flat 7575-dim vector per image.
        This vector is primarily used for LightGBM stacking or disk caching.
        
        The 7575 dims consist of:
        - 4096 (DINOv2 cls_multi)
        - 3073 (DINOv2 patch_stats)
        - 256 (SpectralCNN on SRM residuals - returning zeros here as placeholder since SpectralCNN is part of Fusion)
        - 128 (FFT azimuthal)
        - 20 (JPEG ghost)
        - 2 (Bayer autocorrelation)
        """
        return self.flatten_dict(res)

    def flatten_dict(self, res: Dict[str, Any]) -> np.ndarray:
        """
        Converts an already extracted feature dict into the flat 7575-dim vector.
        Avoids redundant forward passes when extract() was already called.
        """
        def to_flat_np(x):
            if isinstance(x, torch.Tensor):
                return x.detach().cpu().numpy().flatten()
            return np.asarray(x).flatten()
            
        cls_multi = to_flat_np(res["cls_multi"])
        patch_stats = to_flat_np(res["patch_stats"])
        fft_feat = to_flat_np(res["fft_features"])
        jpeg_feat = to_flat_np(res["jpeg_features"])
        bayer_feat = to_flat_np(res["bayer_features"])
        
        # Placeholder for the 256-dim SpectralCNN embedding output
        spectral_cnn_placeholder = np.zeros(256, dtype=np.float32)
        
        feature_vector = np.concatenate([
            cls_multi,
            patch_stats,
            spectral_cnn_placeholder,
            fft_feat,
            jpeg_feat,
            bayer_feat
        ])
        
        return feature_vector
