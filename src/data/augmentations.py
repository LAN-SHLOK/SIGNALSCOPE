"""
SignalScope — Data Augmentations Pipeline
Provides robust train and validation transforms for deep visual detection.
"""
from torchvision import transforms

def get_train_transform(image_size: int = 518):
    """Training transformations with standard random augmentations."""
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

def get_val_transform(image_size: int = 518):
    """Validation transformations with deterministic resize and normalization."""
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
