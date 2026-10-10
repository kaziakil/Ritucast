# Environment Reproducibility Guide — Ritucast Operations

## 1. System Requirements

The Ritucast system is engineered to run reproducibly across standard UNIX development environments (macOS Apple Silicon M-series, Linux x86_64/arm64) and containerized runners.

### System Specifications
- **Operating System**: macOS (Darwin 24+) or Linux (Ubuntu 22.04+ LTS).
- **RAM**: Minimum 8GB (tested on Apple M1 with 16GB).
- **Disk Space**: ~2GB for Python virtualenv, Node dependencies, and sample datasets.
- **Python Runtime**: Python 3.10.x.
- **Node Runtime**: Node.js v18.x or v20.x+.

---

## 2. Clean Installation and Setup Procedure

### Step 1: Clone Repository
```bash
git clone https://github.com/organization/RITUCAST.git
cd RITUCAST
```

### Step 2: Python Environment Setup
```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r pipelines/requirements.txt
```

### Step 3: Frontend Environment Setup
```bash
cd frontend
npm install
cd ..
```

### Step 4: Generate Baseline Feature Tables
```bash
python3.10 -m pipelines.orchestrator --dataset all --use-sample
```
This command generates the four verified Parquet tables under `data/processed/` needed for backend readiness.

### Step 5: Verification Suite
```bash
python3.10 -m pytest tests/ -q
cd frontend && npm run test && npm run build && cd ..
```

---

## 3. Configuration Management

Environment variables are loaded with safe defaults:

| Variable Name | Default Value | Purpose |
| :--- | :--- | :--- |
| `RITUCAST_ENV` | `development` | Operating mode (`development`, `test`, `production`). |
| `RITUCAST_API_HOST` | `127.0.0.1` | Host interface for FastAPI Uvicorn server. |
| `RITUCAST_API_PORT` | `8000` | Port for backend service. |
| `RITUCAST_DATA_DIR` | `data/processed` | Location of Parquet feature tables. |
| `RITUCAST_SAMPLE_DIR`| `data/sample` | Location of sample fallback fixtures. |
| `VITE_API_BASE_URL` | `""` (empty string) | Frontend base URL; empty string enables Vite reverse proxy to `:8000`. |
