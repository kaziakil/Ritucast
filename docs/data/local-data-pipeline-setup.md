# Phase 8: Local Data Pipeline Setup & Environment Guide

## 1. System Requirements

- **Operating System**: macOS (Apple Silicon / Intel) or Linux (Ubuntu 22.04+).
- **Python Version**: Python 3.10+ (tested on Python 3.10.x).
- **Core Dependencies**:
  - `pydantic >= 2.7.0` (Structural validation)
  - `pandas >= 2.2.0` (Tabular time-series processing)
  - `pyarrow >= 16.0.0` (Columnar Parquet serialization)
  - `shapely >= 2.0.0` (WGS84 planar geometric intersection)
  - `requests >= 2.31.0` (HTTP API adapter networking)
  - `pytest >= 8.0.0` (Automated testing framework)

---

## 2. Step-by-Step Environment Setup

### 2.1 Verify Python 3.10 Availability
```bash
python3.10 --version
# Expected: Python 3.10.x
```

### 2.2 Install Pipeline Dependencies
If working in a dedicated virtual environment:
```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r pipelines/requirements.txt
```

### 2.3 Configuration Setup
Ensure configuration files exist in `configs/datasets/`:
- `configs/datasets/pilot_zones.json`
- `configs/datasets/dataset_sources.json`
- `configs/datasets/validation_thresholds.json`

If optional authenticated providers are used (e.g., NASA Earthdata for GPM IMERG HDF5 or CDSE for Sentinel-1):
```bash
# Create local .env from example (never commit secrets to Git)
cp .env.example .env
# Edit .env with your credentials
# EARTHDATA_USERNAME=your_username
# EARTHDATA_PASSWORD=your_password
# CDSE_ACCESS_TOKEN=your_token
```

---

## 3. Verifying the Pipeline Installation

### 3.1 Run Automated Test Suite
```bash
python3.10 -m pytest tests/ -v
```
All unit, spatial, temporal, and failure tests should pass with 0 errors.

### 3.2 Execute Testbed Ingestion using Local Fixtures
```bash
python3.10 -m pipelines.orchestrator --dataset all --upazila pilot --use-sample
```

### 3.3 Inspect Generated Parquet Outputs
```bash
python3.10 -c "
import pandas as pd
df = pd.read_parquet('data/processed/meteorology_daily_upazila.parquet')
print('Meteorology rows:', len(df))
print(df.head(2))
"
```

---

## 4. Troubleshooting Common Issues

1. **`ModuleNotFoundError: No module named 'pydantic'`**:
   - Ensure you are executing with `python3.10` where packages are installed, rather than a different system Python.
2. **`NASA POWER 429 Too Many Requests`**:
   - NASA POWER enforces a 30 req/min limit per IP. Use `--use-sample` during local iterative testing, or ensure the built-in rate limiter is active.
3. **`Parquet File Not Found`**:
   - Verify that `data/processed/` directory exists and write permissions are available. The orchestrator automatically creates missing directories.
