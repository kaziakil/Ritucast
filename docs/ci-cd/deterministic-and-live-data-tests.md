# Deterministic vs. Live Data Testing Strategy: Ritucast

## 1. Overview and Problem Statement

Ritucast synthesizes environmental data from third-party public satellite and numerical weather prediction APIs:
- NASA POWER (Solar irradiance, daily temperature, relative humidity).
- Open-Meteo / BMD (Hourly NWP rainfall and wind speed forecasts).
- ESA Copernicus Data Space Ecosystem (Sentinel-1 SAR radar backscatter).

Connecting CI test pipelines directly to external public APIs creates severe operational risks:
1. **Flaky Builds**: Network latency spikes, rate-limit throttling, or temporary cloud maintenance outages cause false-positive CI failures.
2. **Slow Pipelines**: Downloading multi-megabyte NetCDF or HDF5 satellite rasters inflates CI runtime from seconds to 15+ minutes.
3. **Non-Reproducibility**: If upstream providers update an archive or backfill observations, historical tests fail without code changes.

To resolve this, Ritucast establishes a **Strict Architectural Boundary between Deterministic Tests and Live Data Smoke Tests (`DEC-48`, `DEC-54`)**.

---

## 2. Test Suite Classification & Execution

```
                                  [ Test Corpus (95 Tests) ]
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
     [ Deterministic Tests (93 Tests) ]                 [ Live Smoke Tests (2 Tests) ]
     - Tag: pytest -m "not smoke"                       - Tag: pytest -m "smoke"
     - Fixtures: data/sample/*.parquet, *.geojson       - Fixtures: Live HTTP calls to NASA & Open-Meteo
     - Runtime: < 5 seconds                             - Runtime: ~3 seconds (subject to WAN latency)
     - Execution: Every PR & Commit                     - Execution: Daily Scheduled Cron & Manual
     - Gate: BLOCKING (100% Pass)                       - Gate: NON-BLOCKING (Telemetry Alert Only)
```

### 2.1 Deterministic Regression Suite
- **Executed via**: `pytest -m "not smoke"`
- **Characteristics**:
  - Uses verified, immutable sample fixtures stored in `data/sample/`:
    - `meteorology_daily_upazila.parquet` (7.8 KB)
    - `forecast_hourly_pilot.parquet` (9.7 KB)
    - `catchment_rainfall_daily.parquet` (6.4 KB)
    - `hydrology_river_stage.parquet` (8.1 KB)
    - `bangladesh_pilot_upazilas.geojson` (32 KB)
  - Mocks external network socket calls.
  - Verifies agronomic equation math (FAO-56 PM ET0, SWD, Haor flood index).
  - Verifies Pydantic schema validation, rate limiter token buckets, and contextual gating (`DEC-17`).

### 2.2 Live-Source Smoke Suite
- **Executed via**: `pytest -m "smoke"` (`tests/integration/test_live_smoke.py`)
- **Characteristics**:
  - Issues bounded, single-coordinate HTTP queries to Open-Meteo and NASA POWER.
  - Verifies that external providers have not introduced breaking schema changes or deprecated query parameters.
  - Catches connection timeouts and network errors gracefully using `pytest.skip` rather than crashing the runner.
  - Executed independently via `.github/workflows/live-data-smoke.yml` on a daily schedule (02:00 UTC).
