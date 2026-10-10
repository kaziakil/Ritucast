# Ritucast: Backend API Endpoints Catalog

## 1. Summary of Available Endpoints

The table below catalogs all endpoints implemented and tested in Phase 10:

| Path | HTTP Method | Tags | Description |
| :--- | :--- | :--- | :--- |
| `/health` | `GET` | Service Health | Process liveness probe |
| `/ready` | `GET` | Service Health | Parquet table & analytics dependency probe |
| `/api/v1/upazilas` | `GET` | Geographic Catalog | List authorized pilot Upazilas |
| `/api/v1/upazilas/{upazila_id}` | `GET` | Geographic Catalog | Upazila boundary, centroid, and risk focus |
| `/api/v1/crops` | `GET` | Agricultural Metadata | List calibrated pilot crops and stages |
| `/api/v1/seasons` | `GET` | Agricultural Metadata | List cropping seasons (Boro, Aus, Aman) |
| `/api/v1/upazilas/{upazila_id}/weather` | `GET` | Weather | Tier 1 observations & Tier 3 forecasts |
| `/api/v1/upazilas/{upazila_id}/water-balance`| `GET` | Agronomic Indicators | Tier 2 FAO-56 $ET_0$ & Soil Deficit $D_t$ |
| `/api/v1/upazilas/{upazila_id}/flood-hazard` | `GET` | Agronomic Indicators | Tier 2 Haor Flash Flood Index $I_{\text{flood}}$ |
| `/api/v1/upazilas/{upazila_id}/advisories` | `GET` | Advisories | Gated 4-Tier agricultural decision cards |
| `/api/v1/advisories/evaluate` | `POST` | Advisories | Direct scenario evaluation with custom inputs |
| `/api/v1/risk/evaluate` | `POST` | Physical Risk | Physical hazard thresholds (`DEC-06` compliant)|
| `/api/v1/provenance` | `GET` | Provenance | Dataset freshness, formulas, non-goals |

---

## 2. Detailed Endpoint Contracts

### 2.1 Service Health Probes
- `GET /health` / `GET /api/v1/health`:
  - Returns `200 OK` with `status: "healthy"` and server timestamp.
- `GET /ready` / `GET /api/v1/ready`:
  - Audits presence of required Parquet tables (`meteorology_daily_upazila.parquet`, `forecast_hourly_pilot.parquet`, etc.).
  - Returns `200 OK` with `status: "ready"`, `data_store_ready: true`, `analytics_ready: true`.

---

### 2.2 Upazila Catalog
- `GET /api/v1/upazilas`:
  - Returns 4 pilot Upazilas:
    - Godagari (`BD-50-20-30`, AEZ 26 High Barind)
    - Tanore (`BD-50-20-90`, AEZ 26 High Barind)
    - Sunamganj Sadar (`BD-60-90-86`, AEZ 21 Haor Basin)
    - Tahirpur (`BD-60-90-89`, AEZ 21 Haor Basin)
- `GET /api/v1/upazilas/{upazila_id}`:
  - Supports canonical IDs and shorthand aliases (`BD-50-28` $\rightarrow$ Godagari, `BD-60-90` $\rightarrow$ Tahirpur).
  - Returns `404 Not Found` if Upazila is outside pilot testbeds.

---

### 2.3 Environmental Indicators
- `GET /api/v1/upazilas/{upazila_id}/weather`:
  - Returns NASA POWER / BMD observations (yesterday $T_{\max}$, $T_{\min}$, radiation, rain) and ECMWF IFS 72h forecasts.
- `GET /api/v1/upazilas/{upazila_id}/water-balance?crop=boro_rice&stage=vegetative_tillering`:
  - Evaluates FAO-56 Penman-Monteith equation (`EQN-ET0-01`), crop coefficient $K_c$, crop demand $ET_c$ (`EQN-ETC-01`), and root-zone water deficit $D_t$ (`EQN-SWD-01`).
- `GET /api/v1/upazilas/{upazila_id}/flood-hazard`:
  - Computes Haor Flash Flood Hazard Index $I_{\text{flood}}$ (`IDX-FLD-01`) for Haor Upazilas.
  - Returns `NOT_APPLICABLE` for Barind Upazilas.

---

### 2.4 Core Advisory Service
- `GET /api/v1/upazilas/{upazila_id}/advisories?crop=boro_rice&stage=tillering`:
  - Strictly requires `crop` and `stage` parameters (`DEC-17`).
  - Synthesizes Phase 9 rules (`RULE-IRR-01`, `RULE-IRR-02`, `RULE-FLD-01`, `RULE-TMP-01`, `RULE-TMP-02`).
  - Formats output with 4-Tier keys, mandatory ground verification copy, and anti-overconfidence guarantees.

---

### 2.5 Physical Risk Assessment (`DEC-06` Safe)
- `POST /api/v1/risk/evaluate`:
  - Evaluates physical threshold breach across moisture deficit, flash flood, and thermal stress.
  - Explicitly carries scientific safeguard disclaimer prohibiting financial loss or yield guarantee claims.

---

### 2.6 System Provenance & Freshness
- `GET /api/v1/provenance`:
  - Exposes metadata for `DATA-MET-01`, `DATA-FCST-01`, and `DATA-HYD-01`.
  - Lists scientific equations and operational rules.
  - Documents explicit boundary declarations and non-goals (`DEC-06`).

---

## 3. Related Documentation

- Architecture: [phase-10-backend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md)
- OpenAPI Specification: [openapi.json](file:///Users/kazi/Projects/RITUCAST/docs/backend/openapi.json)
- Integration Contract: [phase-9-integration-contract.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-9-integration-contract.md)
