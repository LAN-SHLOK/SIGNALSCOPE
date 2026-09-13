# ==============================================================================
# SignalScope — Multi-Stage Production Container (Role 5)
# Serves both high-performance FastAPI REST server (port 8000) and Streamlit (port 8501)
# ==============================================================================

# Stage 1: Runtime Environment
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system runtime dependencies for OpenCV and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application modules and configs
COPY src/ src/
COPY app/ app/
COPY api/ api/
COPY configs/ configs/
COPY data/samples/ data/samples/
COPY predict.py .

# Copy pre-compiled React frontend bundle if present
COPY frontend/dist/ frontend/dist/

# Ports: 8000 (FastAPI + Fullstack UI), 8501 (Streamlit Fallback)
EXPOSE 8000 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/api/health || exit 1

# Default launch: High-Performance Fullstack FastAPI Engine
ENTRYPOINT ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
