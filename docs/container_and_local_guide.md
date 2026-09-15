# SignalScope: Containerization and Local Runtime Guide

This guide details instructions for launching the SignalScope system via Docker containerization and executing the local evaluation pipeline.

---

## 1. Containerized Execution (Docker Compose)

The repository provides a multi-stage `Dockerfile` and `docker-compose.yml` that build the React interface and serve it alongside the FastAPI backend.

### Prerequisites
- Docker Engine 24.0+
- Docker Compose v2+

### Quick Start
To build and start the containerized service:

```bash
docker compose up --build
```

### Verification
Once launched, the service is accessible at:
- Web Interface: `http://localhost:8000`
- API Health Endpoint: `http://localhost:8000/api/health`
- Interactive API Docs: `http://localhost:8000/docs`

### Stopping the Container
```bash
docker compose down
```

---

## 2. Native Local Runtime

For development, testing, and batch held-out dataset evaluation, execute directly via Python.

### Prerequisites
- Python 3.10 or 3.11
- Node.js 18+ (for frontend development)
- CUDA-enabled GPU (optional; automatically detected, falls back to CPU)

### Setup
```bash
# 1. Clone repository
git clone https://github.com/LAN-SHLOK/SIGNALSCOPE.git
cd SIGNALSCOPE

# 2. Create and activate virtual environment
python -m venv venv
# Linux / macOS:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Executing Predictions
```bash
# Single image prediction
python predict.py --image path/to/image.jpg

# Single image with explanation and heatmap generation
python predict.py --image path/to/image.jpg --explain --output_dir output/

# Batch directory evaluation (held-out test sets)
python predict.py --image_dir path/to/images/ --output results.csv
```
