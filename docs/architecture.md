# SignalScope Architecture & Technical Design

## 1. System Overview
SignalScope is an industrial dual-stream forensic pipeline that determines whether digital imagery originates from physical optical camera sensors or synthetic AI generation pipelines (Diffusion, GANs, Autoregressive models).

```
┌────────────────────────────────────────────────────────────────────────┐
│             SIGNALSCOPE REACT FRONTEND (`frontend/`)                  │
│   • Google AI Studio Brutalist Design (Vite + Tailwind v4 + Motion)   │
│   • 60 FPS Viewport-aware scroll transitions & dynamic color worlds    │
│   • Client-side split comparison slider & real-time degradation lab    │
│   • Zero emojis • Clear, human-readable forensic explanations          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP REST (multipart/form-data)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   FASTAPI REST BRIDGE (`api/server.py`)                │
│   • `POST /api/analyze`: Single-image deep forensic scan               │
│   • `POST /api/batch`: Multi-image / ZIP folder audit                  │
│   • `GET /api/health`: Health & device readiness status                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Python Service Adapter
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│          SERVICE & PROVENANCE LAYER (Roles 4 & 5)                     │
│   • `app/services/analysis_service.py`: Adapter pattern orchestration │
│   • `src/metadata/deep_exif.py`: Hardware EXIF & optical lens tags    │
│   • `src/metadata/exif_auditor.py`: AI generator signature audit       │
│   • `src/metadata/c2pa_checker.py`: C2PA Content Credentials verify    │
│   • `src/metadata/provenance_report.py`: Multi-modal score fusion      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Scientific feature inputs
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│        UPSTREAM ML BACKBONE & DETECTORS (Roles 1, 2, 3)                │
│   • DINOv2 ViT-L/14 Foundation Backbone (Self-supervised vision)       │
│   • SRM High-Pass Filter Residuals (Spatial manipulation traces)       │
│   • Radially-Averaged 2D FFT Power Spectrum (Checkerboard artifacts)  │
│   • Bayer CFA Autocorrelation (Physical silicon hardware noise)        │
└────────────────────────────────────────────────────────────────────────┘
```

## 2. Decoupled Architecture Principles
- **Dual-Interface Flexibility**:
  - Primary Production UI: React + Vite + Motion (`frontend/`)
  - Standalone Python Fallback: Streamlit (`app/streamlit_app.py`)
  - Headless / Batch CLI: Python Script (`scripts/batch_predict.py`)
- **Domain Contracts**: All layers communicate via strictly typed data models defined in `app/schemas/contracts.py` and `frontend/src/types/signalscope.ts`.
- **Zero-Leakage Security Policy**: Model weights, feature arrays, datasets, API keys, and video media are excluded via `.gitignore`.
