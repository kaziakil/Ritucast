# Phase 8: Pipeline Execution & CLI Orchestration Guide

## 1. Executive Summary & Invocation Patterns

The Ritucast data pipeline is orchestrated through a unified command-line interface (`pipelines.orchestrator`). It allows engineers and automated Celery schedulers to execute dataset ingestion, quality auditing, spatial aggregation, and feature table preparation either as a complete end-to-end batch or as modular individual steps.

---

## 2. CLI Command Syntax & Options

```bash
# General invocation syntax
python3.10 -m pipelines.orchestrator [COMMAND] [OPTIONS]
```

### Supported Commands & Arguments

| Argument | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `--dataset` | `STRING` | `all` | Specific dataset to ingest (`nasa_power`, `open_meteo`, `gpm_imerg`, `sentinel1`, `smap`, `bwdb`, `all`). |
| `--upazila` | `STRING` | `pilot` | Geographic scope: `pilot` (4 pilot testbeds), specific Upazila ID (e.g. `BD-50-20-30`), or `national` (all 495). |
| `--start-date` | `STRING` | `2026-03-01` | Start of temporal window (`YYYY-MM-DD`). |
| `--end-date` | `STRING` | `2026-03-31` | End of temporal window (`YYYY-MM-DD`). |
| `--use-sample` | `FLAG` | `false` | Execute using local synthetic sample fixtures in `data/sample/` (zero internet required). |
| `--dry-run` | `FLAG` | `false` | Validate query parameters and schema without writing output files. |
| `--output-dir` | `PATH` | `data/processed` | Target publication directory for Parquet feature tables. |
| `--log-level` | `STRING` | `INFO` | Console log verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |

---

## 3. Practical Execution Examples

### 3.1 Local Offline Execution Using Fixtures (Routine Development)
```bash
python3.10 -m pipelines.orchestrator \
  --dataset all \
  --upazila pilot \
  --use-sample \
  --output-dir data/processed
```
- **Expected Outcome**: Reads sample fixtures, validates schemas, aggregates spatial centroids, computes daily rolling metrics, emits Parquet tables, and publishes `manifest.json`. Execution time $<2.0\text{ seconds}$.

### 3.2 Ingesting NASA POWER Agrometeorology for Godagari
```bash
python3.10 -m pipelines.orchestrator \
  --dataset nasa_power \
  --upazila BD-50-20-30 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15
```
- **Expected Outcome**: Queries NASA POWER REST API at $(88.33^\circ\text{E}, 24.47^\circ\text{N})$, validates temperature and solar radiation bounds, resamples to daily, and outputs `meteorology_daily_upazila.parquet`.

### 3.3 Running Dry-Run Schema & Quality Audit
```bash
python3.10 -m pipelines.orchestrator \
  --dataset open_meteo \
  --upazila BD-60-90-86 \
  --dry-run \
  --use-sample
```
- **Expected Outcome**: Executes Pydantic and semantic validators; logs quality report metrics to console without writing to disk.

---

## 4. Exit Codes & Error Diagnostics

| Exit Code | Status | Meaning & Recommended Action |
| :---: | :--- | :--- |
| `0` | **SUCCESS** | All requested datasets ingested, validated, and published with manifest. |
| `1` | **VALIDATION_ERROR** | Input schema invalid, corrupted response, or physical bound violation. Inspect `quality_report.json`. |
| `2` | **NETWORK_ERROR** | Upstream provider connection timeout or HTTP 5xx error after 3 retries. Check connectivity or upstream status. |
| `3` | **CONFIGURATION_ERROR**| Missing configuration parameter, invalid date range (start > end), or unknown Upazila ID. |
| `4` | **PARTIAL_SUCCESS** | Some non-critical datasets ingested, but one or more optional feeds timed out. Provenance manifest flagged. |
