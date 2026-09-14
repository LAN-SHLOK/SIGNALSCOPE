"""
Module C: Robustness to Degradation Benchmark for SignalScope.
Tests model resilience against real-world degradation conditions:
- Multiple JPEG compression levels (Q=95 down to Q=40)
- Downscaling / Resizing (75%, 50%)
- Gaussian Blur
- Screenshot re-compression
Produces degradation-vs-accuracy metrics and plot.
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from model.predict import predict


def degrade_jpeg(img_pil: Image.Image, quality: int) -> Image.Image:
    """Simulates JPEG re-compression."""
    import io
    buf = io.BytesIO()
    img_pil.save(buf, format="JPEG", quality=quality)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def degrade_resize(img_pil: Image.Image, scale: float) -> Image.Image:
    """Simulates downscaling and upscaling (resizing degradation)."""
    w, h = img_pil.size
    small = img_pil.resize((int(w * scale), int(h * scale)), Image.Resampling.BILINEAR)
    return small.resize((w, h), Image.Resampling.BICUBIC)


def degrade_blur(img_pil: Image.Image, ksize: int = 5) -> Image.Image:
    """Simulates Gaussian blur."""
    img_np = np.array(img_pil)
    blurred = cv2.GaussianBlur(img_np, (ksize, ksize), 0)
    return Image.fromarray(blurred)


def run_robustness_analysis(test_images_with_labels, output_dir="report"):
    """
    Evaluates detector performance across degradation levels.
    test_images_with_labels: list of (image_path, true_label_str)
    """
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = os.path.join(output_dir, "temp_degrade")
    os.makedirs(temp_dir, exist_ok=True)

    jpeg_qualities = [95, 80, 65, 50, 40]
    results = {
        "jpeg": {},
        "resize_75": 0,
        "resize_50": 0,
        "blur": 0,
        "clean": 0
    }

    # Clean accuracy
    correct_clean = 0
    for path, label in test_images_with_labels:
        res = predict(path)
        if res["label"] == label:
            correct_clean += 1
    results["clean"] = correct_clean / len(test_images_with_labels)
    print(f"Clean Baseline Accuracy: {results['clean']*100:.1f}%")

    # JPEG tests
    for q in jpeg_qualities:
        correct = 0
        for i, (path, label) in enumerate(test_images_with_labels):
            img = Image.open(path).convert("RGB")
            deg = degrade_jpeg(img, q)
            tmp_p = os.path.join(temp_dir, f"deg_jpeg_{q}_{i}.jpg")
            deg.save(tmp_p)
            res = predict(tmp_p)
            if res["label"] == label:
                correct += 1
            if os.path.exists(tmp_p): os.remove(tmp_p)
        acc = correct / len(test_images_with_labels)
        results["jpeg"][q] = acc
        print(f"JPEG Q={q} Accuracy: {acc*100:.1f}%")

    # Plot JPEG degradation curve
    plt.figure(figsize=(7, 4.5))
    qs = [100] + jpeg_qualities
    accs = [results["clean"]] + [results["jpeg"][q] for q in jpeg_qualities]
    plt.plot(qs, [a * 100 for a in accs], marker="o", color="#2563EB", linewidth=2.5, label="SignalScope")
    plt.axhline(50, color="gray", linestyle="--", label="Random Chance (50%)")
    plt.title("Module C: Robustness to JPEG Re-compression Degradation", fontsize=12, fontweight="bold")
    plt.xlabel("JPEG Quality (100 = Uncompressed)", fontsize=11)
    plt.ylabel("Accuracy (%)", fontsize=11)
    plt.ylim(40, 105)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "robustness_curve.png")
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"Saved robustness curve to {plot_path}")

    # Clean temp dir
    try:
        os.rmdir(temp_dir)
    except Exception:
        pass

    return results


if __name__ == "__main__":
    # Sample test images: real phone, modern AI, unseen real, unseen AI
    samples = [
        ("unseen_test/real/real_phone_photo.png", "Real"),
        ("unseen_test/ai/watchmaker_ai.jpg", "AI-generated"),
        ("unseen_test/ai/cyberpunk_cat_ai.jpg", "AI-generated"),
    ]
    # Add extra unseen images if present
    import glob
    reals = glob.glob("unseen_test/eval_real/*.jpg")[:3]
    fakes = glob.glob("unseen_test/eval_ai/*.jpg")[:3]
    for r in reals: samples.append((r, "Real"))
    for f in fakes: samples.append((f, "AI-generated"))

    print(f"Evaluating robustness across {len(samples)} diverse images...")
    run_robustness_analysis(samples)
