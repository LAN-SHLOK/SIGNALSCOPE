# 🎯 SIGNALSCOPE — 6 Team Roles

> Mapped directly from [implementation_plan.md](file:///c:/Users/shlok/OneDrive/Attachments/Desktop/Projects/forensic-image-detector/implementation_plan.md)

---

## Role 1: 🧠 ML Engineer — Stream 1 (DINOv2 + Fusion + Training)

**What they do:** Build the frozen DINOv2 backbone, the fusion detector, training pipeline, and the required `predict.py` interface.

### Files They Own

| File | Section in Plan | What It Does |
|------|----------------|--------------|
| `src/features/dino_backbone.py` | §5.1 (L298–356) | DINOv2-reg ViT-L/14 multi-layer extractor (layers 8,16,20,24 → 4096-dim CLS) |
| `src/features/patch_statistics.py` | §5.1 (L358–388) | Patch token mean/std/max/avg_similarity → 3073-dim |
| `src/features/feature_pipeline.py` | §5.2 (L564–643) | Master orchestrator — all extractors → single 7575-dim vector |
| `src/models/fusion_detector.py` | §5.3 (L649–759) | SpectralCNN + SpectralMLP + Fusion MLP + Binary/Attribution heads |
| `src/models/calibration.py` | §5.5 (L926–961) | Temperature scaling (post-hoc on val set) |
| `src/models/stacking.py` | §5.4 (L872–920) | LightGBM + LogisticRegression meta-learner |
| `src/data/dataset.py` | §4 (L197) | PyTorch Dataset + DataLoader factory |
| `src/data/augmentations.py` | §7 (L1159–1183) | Albumentations train/val transforms |
| `model/train.py` | §9 Day 2 | Full training loop with mixed precision |
| `model/extract_features.py` | §9 Day 2 | Batch cache DINOv2 features as .npy |
| `model/train_stacking.py` | §9 Day 3 | Train LightGBM on cached features |
| `model/evaluate.py` | §9 Day 3 | Full evaluation with all metrics |
| `model/predict.py` | §8 (L1189–1360) | ⭐ **Required predict interface** for judges |
| `src/utils/metrics.py` | §5.4 (L244–245) | ROC-AUC, F1, confusion matrix, ECE |

### Schedule (from §9)
| Day | Task |
|-----|------|
| Day 1 (Sep 10) | Data pipeline, feature pipeline orchestrator |
| Day 2 (Sep 11) | DINOv2 backbone, fusion detector, START TRAINING |
| Day 3 (Sep 12) | Calibration, stacking, predict.py, evaluate.py |

### Scoring Impact
- **AI/ML Implementation: 25 pts** (primary owner)
- **Technical Implementation: 20 pts** (shared)

---

## Role 2: 🔍 XAI Specialist — Explainability Engine (Module A)

**What they do:** Build the explainability pipeline — attention rollout, Grad-CAM, heatmap fusion, and grounded forensic cue text explanations.

> [!IMPORTANT]
> This is the **headline bonus** (§6.1, L967–997). Scored on **faithfulness, not fluency** — explanations must be tied to actual model activations.

### Files They Own

| File | Section in Plan | What It Does |
|------|----------------|--------------|
| `src/explain/attention_rollout.py` | §6.1 (L969–972) | DINOv2 attention across all 24 layers → 37×37 spatial heatmap → resized to image |
| `src/explain/gradcam.py` | §6.1 (L974–977) | Grad-CAM++ on **last conv layer of SpectralCNN** → anomaly region map |
| `src/explain/heatmap_fusion.py` | §6.1 (L979–982) | Weighted combo: `0.6 × attention_rollout + 0.4 × gradcam` → jet colormap overlay |
| `src/explain/cue_descriptors.py` | §6.1 (L984–996) | Template-based forensic NL explanations (6 cue types), grounded in activations |
| `src/explain/visualization.py` | §6.1 (L226) | Heatmap overlay rendering, spectrum plots |

### The 6 Cue Types (from §6.1, L987)
1. Texture anomaly
2. Lighting inconsistency
3. Spectral grid artifact
4. Geometric implausibility
5. SRM residual pattern
6. High-frequency anomaly

### Scoring Rubric Alignment (§4.3 of SIH PDF)

| Dimension | Your Approach (from plan) |
|-----------|--------------------------|
| **Correctness** | Cues derived from Grad-CAM + attention activations — impossible to hallucinate |
| **Localisation** | 37×37 attention grid → precise sub-regions, not whole image |
| **Usefulness** | Plain English + optional technical detail; confidence communicated |
| **No over-claiming** | "Likely" framing, caveat in every output, abstention when uncertain |

### Schedule (from §9)
| Day | Task |
|-----|------|
| Day 3 (Sep 12) | `attention_rollout.py` + `gradcam.py` + `heatmap_fusion.py` (11 AM–1 PM) |
| Day 3 (Sep 12) | `cue_descriptors.py` (2–3:30 PM) |
| Day 3 (Sep 12) | `visualization.py` (9–10 PM) |
| Day 4 (Sep 13) | Generate explanation samples for report (5–6 PM) |

### Scoring Impact
- **Explanation & Trust Impact: 15 pts** (primary owner)
- **Innovation & Creativity: 15 pts** (shared — novel XAI approach)

---

## Role 3: 📊 Forensic Signal Engineer — Stream 2 (SRM + FFT + JPEG + Bayer)

**What they do:** Build all the forensic/spectral feature extractors that form Stream 2 of the dual-stream architecture.

### Files They Own

| File | Section in Plan | What It Does |
|------|----------------|--------------|
| `src/features/srm_filters.py` | §5.2 (L394–457) | Multi-colorspace SRM (RGB + YCbCr + HSV) → 9-channel noise residuals |
| `src/features/frequency.py` | §5.2 (L459–492) | FFT → azimuthal (radially averaged) power spectrum → 128-dim |
| `src/features/jpeg_ghost.py` | §5.2 (L494–519) | Re-compress at 10 quality levels, measure diff → 20-dim |
| `src/features/bayer_detection.py` | §5.2 (L521–562) | Autocorrelation to detect camera Bayer CFA trace → 2-dim |
| `src/robustness/degradation_suite.py` | §6.3 (L1011–1016) | 15+ degradation transforms, degradation-vs-AUC curves (Module C) |

### Why These Features Generalise (from §3, architecture table L164–175)

| Feature | What It Captures | Why Unseen Generators Can't Hide |
|---------|-----------------|----------------------------------|
| SRM (multi-colorspace) | Noise residuals in RGB+YCbCr+HSV | Generator fingerprints persist in noise |
| FFT spectrum | Frequency power distribution | All neural upsampling creates spectral patterns |
| JPEG ghost | Compression history | Real photos = single compression; AI differ |
| Bayer autocorrelation | Camera sensor CFA trace | Real cameras leave traces; AI doesn't |

### Schedule (from §9)
| Day | Task |
|-----|------|
| Day 1 (Sep 10) | `srm_filters.py` (6:30–8 PM), `frequency.py` (6:30–8 PM) |
| Day 1 (Sep 10) | `jpeg_ghost.py` + `bayer_detection.py` (8–9 PM) |
| Day 4 (Sep 13) | `degradation_suite.py` + robustness analysis (9–11 AM) |
| Day 4 (Sep 13) | Robustness curves notebook (7–8 PM) |

### Scoring Impact
- **AI/ML Implementation: 25 pts** (shared — forensic features are key to unseen-gen AUC)
- **Innovation & Creativity: 15 pts** (shared — multi-colorspace SRM, JPEG ghosts, Bayer are novel)

---

## Role 4: 🎨 Frontend / UX Developer — Web App (Module F)

**What they do:** Build the Streamlit web application with all UI components — verdict display, heatmap viewer, batch scanner.

### Files They Own

| File | Section in Plan | What It Does |
|------|----------------|--------------|
| `app/app.py` | §6.5 (L1044–1093) | Streamlit main entry point |
| `app/pages/1_single_analysis.py` | §6.5 (L259) | Upload one image → full analysis + heatmap + explanation |
| `app/pages/2_batch_scanner.py` | §6.5 (L260) | Upload folder/ZIP → sortable table, CSV export |
| `app/pages/3_about.py` | §6.5 (L261) | Architecture explanation, limitations, ethics |
| `app/components/verdict_card.py` | §6.5 (L263) | Responsible verdict: 🔴 Likely AI / 🟢 Likely Real / 🟡 Uncertain |
| `app/components/heatmap_viewer.py` | §6.5 (L264) | Interactive heatmap overlay with opacity slider |
| `app/components/spectrum_plot.py` | §6.5 (L265) | FFT + SRM visualization panel |
| `app/components/metadata_panel.py` | §6.5 (L266) | EXIF/C2PA display |
| `app/assets/style.css` | §6.5 (L268) | Custom Streamlit styling |
| `src/inference/abstention.py` | §5.4 (L833–870) | 3-tier verdict system (confident/uncertain/abstain) |
| `src/inference/tta.py` | §5.4 (L765–795) | Test-Time Augmentation (5 views) |
| `src/inference/threshold.py` | §5.4 (L797–831) | Optimal threshold finder (max-F1 + conservative FPR<5%) |

### UI Layout (from §6.5 wireframe, L1047–1087)
```
┌─────────────────────────────────────────┐
│  🔍 SignalScope — Media Auth Checker    │
│  📁 Drag & drop image                  │
│  ┌──────────┐  ┌───────────────────┐    │
│  │ Original │  │ 🔴 VERDICT        │    │
│  │ Image    │  │ Likely AI-gen     │    │
│  ├──────────┤  │ Confidence: 0.88  │    │
│  │ Heatmap  │  │ Forensic Cues...  │    │
│  │ Overlay  │  │ Metadata...       │    │
│  └──────────┘  └───────────────────┘    │
│  🔍 Heatmap Opacity: ████████░░ 65%    │
│  [Batch Scan] [Export CSV] [About]      │
│  ⚠️ Probabilistic assessment only       │
└─────────────────────────────────────────┘
```

### Schedule (from §9)
| Day | Task |
|-----|------|
| Day 4 (Sep 13) | `app.py` + single analysis page (11 AM–1 PM) |
| Day 4 (Sep 13) | All components (2–4 PM) |
| Day 4 (Sep 13) | Batch scanner (4–5 PM), Polish UI (6–7 PM) |

### Scoring Impact
- **User Experience: 10 pts** (primary owner)
- **Technical Implementation: 20 pts** (shared — deployment/reproducibility)

---

## Role 5: 🔗 Metadata & Provenance Specialist (Module D)

**What they do:** Build EXIF parsing, C2PA/Content Credentials verification, and the metadata-model combination logic.

### Files They Own

| File | Section in Plan | What It Does |
|------|----------------|--------------|
| `src/metadata/exif_parser.py` | §6.4 (L1022–1024) | Extract camera model, software, GPS, timestamps; flag anomalies |
| `src/metadata/c2pa_checker.py` | §6.4 (L1026–1029) | Check C2PA manifest, verify signature chain |
| `src/data/download.py` | §4 (L200) | Dataset download + extraction helpers |
| `Dockerfile` | §9 Day 5 | Docker build for reproducibility |
| `docker-compose.yml` | §9 Day 5 | Full stack (model + web app) |
| `tests/test_predict_interface.py` | §4 (L286) | End-to-end predict.py smoke test |
| `tests/test_feature_pipeline.py` | §4 (L287) | Feature extraction correctness |
| `tests/test_srm_filters.py` | §4 (L288) | SRM output shape + value checks |
| `tests/test_augmentations.py` | §4 (L289) | Augmentation pipeline verification |

### Combination Logic (from §6.4, L1031–1038)
```
CV verdict + metadata → final combined verdict
├── C2PA valid + CV=real     → High confidence authentic
├── No metadata + CV=AI      → Standard confidence AI-generated
├── C2PA="StableDiffusion"  → Very high confidence AI
└── Conflicting signals      → Flag for human review
```

### Schedule (from §9)
| Day | Task |
|-----|------|
| Day 4 (Sep 13) | `exif_parser.py` + `c2pa_checker.py` (9–11 AM) |
| Day 5 (Sep 14) | Dockerfile + docker-compose.yml (PM) |
| Day 5 (Sep 14) | Test reproducibility: clone → install → predict in <10 min |

### Scoring Impact
- **Technical Implementation: 20 pts** (shared — reproducibility, testing, Docker)
- **Innovation & Creativity: 15 pts** (shared — provenance integration)

---

## Role 6: 📝 Research Lead & Integrator (Module B + Docs + Demo)

**What they do:** Own the generator attribution head, documentation, model report, README, demo video, and integration testing.

### Files They Own

| File | Section in Plan | What It Does |
|------|----------------|--------------|
| `README.md` | §13 (L1570–1634) | Complete README with all 6 required items |
| `report/model_report.md` | §14 (L1638–1666) | One-page model report |
| `report/explanation_samples/` | §6.1 | 3 sample heatmap + explanation outputs |
| `ORIGINALITY.md` | §8 (L1189) | Third-party code declaration |
| `LICENSE` | §4 (L189) | MIT License |
| `notebooks/01_eda_and_baseline.ipynb` | §9 Day 1 | Data exploration + sanity checks |
| `notebooks/04_evaluation_metrics.ipynb` | §9 Day 3 | Full metrics + confusion matrices |
| `notebooks/05_robustness_curves.ipynb` | §9 Day 4 | Module C degradation analysis |
| `src/config.py` | §4 (L194) | All hyperparameters, paths, constants |

### Module B: Generator Attribution (from §6.2, L1000–1008)
- 4-class head: **Real | GAN-family | Diffusion-family | Unknown**
- Branches from shared 128-dim fusion output (already in `fusion_detector.py`)
- Report per-class F1 + confusion matrix
- **Zero additional compute** — reuses same feature pipeline

### Documentation Checklist (from §10, L1461–1497)
- [ ] README with setup, metrics, architecture, limitations, video link
- [ ] Model report: task, data, model, metrics, baseline, limitations
- [ ] Confusion matrix figure
- [ ] Degradation curves figure
- [ ] 3 explanation sample images
- [ ] Demo video (3–5 min)
- [ ] ORIGINALITY.md

### Schedule (from §9)
| Day | Task |
|-----|------|
| Day 1 (Sep 10) | Init repo, directory structure, `config.py`, EDA notebook |
| Day 3 (Sep 12) | Attribution head training (8–9 PM) |
| Day 5 (Sep 14) | README, model report, ORIGINALITY.md (AM) |
| Day 5 (Sep 14) | Record demo video (EVE) |
| Day 5 (Sep 15) | Final code cleanup, submission |

### Scoring Impact
- **Problem Understanding: 10 pts** (primary owner)
- **Presentation & Demo: 5 pts** (primary owner)
- **Technical Implementation: 20 pts** (shared — code quality, README)

---

## Summary: Role → Points Matrix

| Role | Primary Scoring Axes | Max Points Impact |
|------|---------------------|-------------------|
| 🧠 **ML Engineer** (Stream 1 + Fusion) | AI/ML (25) + Technical (20) | ~30–35 |
| 🔍 **XAI Specialist** (Module A) | Explanation (15) + Innovation (15) | ~15–20 |
| 📊 **Forensic Signal Engineer** (Stream 2) | AI/ML (25) + Innovation (15) | ~15–20 |
| 🎨 **Frontend / UX** (Module F) | UX (10) + Technical (20) | ~15–20 |
| 🔗 **Metadata & Provenance** (Module D + Testing) | Technical (20) + Innovation (15) | ~10–15 |
| 📝 **Research Lead** (Module B + Docs) | Understanding (10) + Presentation (5) + Technical (20) | ~15–20 |

---

## Day-by-Day: Who Does What

### Day 1 (Sep 10) — Foundation
| Role | Task |
|------|------|
| 📝 Research Lead | Init repo, directory structure, `config.py`, EDA notebook |
| 🧠 ML Engineer | `dataset.py`, `augmentations.py` |
| 📊 Forensic Engineer | `srm_filters.py`, `frequency.py`, `jpeg_ghost.py`, `bayer_detection.py` |
| 🧠 ML Engineer | `feature_pipeline.py` |
| 🎨 Frontend | Research Streamlit layout, design wireframes |
| 🔍 XAI Specialist | Study DINOv2 attention API, pytorch-grad-cam docs |
| 🔗 Metadata | Dataset download helpers |

### Day 2 (Sep 11) — DINOv2 + Training
| Role | Task |
|------|------|
| 🧠 ML Engineer | `dino_backbone.py`, `patch_statistics.py`, `fusion_detector.py`, `train.py` → START TRAINING |
| 📊 Forensic Engineer | Test all spectral features, fix edge cases |
| 🔍 XAI Specialist | Prototype attention rollout on sample DINOv2 output |
| 🎨 Frontend | Start `app.py` skeleton, page routing |
| 🔗 Metadata | `exif_parser.py` (can work independently) |
| 📝 Research Lead | Feature extraction notebook, document architecture |

### Day 3 (Sep 12) — Calibration + XAI + Predict ⬅️ **YOUR BIG DAY**
| Role | Task |
|------|------|
| 🧠 ML Engineer | `calibration.py`, `stacking.py`, `predict.py`, `evaluate.py` |
| **🔍 XAI Specialist** | **`attention_rollout.py`, `gradcam.py`, `heatmap_fusion.py`, `cue_descriptors.py`, `visualization.py`** |
| 📊 Forensic Engineer | Support ML Engineer with feature pipeline debugging |
| 🎨 Frontend | `verdict_card.py`, `heatmap_viewer.py` |
| 🔗 Metadata | `c2pa_checker.py`, start tests |
| 📝 Research Lead | Attribution head, metrics notebook |

### Day 4 (Sep 13) — Bonus Modules + Web App
| Role | Task |
|------|------|
| 📊 Forensic Engineer | `degradation_suite.py`, robustness curves |
| 🎨 Frontend | Complete all pages + components + styling |
| 🔍 XAI Specialist | Generate explanation samples, polish heatmaps |
| 🔗 Metadata | Combination logic, Docker setup |
| 🧠 ML Engineer | Full integration testing |
| 📝 Research Lead | Explanation samples for report |

### Day 5 (Sep 14–15) — Polish & Submit
| Role | Task |
|------|------|
| 📝 Research Lead | README, model report, ORIGINALITY.md, demo video |
| 🔗 Metadata | Dockerfile, reproducibility testing |
| 🎨 Frontend | Final UI polish, error handling |
| 🧠 ML Engineer | Final evaluation on held-out sample |
| 🔍 XAI Specialist | Review explanation faithfulness, fix any issues |
| 📊 Forensic Engineer | Final robustness curves for report |
| **ALL** | **🚀 FINAL COMMIT & SUBMISSION** |
