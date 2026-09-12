import torch
import torch.nn as nn
import numpy as np
import cv2

class JPEGGhostFeatures(nn.Module):
    """
    Extracts JPEG Ghost features by repeatedly re-compressing the image 
    at different quality levels and comparing the differences.
    """
    def __init__(self):
        super(JPEGGhostFeatures, self).__init__()
        # 10 qualities as specified
        self.qualities = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Extract JPEG Ghost features.
        Args:
            x (torch.Tensor): Image batch, shape (B, C, H, W). 
                              Expected range is [0, 1] or [0, 255].
        Returns:
            torch.Tensor: Feature vector of shape (B, 20).
        """
        device = x.device
        B, C, H, W = x.shape
        
        # Ensure values are roughly [0, 255] for JPEG compression
        if x.max() <= 2.0:
            x_255 = x * 255.0
        else:
            x_255 = x
            
        x_255 = torch.clamp(x_255, 0, 255)
        
        # We need to process this on CPU with OpenCV
        x_np = x_255.detach().cpu().numpy().astype(np.uint8)
        
        # Ensure it's channels-last for OpenCV: (B, H, W, C)
        x_np = np.transpose(x_np, (0, 2, 3, 1))
        
        # If 1-channel, cv2 imencode handles it. 
        # If 3-channel, PyTorch is RGB but cv2 expects BGR for JPEG compression?
        # Actually JPEG standard defines YCbCr, but OpenCV's imencode accepts BGR by default.
        # However, for simply measuring compression noise, whether we encode RGB or BGR 
        # as the input channels produces the exact same magnitude of compression error 
        # on the channels themselves. But let's be technically correct and swap to BGR if C==3.
        if C == 3:
            # RGB to BGR
            x_bgr = x_np[..., ::-1].copy()
        else:
            x_bgr = x_np
            
        batch_features = []
        
        for i in range(B):
            img = x_bgr[i]
            img_float = img.astype(np.float32)
            
            img_features = []
            
            for q in self.qualities:
                # Encode
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), q]
                success, encoded_img = cv2.imencode('.jpg', img, encode_param)
                
                if not success:
                    # Fallback if compression fails (e.g. empty image)
                    img_features.extend([0.0, 0.0])
                    continue
                    
                # Decode
                decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_UNCHANGED)
                
                if decoded_img is None or decoded_img.shape != img.shape:
                    img_features.extend([0.0, 0.0])
                    continue
                    
                # Calculate difference
                # Convert to float to avoid uint8 overflow/underflow
                decoded_float = decoded_img.astype(np.float32)
                
                diff = np.abs(img_float - decoded_float)
                
                mean_diff = float(np.mean(diff))
                std_diff = float(np.std(diff))
                
                img_features.extend([mean_diff, std_diff])
                
            batch_features.append(img_features)
            
        # Convert to tensor
        features_tensor = torch.tensor(batch_features, dtype=torch.float32, device=device)
        
        return features_tensor

