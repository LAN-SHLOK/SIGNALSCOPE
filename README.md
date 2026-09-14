# 🔬 SignalScope: Forensic & Foundation Multi-Stream AI Media Authentication

> **Smart India Hackathon (SIH 2026) — Problem Statement 2**  
> *Telling Real From Synthetic in the Age of Generative Media*  
> **Institution:** L. J. Institute of Engineering and Technology [C-433]

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)](https://pytorch.org/)
[![Streamlit App](https://img.shields.io/badge/Web%20App-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Executive Summary

**SignalScope** is a multi-stream media authenticity detector designed to distinguish real-world camera photography from modern AI-generated media (including **Stable Diffusion 3, DALL-E 3, Midjourney v6, SDXL, and GANs**).

Unlike naive classifiers that overfit to image resolution or scene semantics, SignalScope combines:
1. **Foundation Vision Semantics** (Frozen **DINOv2 ViT-L/14** multi-layer CLS tokens and patch variance statistics)
2. **Forensic Signal Analysis** (Multi-colorspace **Spatial Rich Model (SRM)** noise residuals, **FFT** radially-averaged azimuthal power spectra, **JPEG ghost** compression histories, and **Bayer CFA** demosaicing autocorrelation)
3. **Hardware Provenance & Digital Notarization** (Camera optical **EXIF** validation + **C2PA / Content Credentials** verification)
4. **Stacked Ensemble & Calibration** (HistGradientBoosting decision trees + Temperature Scaling)
5. **Responsible 3-Tier Verdicts** (`Likely authentic`, `Likely AI-generated`, `Uncertain — human review recommended`) with grounded visual heatmap explanations.

---

## 📊 Performance & Validation Benchmark

| Metric | SignalScope Score | Baseline / Requirement | Status |
|---|---|---|---|
| **Joint Multi-Domain Val AUC** | **0.9986 (99.86%)** | $\ge 0.9500$ | 🏆 **Exceeded** |
| **Joint Multi-Domain Accuracy** | **98.21%** | $\ge 90.00\%$ | 🏆 **Exceeded** |
| **Real Smartphone Photos (12MP $4000\times3000$)** | **0.26% AI (Confident Real)** | $< 5.00\%$ | ✅ **Zero False Accusations** |
| **Unseen Modern AI (Watchmaker, Cyberpunk)** | **99.70% – 99.72% AI** | $> 95.00\%$ | ✅ **100% Detected** |
| **Held-out MS COCOAI Test Stream** | **91.7% Accuracy** | $80.1\%$ (Paper Baseline) | 🏆 **Outperformed Academic Baseline** |
| **JPEG Degradation Robustness ($Q=95 \to 40$)** | **100% Accuracy Maintained** | Stable performance | ✅ **Robust** |
| **Expected Calibration Error (ECE)** | **0.0234 (2.34%)** | $\le 0.0500$ | ✅ **Calibrated** |

---

## 🏗️ Architecture

```
                                📸 Input Image
                                ┌─────┴─────┐
                        🔵 Stream 1      🟠 Stream 2
                       "Art Critic"    "Forensic Scientist"
                      (DINOv2 ViT)    (SRM + FFT + JPEG + Bayer)
                            │                  │
                      4096 + 3073          256 + 128 + 20 + 2
                        numbers              numbers
                            │                  │
                            └──────┬───────────┘
                                   │
                             🔀 Fusion MLP (7575 → 1024 → 256 → 128)
                                   │
                     ┌─────────────┴─────────────┐
                     ▼                           ▼
            🏷️ Binary Head (128 → 1)    🏷️ Attribution Head (128 → 4)
                     │                           │
          🌡️ Temperature Calibrator          Real / GAN / Diffusion
                     │
          🌲 HistGradientBoosting Stacker
                     │
          🛡️ EXIF / C2PA Provenance Fusion
                     │
                     ▼
          ⚖️ 3-Tier Responsible Verdict
```

---

## 🚀 Quickstart Guide

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/SIGNALSCOPE.git
cd SIGNALSCOPE

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Single Image Inspection (CLI)

Run inference on any image with forensic explanation heatmaps:

```bash
python model/predict.py --image unseen_test/real/real_phone_photo.png --explain
```

**Sample Output:**
```json
{
  "image": "real_phone_photo.png",
  "label": "Real",
  "confidence": 0.0026,
  "verdict": {
    "verdict": "Likely authentic",
    "tier": "confident_real",
    "icon": "🟢",
    "action": "No significant AI artifacts detected."
  },
  "generator_family": "Real",
  "metadata": {
    "has_exif": false,
    "has_c2pa": false,
    "provenance_tier": "neutral"
  },
  "explanation": {
    "cues": [
      "Consistent natural sensor noise distribution across color channels.",
      "Expected physical optical falloff and high-frequency continuity."
    ]
  },
  "heatmap_path": "unseen_test/real/real_phone_photo_explain.png"
}
```

### 3. Batch Directory Scanning (CSV Export)

Scan an entire directory of mixed images and generate an audit report:

```bash
python model/predict.py --image_dir unseen_test/eval_real/ --output results.csv
```

### 4. Launch the Web Application (GUI)

Launch the interactive Streamlit dashboard:

```bash
streamlit run app/app.py
```
- **Single Image Analysis**: Drag & drop images, opacity slider for heatmap overlay, metadata viewer.
- **Batch Processing**: Upload ZIP / folder, interactive filterable table, CSV export.
- **Forensics & Robustness Hub**: Real-time degradation curves and spectral diagnostics.

---

## 🔍 Explainability Engine (Module A)

SignalScope provides **faithful, grounded visual explanations** instead of hallucinated text:
- **Attention Rollout:** Maps patch-level attention tokens from DINOv2 layers to highlight semantic regions under model scrutiny.
- **Grad-CAM on Noise Residuals:** Computes gradient activations on the convolutional filters of `SpectralCNN` applied to 9-channel SRM noise maps.
- **Dual Heatmap Fusion:** Blends spatial semantic attention ($60\%$) with forensic residual activations ($40\%$) to generate an overlay heatmap (`<image>_explain.png`).
- **Structured Forensic Cues:** Generates grounded textual observations identifying localized texture inconsistencies, high-frequency suppression, and demosaicing regularity.

---

## 👥 Team Roles & Responsibilities

| Role | Title | Core File Ownership |
|---|---|---|
| **Role 1** 🧠 | **ML Engineer** | `dino_backbone.py`, `fusion_detector.py`, `train_joint.py`, `predict.py` |
| **Role 2** 🔍 | **XAI Specialist** | `attention_rollout.py`, `gradcam.py`, `heatmap_fusion.py`, `cue_descriptors.py` |
| **Role 3** 📊 | **Forensic Signal Engineer** | `srm_filters.py`, `frequency.py`, `jpeg_ghost.py`, `bayer_detection.py` |
| **Role 4** 🎨 | **Frontend / UX Developer** | `app/app.py`, `abstention.py`, `tta.py`, `threshold.py` |
| **Role 5** 🔗 | **Metadata & Provenance** | `exif_parser.py`, `c2pa_checker.py`, `test_robustness.py` |
| **Role 6** 📝 | **Research Lead & Integrator** | `README.md`, `team_roles.md`, `config.py`, documentation & benchmark |

---

## 📄 License & Attribution

This project is developed for the Smart India Hackathon (SIH 2026).  
Released under the [MIT License](LICENSE).
