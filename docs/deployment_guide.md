# SignalScope Deployment & Execution Guide

SignalScope can be executed in three operational modes depending on target environment.

---

### Option 1: Full-Stack Mode (React + FastAPI) [RECOMMENDED]
Runs the Brutalist React UI connected to the high-performance Python analysis engine.

1. **Start Python Backend**:
   ```bash
   uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
   ```
2. **Start React Frontend (Development)**:
   ```bash
   cd frontend
   npm run dev
   ```
   Open `http://localhost:3000` in your browser.

3. **Single-Port Production Serving**:
   ```bash
   cd frontend && npm run build && cd ..
   uvicorn api.server:app --host 0.0.0.0 --port 8000
   ```
   FastAPI automatically serves the compiled React application directly at `http://localhost:8000`.

---

### Option 2: Streamlit Mode (Rapid Python Demo)
Runs the pure Python Streamlit dashboard.
```bash
streamlit run app/streamlit_app.py
```
Open `http://localhost:8501`.

---

### Option 3: Headless CLI Mode (Batch Processing)
Run forensics on an entire directory from the terminal.
```bash
python scripts/batch_predict.py --input data/samples/ --output reports/results.csv
```
