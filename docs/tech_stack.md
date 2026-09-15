# SignalScope: Technical Stack Specifications

This document outlines the software libraries, foundational models, hardware optimization techniques, and architectural dependencies powering the SignalScope media forensics system.

---

## 1. Machine Learning and Vision Backbones

### Deep Foundation Models
- **Backbone**: DINOv2 ViT-L/14 with Register Tokens (`dinov2_vitl14_reg`)
  - Provider: Meta AI Research via PyTorch Hub (`torch.hub.load('facebookresearch/dinov2', ...)`)
  - Parameters: 304 Million
  - Embedding Dimensions: 1,024
  - Multi-Layer Feature Extraction: Intermediate Transformer Blocks 8, 16, 20, and 24 (4,096 dimensions)
  - Patch-Level Token Spatial Statistics: $37 \times 37$ grid yielding spatial mean, variance, maxima, and sampled pairwise cosine similarities (3,073 dimensions)

### Physical and Mathematical Signal Processing
- **Spatial Rich Models (SRM)**:
  - 30 high-pass filter kernels across RGB, YCrCb, and HSV color representations (9 channels)
  - Spatial manipulation and micro-texture anomaly extraction
- **Fourier Frequency Analysis (2D FFT)**:
  - Orthonormal 2D Fast Fourier Transform ($norm=\text{"ortho"}$) implemented via NumPy and SciPy
  - Azimuthal / radially-averaged power spectral energy distribution (128 bins)
- **Bayer Color Filter Array (CFA) Autocorrelation**:
  - Demosaicing residual periodicity detection ($2 \times 2$ pixel lattice)
- **JPEG Compression Error Modeling**:
  - Differential ghost re-compression across quality factors $Q \in [50, 95]$ (20 bins)

### Classification and Decision Fusion
- **Multi-Task Neural Classifier**:
  - Deep PyTorch Multi-Layer Perceptron (7,575 $\to$ 1,024 $\to$ 512 $\to$ 256 $\to$ 1) with Layer Normalization, LeakyReLU, and Dropout (0.3)
- **Gradient Boosted Tree Ensemble**:
  - `HistGradientBoostingClassifier` with L2 regularization ($L_2 = 3.0$) and Logistic Regression meta-learner
- **Confidence Calibration**:
  - Temperature Scaling ($T = 1.4444$) fitted via L-BFGS to optimize negative log-likelihood (NLL) and minimize Expected Calibration Error (ECE)

---

## 2. Provenance and Metadata Auditing

- **Deep EXIF Parser**:
  - Native Python `PIL.ExifTags` and binary tag parsing
  - Optical verification: Lens Model, Focal Length, Exposure Time, F-Number, ISO, Software signatures
- **C2PA Content Credentials**:
  - ISO/IEC 19566-5 JUMBF (JPEG Universal Metadata Box Format) binary parser
  - Identification of digital signatures, assertions, and cryptographic provenance manifests

---

## 3. Backend and API Services

- **Web Framework**: FastAPI 0.115+
- **ASGI Server**: Uvicorn with standard asynchronous event loop
- **Serialization and Validation**: Pydantic v2
- **Image Processing**: OpenCV (`opencv-python-headless`), Pillow, NumPy, SciPy
- **Tabular Modeling**: Scikit-Learn 1.4+, LightGBM 4.3+

---

## 4. Frontend User Interface

- **Framework**: React 19 with TypeScript 5.6
- **Styling Architecture**: Tailwind CSS v4 (Editorial Brutalist design language)
- **Physics and Motion**: Motion (Framer Motion v12)
- **Iconography**: Lucide React
- **Build Tool**: Vite 6 (ESM bundler)

---

## 5. Hardware Acceleration and Optimization

- **GPU Acceleration**:
  - CUDA 12.x support via PyTorch 2.6
  - Scaled Dot-Product Attention (SDPA) with FlashAttention / memory-efficient attention kernels
  - Automatic hardware detection: prioritized execution on CUDA devices, with automatic fallback to CPU when no GPU is detected
- **Batch Optimization**:
  - Dynamic explainability toggling: visual XAI heatmap overlays are bypassed during batch processing, reducing inference time by over 50% on large datasets
- **Containerization**:
  - Multi-stage Docker build combining Node.js frontend asset compilation with a slim Python runtime base (`python:3.10-slim`)
