import os
import sys
import tempfile
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from datasets import load_dataset
from model.predict import predict

@pytest.mark.network
def test_defactify_unseen():
    print("=" * 65)
    print("TESTING ON UNSEEN DEFACTIFY (MS COCOAI) TEST SPLIT")
    print("=" * 65)

    source_names = {
        0: "MS COCO (Real)",
        1: "Stable Diffusion 2.1",
        2: "SDXL",
        3: "Stable Diffusion 3",
        4: "DALL-E 3",
        5: "Midjourney v6"
    }

    ds = load_dataset('Rajarshi-Roy-research/Defactify_Image_Dataset', split='test', streaming=True)

    correct = 0
    total = 0

    for i, item in enumerate(ds):
        if i >= 12:
            break
        expected = "Real" if item["Label_A"] == 0 else "AI-generated"
        src_name = source_names.get(int(item["Label_B"]), "Unknown")

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name
            item["Image"].convert("RGB").save(tmp_path)

        try:
            res = predict(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        pred = res.get("label", "Unknown")
        conf = res.get("confidence", 0.0)
        verdict = res.get("verdict", {}).get("verdict", "")

        is_match = (pred == expected)
        if is_match:
            correct += 1
        total += 1

        status = "PASS" if is_match else "FAIL"
        print(f"[{status}] #{i+1:02d} | Src: {src_name:22s} | Exp: {expected:12s} | Pred: {pred:12s} | Conf: {conf:.4f}")

    print("=" * 65)
    print(f"Unseen Test Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")
    print("=" * 65)

if __name__ == "__main__":
    test_defactify_unseen()
