# Ritucast: Local Development & Operations Guide

## 1. Prerequisites

- Python 3.10+
- Virtual environment or system Python
- Dependencies installed: `fastapi`, `uvicorn`, `pydantic`, `pydantic-settings`, `pandas`, `pyarrow`, `pytest`, `httpx`

---

## 2. Quickstart Instructions

### 2.1 Starting the API Server
To start the backend service locally:
```bash
python3.10 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
Or execute directly:
```bash
python3.10 api/main.py
```

### 2.2 Accessing Documentation
- Interactive Swagger UI: `http://localhost:8000/docs`
- ReDoc Interface: `http://localhost:8000/redoc`
- OpenAPI JSON Spec: `http://localhost:8000/openapi.json`

---

## 3. Verifying Health & Probes

```bash
# Check service liveness
curl http://localhost:8000/health

# Check data store and analytics readiness
curl http://localhost:8000/ready
```

Expected readiness output:
```json
{
  "status": "ready",
  "data_store_ready": true,
  "analytics_ready": true,
  "verified_datasets": [
    "meteorology_daily_upazila.parquet",
    "forecast_hourly_pilot.parquet",
    "catchment_rainfall_daily.parquet",
    "hydrology_river_stage.parquet"
  ],
  "missing_dependencies": []
}
```

---

## 4. Example API Invocations

### 4.1 Fetch Pilot Upazilas
```bash
curl http://localhost:8000/api/v1/upazilas
```

### 4.2 Query 4-Tier Advisory (Godagari - Barind)
```bash
curl "http://localhost:8000/api/v1/upazilas/BD-50-20-30/advisories?crop=boro_rice&stage=tillering"
```

### 4.3 Query Water Balance (FAO-56 ET0 & Soil Deficit)
```bash
curl "http://localhost:8000/api/v1/upazilas/BD-50-20-30/water-balance?crop=boro_rice&stage=vegetative_tillering"
```

### 4.4 Query Haor Flash Flood Hazard
```bash
curl http://localhost:8000/api/v1/upazilas/BD-60-90-89/flood-hazard
```

---

## 5. Running Automated Tests

```bash
# Run API test suite
python3.10 -m pytest tests/api/ -v

# Run complete repository test suite (Phase 8, Phase 9, Phase 10)
python3.10 -m pytest tests/ -v
```

---

## 6. Regenerating OpenAPI Specification

```bash
python3.10 -c "from api.main import export_openapi_json; export_openapi_json()"
```

---

## 7. Related Documentation

- Architecture: [phase-10-backend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md)
- API Endpoints: [api-endpoints.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/api-endpoints.md)
