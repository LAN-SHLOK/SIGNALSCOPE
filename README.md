# SignalScope — Dual-Stream AI Image Authenticity & Provenance Engine

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **SIH 2026 Problem Statement 2 Deliverable**  
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

Run both the FastAPI backend and Streamlit dashboard inside an isolated multi-stage container:

```bash
docker compose up --build
```

- **FastAPI Backend & API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **FastAPI Web UI**: [http://localhost:8000](http://localhost:8000)
- **Streamlit Forensic Lab**: [http://localhost:8501](http://localhost:8501)

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

Official evaluation script supporting single image analysis, visual heatmaps, and batch processing:

```bash
# 1. Inspect a single image
python predict.py --image path/to/image.jpg

# 2. Inspect with visual XAI explanation & save overlay heatmap
python predict.py --image path/to/image.jpg --explain --output_dir output/

# 3. Batch audit an entire directory and export CSV
python predict.py --image_dir path/to/folder/ --output reports/results.csv
```

---

### Option 4: Streamlit Forensic Dashboard

```bash
streamlit run app/streamlit_app.py
```

---

## Project Structure

```
SIGNALSCOPE/
├── api/
│   ├── __init__.py
│   └── server.py                 # FastAPI REST API & static web server
├── app/
│   ├── assets/custom.css         # Brutalist styling for Streamlit
│   ├── components/               # Gauges, metadata panels, spectrum plots
│   ├── schemas/contracts.py      # Pydantic data models & verdict tiers
│   ├── services/analysis_service.py # Core forensic analysis singleton
│   └── streamlit_app.py          # Streamlit UI dashboard
├── data/
│   └── samples/                  # Curated synthetic, authentic & C2PA test samples
├── docs/
│   ├── api_reference.md          # REST API specifications
│   ├── architecture.md           # Dual-stream deep dive & formulas
│   └── deployment_guide.md       # Docker & production setup
├── frontend/
│   ├── src/
│   │   ├── components/           # Hero, Scanner, Pipeline, Trust & FAQ
│   │   ├── types/signalscope.ts  # TypeScript contracts
│   │   └── App.tsx               # Main SPA shell
│   ├── package.json
│   └── vite.config.ts
├── scripts/
│   ├── batch_predict.py          # CLI batch scanner utility
│   └── download_weights.py       # Checkpoint downloader
├── src/
│   ├── data/download.py          # SHA256-verified dataset downloader
│   ├── metadata/
│   │   ├── c2pa_checker.py       # JUMBF / C2PA binary manifest scanner
│   │   ├── deep_exif.py          # Hardware EXIF & GPS parser
│   │   ├── exif_auditor.py       # AI generator signature auditor
│   │   └── provenance_report.py  # Forensic fusion decision engine
│   └── model/
│       └── predict.py            # Backward-compatible model CLI
├── tests/                        # 12 automated unit tests
├── Dockerfile                    # Multi-stage production container
├── docker-compose.yml            # Docker Compose orchestration
├── predict.py                    # Official evaluation CLI
├── pyproject.toml
└── requirements.txt
```

---

## Running Automated Tests

Run the full pytest test suite:

```bash
python -m pytest
```

All 12 unit tests verify:
1. EXIF parser hardware extraction & GPS rational sanitization.
2. AI software generator fingerprint audits (Midjourney, DALL-E, Stable Diffusion, ComfyUI, etc.).
3. C2PA JUMBF binary box detection & manifest verification.
4. Decision fusion logic (§6.4 provenance matrix).
5. FastAPI endpoints (`/health`, `/api/analyze`, `/api/batch`).
6. CLI evaluator output contracts and heatmap generation.

---

## Security & Privacy Policy

- **100% Ephemeral Processing**: Uploaded images are processed strictly in volatile system memory. No media files, personal metadata, or audit logs are stored in persistent databases or cloud buckets.
- **Zero External Telemetry**: All neural network inferences, frequency transforms, and EXIF audits execute locally on-device.

---

## License

Distributed under the MIT License. See `LICENSE` for details.

