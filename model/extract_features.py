import os
import time
import argparse
import logging
from pathlib import Path

import sys
import numpy as np
import pandas as pd
import torch
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.features.feature_pipeline import FeaturePipeline
from src.data.dataset import SignalScopeDataset
from src.data.augmentations import get_val_transform
from src.config import DINO_INPUT_SIZE, DEVICE, CACHE_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@torch.no_grad()
def extract_and_cache(data_dir: Path, cache_dir: Path, max_samples: int = None):
    """
    Extracts features for all splits and saves them to cache_dir.
    
    Args:
        data_dir (Path): Base dataset directory (e.g., data/cifake).
        cache_dir (Path): Directory to save cached features.
        max_samples (int): Optional maximum number of samples to extract per split.
    """
    device = torch.device(DEVICE if torch.cuda.is_available() else "cpu")
    logging.info(f"Initializing FeaturePipeline on {device}...")
    pipeline = FeaturePipeline().to(device)
    pipeline.eval()
    
    transform = get_val_transform()
    splits = ['train', 'val', 'test']
    
    for split in splits:
        split_dir = data_dir / split
        if not split_dir.exists():
            logging.warning(f"Split directory {split_dir} not found. Skipping.")
            continue
            
        logging.info(f"Processing split: {split}")
        dataset = SignalScopeDataset(root_dir=str(data_dir), split=split, transform=transform)
        
        # If max_samples is set, balance the samples across classes
        if max_samples is not None and hasattr(dataset, 'samples'):
            from collections import defaultdict
            class_samples = defaultdict(list)
            for s in dataset.samples:
                class_samples[s[1]].append(s)
            
            per_class = max_samples // len(class_samples)
            balanced_samples = []
            for cls_id, s_list in class_samples.items():
                balanced_samples.extend(s_list[:per_class])
            dataset.samples = balanced_samples
            logging.info(f"Subsampled {len(dataset.samples)} balanced samples ({per_class} per class).")
            
        split_cache_dir = cache_dir / split
        split_cache_dir.mkdir(parents=True, exist_ok=True)
        
        labels_info = []
        labels_file = split_cache_dir / "labels.csv"
        
        start_time = time.time()
        processed_count = 0
        skipped_count = 0
        error_count = 0
        
        from torch.utils.data import DataLoader
        from src.features.patch_statistics import compute_patch_statistics
        from src.features.frequency import azimuthal_power_spectrum
        from src.features.jpeg_ghost import jpeg_ghost_features
        from src.features.bayer_detection import bayer_autocorrelation_features
        import cv2

        batch_size = 8 if torch.cuda.is_available() else 2
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0)
        placeholder = np.zeros(256, dtype=np.float32)

        for batch in tqdm(loader, desc=f"Extracting {split}"):
            try:
                img_paths = batch.get("image_path", [])
                labels = batch["label"].numpy()
                img_nps = batch["image_rgb_np"]
                img_t = batch["image_tensor"].to(device)

                # Check if all in batch are already cached
                all_cached = True
                batch_npy_paths = []
                for j in range(len(img_paths)):
                    p = Path(img_paths[j])
                    c_name = p.parent.name if p.parent else "unknown"
                    c_dir = split_cache_dir / c_name
                    c_dir.mkdir(parents=True, exist_ok=True)
                    npy_p = c_dir / (p.stem + ".npy")
                    batch_npy_paths.append((npy_p, c_name, p))
                    if not npy_p.exists():
                        all_cached = False

                if all_cached:
                    for j, (npy_p, c_name, p) in enumerate(batch_npy_paths):
                        skipped_count += 1
                        labels_info.append({
                            "file_path": str(npy_p),
                            "label": int(labels[j]),
                            "class_name": c_name,
                            "original_image": str(p)
                        })
                    continue

                # GPU forward pass for the batch
                is_cuda = device.type == "cuda"
                with torch.no_grad(), torch.autocast(device_type=device.type, dtype=torch.float16, enabled=is_cuda):
                    cls_m, patches = pipeline.dino(img_t)
                    stats = compute_patch_statistics(patches)

                cls_np = cls_m.float().cpu().numpy()
                stats_np = stats.float().cpu().numpy()

                for j, (npy_p, c_name, p) in enumerate(batch_npy_paths):
                    if npy_p.exists():
                        skipped_count += 1
                        labels_info.append({
                            "file_path": str(npy_p),
                            "label": int(labels[j]),
                            "class_name": c_name,
                            "original_image": str(p)
                        })
                        continue

                    # Extract CPU classical features
                    raw_np = img_nps[j].numpy() if isinstance(img_nps, torch.Tensor) else img_nps[j]
                    if isinstance(raw_np, torch.Tensor):
                        raw_np = raw_np.cpu().numpy()

                    gray = cv2.cvtColor(raw_np, cv2.COLOR_RGB2GRAY)
                    bgr = cv2.cvtColor(raw_np, cv2.COLOR_RGB2BGR)

                    fft_f = azimuthal_power_spectrum(gray)
                    jpeg_f = jpeg_ghost_features(bgr)
                    bayer_f = bayer_autocorrelation_features(gray)

                    features = np.concatenate([cls_np[j], stats_np[j], placeholder, fft_f, jpeg_f, bayer_f])
                    np.save(str(npy_p), features)

                    labels_info.append({
                        "file_path": str(npy_p),
                        "label": int(labels[j]),
                        "class_name": c_name,
                        "original_image": str(p)
                    })
                    processed_count += 1

            except Exception as e:
                logging.warning(f"Error processing batch: {e}")
                error_count += 1

        # Save labels to CSV
        if labels_info:
            df = pd.DataFrame(labels_info)
            df.to_csv(labels_file, index=False)
            
        elapsed_time = time.time() - start_time
        images_per_sec = processed_count / elapsed_time if elapsed_time > 0 else 0
        
        logging.info(f"Split {split} completed.")
        logging.info(f"Processed: {processed_count}, Skipped: {skipped_count}, Errors: {error_count}")
        logging.info(f"Time taken: {elapsed_time:.2f}s ({images_per_sec:.2f} images/sec)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and cache features for SignalScope.")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to dataset directory.")
    parser.add_argument("--cache_dir", type=str, default=str(CACHE_DIR), help="Directory to save cached features.")
    parser.add_argument("--max_samples", type=int, default=None, help="Max samples to extract per split (default: all).")
    
    args = parser.parse_args()
    
    data_path = Path(args.data_dir)
    cache_path = Path(args.cache_dir)
    
    extract_and_cache(data_path, cache_path, max_samples=args.max_samples)
