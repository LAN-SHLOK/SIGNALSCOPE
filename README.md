# Forensic Image Tampering Detector

> AI-powered forensic image authentication system combining deep learning (DINOv2), frequency-domain analysis, and explainable AI.

## Quickstart

### Docker (Recommended)
```bash
docker compose -f docker/docker-compose.yml up
```

### Local Setup
```bash
pip install -r requirements.txt
python scripts/download_weights.py
streamlit run app/streamlit_app.py
```

### CLI
```bash
python src/model/predict.py --image path/to/image.jpg
```

## Tech Stack

| Category | Tools |
|----------|-------|
| Deep Learning | PyTorch, Torchvision, DINOv2-reg, timm |
| Signal Processing | SciPy (FFT), NumPy, OpenCV |
| Augmentation | Albumentations, Pillow |
| Classification | Custom MLP, LightGBM, Scikit-Learn |
| Explainability | pytorch-grad-cam, Matplotlib, Seaborn |
| Metadata | Pillow (ExifTags), piexif |
| Web App | Streamlit, Plotly, Pandas |
| DevOps | Docker, GitHub Releases |

## License

MIT License
