# SignalScope — Dual-Stream AI Image Authenticity & Provenance Engine

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **SignalScope Media Authenticity Platform**  
> An industrial, dual-stream forensic image verification system combining spatial foundation models (DINOv2), sensor-level noise residuals (SRM), 2D Fourier frequency analysis (FFT), and multi-layer provenance auditing (EXIF / C2PA / JUMBF).

---

## Architecture Overview

SignalScope employs a **Dual-Stream Multi-Modal Pipeline** to detect synthetic and manipulated imagery even when subjected to severe social media compression:

```
                          ┌───────────────────────────┐
                          │   Input Image / Batch     │
                          └─────────────┬─────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
  ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
  │  Stream 1:      │          │  Stream 2:      │          │  Stream 3:      │
  │  Spatial Vision │          │  Sensor Noise   │          │  Provenance &   │
  │  (DINOv2-reg)   │          │  (SRM + 2D FFT) │          │  Metadata Audit │
  └────────┬────────┘          └────────┬────────┘          └────────┬────────┘
           │                            │                            │
           ▼                            ▼                            ▼
  Semantic Artifacts &         Pixel Residuals &            Camera Hardware &
  Saliency Attention           Spectral Peaks               C2PA JUMBF Manifests
           │                            │                            │
           └────────────────────────────┼────────────────────────────┘
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │   Forensic Decision Fusion  │
                         │   (Multi-Tier Calibration)  │
                         └──────────────┬──────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
  ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
  │  React Web App  │          │  FastAPI Server │          │  CLI Predictor  │
  │  (Brutalist UI) │          │  (Port 8000)    │          │  (predict.py)   │
  └─────────────────┘          └─────────────────┘          └─────────────────┘
```

---

## Quickstart Guide

### Option 1: Docker (Fastest & Containerized)

Run the containerized FastAPI fullstack application:

```bash
docker compose up --build
```

- **FastAPI Backend & API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **SignalScope Web UI**: [http://localhost:8000](http://localhost:8000)

---

### Option 2: Local Development (FastAPI + React)

#### 1. Backend Setup
```bash
# Create and activate Python virtual environment
python -m venv .venv
source .venv/bin/activate       # On Linux/macOS
.venv\Scripts\activate          # On Windows

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup
```bash
# In a second terminal
cd frontend
npm install
npm run dev
```
Open **`http://localhost:3000`** in your browser.

---

### Option 3: Command-Line Evaluation CLI (`predict.py`)

The evaluation script provides an immediate interface for single-image scans, grounded visual explanations, and batch audits. Execution automatically prioritizes CUDA GPU acceleration if available, falling back to CPU only when no GPU is present.

```bash
# 1. Fast single-image prediction (runs in under 2 seconds)
python predict.py --image data/samples/sample_synthetic_diffusion.png

# 2. Prediction with XAI explanation heatmaps (saves to output/)
python predict.py --image data/samples/sample_synthetic_diffusion.png --explain --output_dir output/

# 3. Batch evaluation on an entire directory (exports CSV summary)
python predict.py --image_dir path/to/held_out_folder/ --output results.csv
```

---

## Challenge Deliverables & Module Coverage (§3.2)

SignalScope implements the Mandatory Core Task and 6 Bonus Modules:

| Module | Status | Implementation Details |
| :--- | :--- | :--- |
| **Mandatory Core Task** | **Complete** | Binary real-vs-AI classification with calibrated confidence scores and fast evaluation CLI (`predict.py`). |
| **Module A: Faithful Explanation** | **Complete** | DINOv2 self-attention rollout (60%) + SRM noise Grad-CAM (40%) fused heatmaps and grounded forensic text descriptors. |
| **Module B: Generator Attribution** | **Complete** | Multi-generator identification across SD3 (Flow Matching), SDXL, SD 2.1, DALL-E 3, and Midjourney v6. |
| **Module C: Robustness to Degradation**| **Complete** | Resilient against social media compression: 100.0% accuracy across JPEG qualities Q=95 down to Q=40. |
| **Module D: Provenance & Metadata** | **Complete** | Deep optical EXIF camera hardware extraction + binary C2PA JUMBF box verification. |
| **Module F: Real-Time / Deployable** | **Complete** | React 19 brutalist SPA with theme-colored progress tracking, interactive layer viewer, and batch inspection lab. |
| **Module G: Active Defense & Analysis** | **Complete** | Comprehensive root-cause post-mortem resolving the CIFAKE $32\times32$ resolution shortcut and unnormalized FFT energy scaling. |

---

## Official Model Evaluation Metrics (§7.2 & §7.3)

Evaluated across the held-out test split, modern unseen generative engines, and genuine camera captures:

| Metric | Measured Score | Baseline (ViT-B/16) | Delta |
| :--- | :--- | :--- | :--- |
| **Overall Held-out AUC** | **0.9986** | 0.8840 | `+11.46%` |
| **Unseen-Generator AUC (Primary)** | **0.9170** | 0.7240 | **`+19.30%`** (Primary Metric) |
| **Macro-F1 Score** | **0.9818** | 0.8410 | `+14.08%` |
| **Accuracy @ 0.50 Threshold** | **98.21%** | 85.30% | `+12.91%` |
| **False Positive Rate (FPR)** | **1.64%** | 14.80% | `-13.16%` |
| **Expected Calibration Error (ECE)** | **0.0185** | 0.1420 | `-0.1235` (Calibrated) |

### Confusion Matrix
$$\begin{bmatrix} \text{TN (Authentic Real): 713} & \text{FP (False AI): 12} \\ \text{FN (Missed AI): 14} & \text{TP (Detected AI): 711} \end{bmatrix}$$

---

## Datasets Used & Citations (§4.1 & §7.2)

1. **Core Benchmark Baseline**: [CIFAKE](https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images) (CIFAR-10 authentic photography + Stable Diffusion 1.4 synthetic imagery, ~100k scale).
2. **Added Public Synthetic Dataset**: [Defactify Image Dataset (`Rajarshi-Roy-research/Defactify_Image_Dataset`)](https://huggingface.co/datasets/Rajarshi-Roy-research/Defactify_Image_Dataset) hosted on Hugging Face (MIT/Open License). Contains authentic MS-COCO images paired with multi-engine synthetic counterparts across Stable Diffusion 3, SDXL, SD 2.1, DALL-E 3, and Midjourney v6.
3. **Multi-Domain Authentic Crops**: Curated uncompressed high-resolution smartphone photography (Hemg dataset) across iPhone, Samsung Galaxy, and Google Pixel hardware.

---

## Project Structure (§7.1)

```
SIGNALSCOPE/
├── api/
│   ├── __init__.py
│   └── server.py                 # FastAPI REST API & static React server
├── app/
│   ├── schemas/contracts.py      # Pydantic contracts & 3-tier verdict models
│   └── services/analysis_service.py # Unified forensic analysis engine
├── data/
│   └── samples/                  # Curated synthetic, authentic & C2PA test samples
├── docs/
│   ├── api_reference.md          # REST API specifications
│   ├── architecture.md           # Dual-stream formulas & mathematical derivations
│   ├── container_and_local_guide.md # Docker containerization & local execution guide
│   ├── evaluation_report.md      # Detailed evaluation protocols & benchmark tables
│   └── tech_stack.md             # Complete stack specifications & hardware requirements
├── frontend/
│   ├── src/
│   │   ├── components/           # Hero, Scanner, Pipeline, Trust & FAQ
│   │   ├── types/signalscope.ts  # TypeScript data interfaces
│   │   └── App.tsx               # SPA shell with dynamic theme scrollbar
│   ├── package.json
│   └── vite.config.ts
├── model/
│   ├── weights/                  # Trained PyTorch weights (detector.pth, stacker.joblib, calibrator.pth)
│   ├── predict.py                # Official evaluation predict interface (§4.1)
│   ├── evaluate.py               # Quantitative validation suite
│   ├── train.py                  # Initial training routine
│   └── train_joint.py            # Continual joint training with Defactify
├── report/
│   ├── complete_analysis_report.md # Engineering post-mortem & evolution report
│   ├── performance_report.md     # Detailed benchmark analysis
│   ├── metrics.json              # Machine-readable evaluation metrics
│   ├── confusion_matrix.png      # High-resolution confusion matrix plot
│   ├── roc_curve.png             # Receiver Operating Characteristic plot
│   └── robustness_curve.png      # JPEG degradation-vs-accuracy curve
├── scripts/
│   ├── batch_predict.py          # Batch evaluation scanner
│   └── download_weights.py       # Weights release downloader
├── src/
│   ├── config.py                 # Central hyperparameter & path constants
│   ├── explain/                  # Attention rollout, noise Grad-CAM & cue descriptors
│   ├── features/                 # DINOv2, SRM, Orthonormal FFT, Bayer & JPEG features
│   ├── inference/                # Temperature calibration, abstention & TTA
│   ├── metadata/                 # Deep EXIF parser & C2PA JUMBF binary scanner
│   └── models/                   # SignalScopeDetector, MLP fusion & stacking
├── tests/                        # 12 automated unit tests & regression suite
├── unseen_test/                  # Independent validation samples (real phone, modern AI)
├── Dockerfile                    # Multi-stage production container
├── docker-compose.yml            # Docker orchestration
├── predict.py                    # Official top-level evaluation CLI
├── pyproject.toml
└── requirements.txt
```

---

## Running Automated Tests

Run the full pytest unit test suite:

```bash
python -m pytest
```

Run the regression and zero-catastrophic-forgetting gate:

```bash
python tests/verify_joint_model.py
```

---

## Security & Privacy Policy

- **100% Ephemeral Processing**: Uploaded images are processed strictly in volatile system memory. No media files, personal metadata, or audit logs are stored in persistent databases or cloud buckets.
- **Zero External Telemetry**: All neural network inferences, frequency transforms, and EXIF audits execute locally on-device.

---

## License

Distributed under the MIT License. See `LICENSE` for details.

## 🎥 Demo Video

[Watch the SignalScope Demo Video (Google Drive)](https://drive.google.com/file/d/1DnwGJWE2Jln-qofowCdh_x49AuLLuxmi/view?usp=sharing)


