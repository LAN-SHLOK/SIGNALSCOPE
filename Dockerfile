# ==============================================================================
# SignalScope — Multi-Stage Fullstack Container
# Stage 1: Build React Frontend UI
# Stage 2: Serve High-Performance FastAPI + React UI (Port 8000)
# ==============================================================================

# Stage 1: Frontend Builder
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json ./
RUN npm install --no-package-lock
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Runtime Environment
FROM python:3.11-slim AS runtime

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
COPY model/ model/
COPY configs/ configs/
COPY data/ data/
COPY weights/ weights/
COPY predict.py .

# Copy compiled React frontend bundle from stage 1
COPY --from=frontend-builder /app/frontend/dist/ frontend/dist/

# Expose port 8000 (FastAPI serving React UI & REST API)
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/api/health || exit 1

# Launch FastAPI Engine (serves React app at http://localhost:8000)
ENTRYPOINT ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]

