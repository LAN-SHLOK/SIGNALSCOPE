# SignalScope Deployment & Production Guide

SignalScope is engineered to support both local development and zero-cost, production-grade cloud deployment without requiring paid Docker subscriptions.

---

## 1. Recommended Free Cloud Deployment (Vercel + Render.com)

This architecture gives you a **100% free tier**, zero credit card requirement, enterprise-grade edge caching, and automated Git CI/CD deployments.

```
┌────────────────────────────────┐         ┌────────────────────────────────┐
│      Frontend on VERCEL        │         │      Backend on RENDER         │
│  - React 19 / Vite SPA         │ ──────> │  - FastAPI Python 3.10 Engine  │
│  - Edge Global CDN (0ms cold)  │  HTTPS  │  - Native Web Service (Free)   │
│  - Custom domain + SSL free    │         │  - Volatile In-Memory Audits   │
└────────────────────────────────┘         └────────────────────────────────┘
```

### Step 1: Deploy Backend to Render.com (Free Native Python Web Service)
Render provides free web services for Python with zero Docker setup required:

1. Sign up / Log in to [Render.com](https://render.com/) (No credit card needed).
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository (`LAN-SHLOK/SIGNALSCOPE`).
4. Configure service settings:
   - **Name**: `signalscope-backend`
   - **Language**: `Python`
   - **Branch**: `main`
   - **Region**: Closest to your users (e.g., Oregon or Frankfurt)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.server:app --host 0.0.0.0 --port $PORT`
   - **Plan Type**: `Free`
5. Click **Create Web Service**. Render will build and deploy the backend.
6. Copy your generated service URL (e.g., `https://signalscope-backend.onrender.com`).

---

### Step 2: Deploy Frontend to Vercel (Free React Edge Hosting)
Vercel hosts React/Vite frontends with global edge CDN distribution and instant deployments:

1. Sign up / Log in to [Vercel](https://vercel.com/) with GitHub.
2. Click **Add New...** -> **Project**.
3. Import the `LAN-SHLOK/SIGNALSCOPE` repository.
4. Configure the project:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click *Edit* and select `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Under **Environment Variables**, add:
   - `VITE_API_URL` = `https://signalscope-backend.onrender.com` (your Render URL from Step 1)
6. Click **Deploy**. Vercel will build the frontend and provide an HTTPS production URL (e.g., `https://signalscope.vercel.app`).

---

## 2. Single-Service Unified Deployment on Render (Alternative)

If you prefer hosting both frontend and backend under a single unified URL on Render:

1. In Render, select **Web Service** -> Python.
2. **Build Command**:
   ```bash
   cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt
   ```
3. **Start Command**:
   ```bash
   uvicorn api.server:app --host 0.0.0.0 --port $PORT
   ```
FastAPI automatically serves the compiled React application from `frontend/dist/` directly at `/` and the REST API at `/api/*`.

---

## 3. Local Development Mode

### 1. Start Python Backend:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start React Frontend:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 4. Headless CLI Evaluation Mode (`predict.py`)

Run forensic evaluations on images directly from the command line:

```bash
# Single image evaluation
python predict.py --image data/samples/authentic/sample1.jpg

# Single image with XAI heatmap visualization
python predict.py --image data/samples/synthetic/sample2.jpg --explain --output_dir output/

# Batch directory audit with CSV export
python predict.py --image_dir data/samples/ --output reports/results.csv
```


