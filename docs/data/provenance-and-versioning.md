# Phase 8: Data Provenance, Lineage & Versioning Specification

## 1. Executive Summary & Traceability Principles

In an agricultural intelligence platform where incorrect advice could cause crop loss or wasted pumping diesel, data provenance is a safety-critical requirement.

Every dataset processed by Ritucast must answer four scientific audit questions:
1. **Source Origin**: What exact provider URL, satellite product version, and query bounds produced this observation?
2. **Transformations**: What specific code commit, equations, and quality thresholds processed this data?
3. **Execution Context**: When was this batch run executed, who triggered it, and what was its cryptographic SHA-256 fingerprint?
4. **Reproducibility**: Can an independent researcher re-execute the identical pipeline configuration and arrive at the exact bit-for-bit analytical table?

---

## 2. Run Manifest Schema (`manifest.json`)

Every execution of the pipeline writes a permanent, immutable JSON manifest into `data/processed/manifests/<run_id>.json`:

```json
{
  "$schema": "https://ritucast.org/schemas/v1/run-manifest.json",
  "run_id": "c1f7a0b3-49d8-4f8a-92b1-6a1d82f390e1",
  "pipeline_version": "0.8.0",
  "git_commit": "3d3cfecb9a2c",
  "execution_timestamp_utc": "2026-10-10T09:30:00Z",
  "target_domain": "Bangladesh Dual-Zone Pilot",
  "parameters": {
    "pilot_upazilas": ["BD-50-20-30", "BD-50-20-90", "BD-60-90-86", "BD-60-90-89"],
    "date_range": {
      "start_date": "2026-03-01",
      "end_date": "2026-03-31"
    },
    "enable_live_network": false,
    "mock_fixtures": true
  },
  "datasets_ingested": [
    {
      "source_id": "DATA-MET-01",
      "provider": "NASA POWER",
      "collection": "daily/point/AG",
      "endpoint": "https://power.larc.nasa.gov/api/temporal/daily/point",
      "raw_records_count": 124,
      "valid_records_count": 124,
      "rejected_records_count": 0,
      "sha256_checksum": "a8f3b2c1d9e4..."
    },
    {
      "source_id": "DATA-FCST-01",
      "provider": "Open-Meteo",
      "collection": "forecast/ecmwf_ifs025",
      "endpoint": "https://api.open-meteo.com/v1/forecast",
      "raw_records_count": 672,
      "valid_records_count": 672,
      "rejected_records_count": 0,
      "sha256_checksum": "f1d4e8a2b5c7..."
    }
  ],
  "published_artifacts": [
    {
      "file_name": "meteorology_daily_upazila.parquet",
      "file_path": "data/processed/meteorology_daily_upazila.parquet",
      "rows_count": 124,
      "columns_count": 9,
      "sha256_checksum": "b3e9d8c7a1f2..."
    }
  ],
  "quality_report_summary": {
    "total_records_checked": 796,
    "passed_count": 796,
    "rejected_count": 0,
    "warnings_count": 0,
    "status": "PASS"
  }
}
```

---

## 3. Cryptographic Hashing Protocol

1. **Source Artifact Fingerprinting**: Prior to parsing, raw response payloads written to `data/raw/` are hashed using SHA-256:
   $$\text{Hash}_{\text{raw}} = \text{SHA256}(\text{bytes}(\text{RawFile}))$$
2. **Processed Output Hashing**: Upon passing the validation and feature preparation gates, the final Parquet table is hashed:
   $$\text{Hash}_{\text{out}} = \text{SHA256}(\text{bytes}(\text{ParquetFile}))$$
3. **Ledger Integrity**: Hashes are stored both in the run manifest and directly in the database metadata table (`provenance_ledger`), enabling instantaneous detection of silent file corruption or tampering.

---

## 4. Upstream Versioning Strategy

| Dataset | Provider Versioning System | Ritucast Ingestion Handling |
| :--- | :--- | :--- |
| **NASA POWER** | Semantic API version (`v2.0`) | Explicitly locked in query URL; schema changes detected via Pydantic validator. |
| **Open-Meteo** | Model run timestamp (`init_time_utc`) | Captured per forecast; older model runs retained in raw cache for hindcasting. |
| **GPM IMERG** | Collection version (`V07B`) | Logged in manifest; pipeline disallows mixing V06 and V07 records. |
| **Sentinel-1 SAR** | Processing baseline (e.g. `IPF 003.40`) | Metadata attribute extracted from CDSE OData JSON payload. |
| **SMAP L3** | Version number (`006`) | NSIDC collection identifier recorded in provenance manifest. |
