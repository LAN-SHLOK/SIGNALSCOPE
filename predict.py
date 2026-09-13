#!/usr/bin/env python3
"""
SignalScope — Predict Interface
Official Evaluation CLI required by Section 8 of the Implementation Plan.

Usage:
    # Single image
    python predict.py --image path/to/image.jpg
    
    # Single image with explanation & saved heatmap overlay
    python predict.py --image path/to/image.jpg --explain --output_dir output/
    
    # Batch processing
    python predict.py --image_dir path/to/folder/ --output results.csv
"""
import sys
import json
import argparse
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.analysis_service import AnalysisService


def parse_args():
    parser = argparse.ArgumentParser(description="SignalScope — Image Authenticity Predictor")
    parser.add_argument("--image", "-i", type=str, default=None, help="Path to a single image file")
    parser.add_argument("--image_dir", "-d", type=str, default=None, help="Directory containing images for batch audit")
    parser.add_argument("--explain", "-e", action="store_true", help="Generate forensic explanation cues and save heatmap")
    parser.add_argument("--output", "-o", type=str, default="results.csv", help="Output path for batch results CSV")
    parser.add_argument("--output_dir", type=str, default="output", help="Directory to save visual explanations/heatmaps")
    return parser.parse_args()


def predict_single(image_path: Path, explain: bool = False, output_dir: str = "output") -> dict:
    """Run full forensic inspection on a single image and return structured JSON."""
    service = AnalysisService()
    
    with open(image_path, "rb") as f:
        file_bytes = f.read()

    analysis = service.analyze_image(file_bytes, filename=image_path.name)

    # Base output structure
    output = {
        "filename": image_path.name,
        "label": analysis.verdict.label,
        "confidence": round(analysis.verdict.confidence, 4),
        "raw_confidence": round(analysis.verdict.raw_confidence, 4),
        "tier": analysis.verdict.tier.value,
        "generator_family": analysis.generator_family,
        "metadata": {
            "has_exif": analysis.metadata.has_exif,
            "camera_make": analysis.metadata.camera_make,
            "camera_model": analysis.metadata.camera_model,
            "has_c2pa": analysis.metadata.c2pa_present,
            "c2pa_status": analysis.metadata.c2pa_status,
            "trust_signal": analysis.metadata.trust_signal,
            "is_ai_software_detected": analysis.metadata.is_ai_software_detected,
        },
        "spectral": {
            "has_bayer_trace": analysis.spectral.has_bayer_trace,
            "bayer_confidence": analysis.spectral.bayer_confidence,
        },
        "latency_ms": round(analysis.processing_time_ms, 2),
    }

    if explain:
        # Save heatmap overlay to disk
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        heatmap_file = out_dir / f"{image_path.stem}_heatmap.png"

        # Decode image and generate overlay
        np_arr = np.frombuffer(file_bytes, np.uint8)
        img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if img_bgr is not None and analysis.heatmap_array is not None:
            h, w = img_bgr.shape[:2]
            hm_resized = cv2.resize(analysis.heatmap_array, (w, h))
            hm_uint8 = np.clip(hm_resized * 255, 0, 255).astype(np.uint8)
            colored_hm = cv2.applyColorMap(hm_uint8, cv2.COLORMAP_INFERNO)
            fused = cv2.addWeighted(img_bgr, 0.5, colored_hm, 0.5, 0)
            cv2.imwrite(str(heatmap_file), fused)
            output["heatmap_path"] = str(heatmap_file.resolve())
        else:
            output["heatmap_path"] = None

        output["explanation"] = {
            "verdict": f"{analysis.verdict.badge_text} — Confidence {analysis.verdict.confidence:.2f}",
            "action_recommendation": analysis.verdict.action_recommendation,
            "primary_cues": [cue.to_dict() for cue in analysis.cues],
            "caveat": "This is a responsible probabilistic forensic assessment grounded in spatial, frequency, and provenance signals.",
        }

    return output


def main():
    args = parse_args()

    if not args.image and not args.image_dir:
        print("SignalScope: Please specify either --image or --image_dir. Use --help for usage.")
        sys.exit(1)

    if args.image:
        img_path = Path(args.image)
        if not img_path.exists():
            print(f"Error: File not found: {img_path}")
            sys.exit(1)

        result = predict_single(img_path, explain=args.explain, output_dir=args.output_dir)
        print(json.dumps(result, indent=2))

    elif args.image_dir:
        from scripts.batch_predict import main as run_batch
        sys.argv = ["batch_predict.py", "--input", args.image_dir, "--output", args.output]
        run_batch()


if __name__ == "__main__":
    main()
