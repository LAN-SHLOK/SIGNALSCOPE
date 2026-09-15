"""
SignalScope — Dataset and Data Loading Implementations
Supports both raw image loading and pre-cached multi-stream feature tensors.
"""
import os
from pathlib import Path
from typing import Optional, Callable, Dict, List, Tuple
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader

class SignalScopeDataset(Dataset):
    """
    Standard PyTorch dataset for binary/multi-class forensic image detection.
    Reads directory structures formatted as:
      root_dir/split/real/
      root_dir/split/fake/
    """
    def __init__(
        self,
        root_dir: str,
        split: str = "train",
        transform: Optional[Callable] = None,
        image_size: int = 518,
    ):
        self.root_dir = Path(root_dir)
        self.split = split
        self.transform = transform
        self.image_size = image_size
        self.samples: List[Tuple[Path, int, int]] = []  # (path, binary_label, attr_label)

        split_dir = self.root_dir / split
        if split_dir.exists():
            for label_name, bin_label in [("real", 0), ("fake", 1), ("ai", 1)]:
                class_dir = split_dir / label_name
                if class_dir.exists():
                    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp"):
                        for img_path in class_dir.glob(ext):
                            attr_label = 0 if bin_label == 0 else 1
                            self.samples.append((img_path, bin_label, attr_label))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        img_path, bin_label, attr_label = self.samples[idx]
        image_pil = Image.open(img_path).convert("RGB")
        image_np = np.array(image_pil.resize((self.image_size, self.image_size)))

        if self.transform is not None:
            image_tensor = self.transform(image_pil)
        else:
            image_tensor = torch.from_numpy(image_np).permute(2, 0, 1).float() / 255.0

        return {
            "image_tensor": image_tensor,
            "image_rgb_np": image_np,
            "label": torch.tensor(bin_label, dtype=torch.float32),
            "attribution_label": torch.tensor(attr_label, dtype=torch.long),
        }


class CachedFeatureDataset(Dataset):
    """
    High-speed dataset reading pre-extracted feature tensors saved as .npz or .pt files.
    """
    def __init__(self, cache_dir: str, split: str = "train"):
        self.cache_dir = Path(cache_dir) / split
        self.files = sorted(list(self.cache_dir.glob("*.npz")) + list(self.cache_dir.glob("*.pt"))) if self.cache_dir.exists() else []

    def __len__(self) -> int:
        return len(self.files)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        file_path = self.files[idx]
        if file_path.suffix == ".npz":
            data = np.load(file_path)
            features = torch.from_numpy(data["features"]).float()
            label = torch.tensor(float(data["label"]), dtype=torch.float32)
            attr = torch.tensor(int(data.get("attribution_label", 0)), dtype=torch.long)
        else:
            data = torch.load(file_path, map_location="cpu")
            features = data["features"].float()
            label = torch.tensor(float(data["label"]), dtype=torch.float32)
            attr = torch.tensor(int(data.get("attribution_label", 0)), dtype=torch.long)

        return {
            "features": features,
            "label": label,
            "attribution_label": attr,
        }

    def get_all(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load all pre-cached features and labels into memory for tabular/stacking models."""
        features_list = []
        labels_list = []
        for i in range(len(self)):
            item = self[i]
            features_list.append(item["features"].numpy())
            labels_list.append(item["label"].numpy())
        if not features_list:
            return np.empty((0, 0)), np.empty((0,))
        return np.vstack(features_list), np.array(labels_list)


def create_dataloaders(
    data_dir: str,
    batch_size: int = 16,
    train_transform: Optional[Callable] = None,
    val_transform: Optional[Callable] = None,
    num_workers: int = 0,
) -> Dict[str, DataLoader]:
    """Create train and val DataLoaders."""
    train_ds = SignalScopeDataset(root_dir=data_dir, split="train", transform=train_transform)
    val_ds = SignalScopeDataset(root_dir=data_dir, split="val", transform=val_transform)
    if len(val_ds) == 0:
        val_ds = SignalScopeDataset(root_dir=data_dir, split="test", transform=val_transform)

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        drop_last=len(train_ds) > batch_size,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )
    return {"train": train_loader, "val": val_loader}
