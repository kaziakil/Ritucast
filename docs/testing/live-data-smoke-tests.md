# Live-Source Smoke Tests — Ritucast System Validation

## 1. Purpose and Protocol

Live-source smoke tests verify end-to-end network connectivity, API authentication, and schema stability against upstream public data providers without requiring full pipeline batch downloads.

These tests are isolated in [tests/integration/test_live_smoke.py](file:///Users/kazi/Projects/RITUCAST/tests/integration/test_live_smoke.py).

---

## 2. Tested Upstream Data Services

### 2.1 Open-Meteo Operational Forecast API (`DATA-FCST-01`)
- **Endpoint**: `https://api.open-meteo.com/v1/forecast`
- **Query Scope**: Bounded 1-day query for Godagari pilot coordinates ($24.4667^\circ\text{N}, 88.3167^\circ\text{E}$).
- **Tested Models**: ECMWF IFS 0.25deg (`ecmwf_ifs025`).
- **Verified Fields**: `temperature_2m`, `precipitation_probability`, `precipitation`.
- **Execution Result**: **PASS (HTTP 200 returned valid payload within 0.8s)**.

### 2.2 NASA POWER Agroclimatology API (`DATA-MET-01`)
- **Endpoint**: `https://power.larc.nasa.gov/api/temporal/daily/point`
- **Query Scope**: Point query for Godagari pilot coordinates for 2-day historical slice (`20240101` to `20240102`).
- **Tested Parameters**: `T2M`, `ALLSKY_SFC_SW_DWN`, `PRECTOTCORR`.
- **Execution Result**: **PASS (HTTP 200 returned valid properties within 1.4s)**.

---

## 3. Resilience and Offline CI Protocol

Per `DEC-10` and testing standards:
- If network access is firewalled or unavailable, the live smoke tests catch `requests.exceptions.RequestException` and trigger `pytest.skip` rather than failing the build.
- This ensures offline deterministic CI pipelines remain green while enabling manual and scheduled online smoke validations.
