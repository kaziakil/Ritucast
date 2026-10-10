# Data and Model Artifacts Management: Ritucast Agricultural Intelligence Platform

## 1. Overview

Ritucast relies on curated, scientifically validated datasets and feature tables to deliver localized agricultural advisories across the High Barind Tract and Haor Basin testbeds.

This document describes the provenance, packaging, verification, and runtime loading characteristics of all data and model artifacts deployed in production.

---

## 2. Inventory of Deployed Artifacts

| Artifact Name | Relative Path | Size | Format | Provenance / Source | License & Redistribution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `barind_pilot_features.parquet` | `data/processed/barind_pilot_features.parquet` | 22 KB | Apache Parquet (Snappy) | NASA POWER v2.0, BMD, Sentinel-1 SAR GRD | Open Access (Public Domain / CC BY 4.0 equivalent) |
| `haor_pilot_features.parquet` | `data/processed/haor_pilot_features.parquet` | 22 KB | Apache Parquet (Snappy) | NASA POWER, BWDB Surma River Stage, BMD | Open Access (Government Public Data / NASA open data) |
| `bangladesh_pilot_upazilas.geojson` | `data/sample/bangladesh_pilot_upazilas.geojson` | 32 KB | GeoJSON RFC 7946 | Bangladesh BBS / HDX Open GIS | ODC-BY / Humanitarian Open Data |
| `meteorology_daily_upazila.parquet` | `data/sample/meteorology_daily_upazila.parquet` | 7.8 KB | Apache Parquet (Snappy) | NASA POWER aggregated daily | Open Access |
| `forecast_hourly_pilot.parquet` | `data/sample/forecast_hourly_pilot.parquet` | 9.7 KB | Apache Parquet (Snappy) | BMD Numerical Weather Prediction model run | Open Access |
| `catchment_rainfall_daily.parquet` | `data/sample/catchment_rainfall_daily.parquet` | 6.4 KB | Apache Parquet (Snappy) | GPM IMERG / BMD | Open Access |
| `hydrology_river_stage.parquet` | `data/sample/hydrology_river_stage.parquet` | 8.1 KB | Apache Parquet (Snappy) | BWDB Hydrology Division (Station SW175) | Open Access |

**Total Deployment Size**: Approximately **108 KB** across all operational datasets and boundaries.

---

## 3. Deployment and Packaging Strategy (`DEC-52`)

Because the entire corpus of pilot datasets is $<110\text{KB}$, Ritucast uses **In-Image Bundling** rather than remote object storage (Cloud Storage buckets) or external databases:

1. **Reproducibility**: Artifacts are checked into version control with verifiable Git commit SHAs, guaranteeing that every container image build is deterministic and self-contained.
2. **Zero-Latency Ingestion**: At container startup, the FastAPI data store (`src/api/routes/data.py`) memory-maps and indexes the Parquet tables in $<15\text{ms}$.
3. **Immutability**: Read-only container file system permissions (`USER ritucast`) prevent runtime mutation, data corruption, or cache poisoning.
4. **Offline Capability**: The container operates autonomously without requiring outbound network connectivity to fetch database records or remote S3/GCS buckets.

---

## 4. Integrity and Readiness Verification

During container startup and subsequent `/ready` endpoint probes, the application validates the presence and schema of all required Parquet files:

```python
# Startup probe verification in src/api/routes/health.py
required_datasets = [
    "meteorology_daily_upazila.parquet",
    "forecast_hourly_pilot.parquet",
    "catchment_rainfall_daily.parquet",
    "hydrology_river_stage.parquet"
]
```

If any dataset file is missing, corrupt, or unreadable:
- `/health` reports `200 OK` (the process is alive).
- `/ready` reports `503 Service Unavailable` with `status: "degraded"` and details of the missing dependency (`NFR-REL-01`).
- Cloud Run orchestrator suppresses incoming traffic until the readiness probe passes.

---

## 5. Artifact Retraining & Refresh Workflow

When new satellite observations (Sentinel-1 SAR) or updated seasonal meteorological records arrive:
1. Run the Phase 7/8 reproducible data pipeline:
   ```bash
   python -m pipelines.ingest
   python -m pipelines.process_features
   ```
2. Run automated validation tests:
   ```bash
   pytest tests/test_data_validation.py
   ```
3. Commit updated Parquet files to `main`.
4. The CI/CD workflow builds new versioned container images and rolls them out without downtime.
