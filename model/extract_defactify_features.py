import os
import sys
import time
from pathlib import Path
import numpy as np
from PIL import Image
from datasets import load_dataset
from tqdm import tqdm

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DEVICE
from src.features.feature_pipeline import FeaturePipeline
from model.predict import preprocess_for_dino

def extract_defactify_dataset(
    target_real: int = 800,
    target_per_ai: int = 160,
    cache_dir: str = "cache",
    batch_save_interval: int = 50
):
    """
    Extracts 7575-dim feature vectors from MS COCOAI (Defactify 4.0).
    Balanced across Real and 5 generative models:
      0: Real (MS COCO)
      1: SD 2.1
      2: SDXL
      3: SD 3
      4: DALL-E 3
      5: Midjourney v6
    """
    os.makedirs(cache_dir, exist_ok=True)
    feats_path = os.path.join(cache_dir, "defactify_feats.npy")
    labels_a_path = os.path.join(cache_dir, "defactify_labels_a.npy")
    labels_b_path = os.path.join(cache_dir, "defactify_labels_b.npy")

    targets = {
        0: target_real,
        1: target_per_ai,
        2: target_per_ai,
        3: target_per_ai,
        4: target_per_ai,
        5: target_per_ai
    }
    total_target = sum(targets.values())

    # Check for existing checkpoint
    if os.path.exists(feats_path) and os.path.exists(labels_a_path) and os.path.exists(labels_b_path):
        feats_list = list(np.load(feats_path))
        labels_a_list = list(np.load(labels_a_path))
        labels_b_list = list(np.load(labels_b_path))
        current_counts = {}
        for b in labels_b_list:
            current_counts[b] = current_counts.get(b, 0) + 1
        print(f"Resuming from existing cache: {len(feats_list)} samples already extracted.")
        print(f"Current class counts: {current_counts}")
    else:
        feats_list = []
        labels_a_list = []
        labels_b_list = []
        current_counts = {k: 0 for k in targets}

    # Check if target already reached
    if all(current_counts.get(k, 0) >= targets[k] for k in targets):
        print(f"Target of {total_target} already reached. Nothing to extract.")
        return

    print(f"Initializing FeaturePipeline on {DEVICE}...")
    pipeline = FeaturePipeline(device=DEVICE)
    pipeline.eval()

    print("Connecting to HuggingFace streaming dataset: Rajarshi-Roy-research/Defactify_Image_Dataset (split='train')...")
    ds = load_dataset("Rajarshi-Roy-research/Defactify_Image_Dataset", split="train", streaming=True)

    pbar = tqdm(total=total_target, initial=len(feats_list), desc="Extracting MS COCOAI Features")
    saved_count = 0

    for item in ds:
        label_b = int(item["Label_B"])
        label_a = int(item["Label_A"])

        if current_counts.get(label_b, 0) >= targets.get(label_b, 0):
            continue

        try:
            img_pil = item["Image"]
            if img_pil.mode != "RGB":
                img_pil = img_pil.convert("RGB")
            
            img_np = np.array(img_pil)
            img_tensor = preprocess_for_dino(img_pil)

            # Extract 7575-dim flat vector
            feat_vec = pipeline.extract_and_flatten(img_np, img_tensor)
            
            feats_list.append(feat_vec)
            labels_a_list.append(label_a)
            labels_b_list.append(label_b)
            current_counts[label_b] = current_counts.get(label_b, 0) + 1

            pbar.update(1)
            saved_count += 1

            # Save checkpoint periodically
            if saved_count % batch_save_interval == 0:
                np.save(feats_path, np.array(feats_list, dtype=np.float32))
                np.save(labels_a_path, np.array(labels_a_list, dtype=np.int64))
                np.save(labels_b_path, np.array(labels_b_list, dtype=np.int64))

            if all(current_counts.get(k, 0) >= targets[k] for k in targets):
                print("\nAll target counts reached successfully!")
                break

        except Exception as e:
            print(f"\nWarning: Failed on sample: {e}")
            continue

    pbar.close()

    # Final save
    np.save(feats_path, np.array(feats_list, dtype=np.float32))
    np.save(labels_a_path, np.array(labels_a_list, dtype=np.int64))
    np.save(labels_b_path, np.array(labels_b_list, dtype=np.int64))
    print(f"\nExtraction complete! Saved {len(feats_list)} samples to {cache_dir}/")
    print(f"Final class distribution: {current_counts}")

if __name__ == "__main__":
    extract_defactify_dataset()
