"""
SignalScope — Command-Line Batch Prediction Utility
Scans an image or entire directory of images and exports forensic verdicts.

Usage:
    python scripts/batch_predict.py --input path/to/images --output reports/results.csv
"""
import sys
import argparse
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from app.services.analysis_service import AnalysisService


def parse_args():
    parser = argparse.ArgumentParser(description="SignalScope CLI Batch Predictor")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to image file or directory")
    parser.add_argument("--output", "-o", type=str, default="batch_results.csv", help="Path to output CSV")
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist.")
        sys.exit(1)

    image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".bmp"}
    files_to_scan = []
    if input_path.is_file():
        files_to_scan.append(input_path)
    else:
        for f in input_path.iterdir():
            if f.suffix.lower() in image_extensions:
                files_to_scan.append(f)

    if not files_to_scan:
        print(f"No valid images found in '{input_path}'.")
        sys.exit(0)

    print(f"SignalScope: Initializing analysis engine for {len(files_to_scan)} images...")
    service = AnalysisService()

    file_tuples = []
    for fp in files_to_scan:
        try:
            with open(fp, "rb") as f:
                file_tuples.append((fp.name, f.read()))
        except Exception as exc:
            print(f"Warning: Could not read {fp.name}: {exc}")

    results = service.batch_analyze(file_tuples)
    rows = [r.to_dict() for r in results]
    df = pd.DataFrame(rows)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Scan complete. Results exported to: {out_path.resolve()}")


if __name__ == "__main__":
    main()
