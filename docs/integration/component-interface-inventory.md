# Component Interface Inventory — Ritucast System Integration

## 1. Overview

This document provides a comprehensive inventory of all component interfaces, modules, protocols, schemas, and error boundaries across the integrated Ritucast system verified during Phase 12.

---

## 2. Ingestion & Feature Engineering Interface Inventory

| Component / Module | Source File Path | Input Contract | Output Contract | Validation Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **Pipeline Orchestrator** | [orchestrator.py](file:///Users/kazi/Projects/RITUCAST/pipelines/orchestrator.py) | CLI flags (`--dataset`, `--use-sample`, `--dry-run`) | Pipeline execution logs & Parquet feature tables | Exit status codes; QC range checks |
| **Open-Meteo Adapter** | [open_meteo.py](file:///Users/kazi/Projects/RITUCAST/pipelines/ingestion/open_meteo.py) | Coordinates (lat, lon), forecast days, model list | JSON object with hourly/daily variables | Physical range checks (`-10°C \le T \le 55°C`, $0 \le P \le 500\text{mm}$) |
| **NASA POWER Adapter** | [nasa_power.py](file:///Users/kazi/Projects/RITUCAST/pipelines/ingestion/nasa_power.py) | Lat/lon, start/end dates (YYYYMMDD) | GeoJSON-like meteorological properties | Latency and missing value checking |
| **GPM IMERG Adapter** | [gpm_imerg.py](file:///Users/kazi/Projects/RITUCAST/pipelines/ingestion/gpm_imerg.py) | Precipitation bounds, temporal range | Precipitation raster/table | Upper boundary capping ($P \ge 0$) |
| **Sentinel-1 SAR Adapter** | [sentinel1_sar.py](file:///Users/kazi/Projects/RITUCAST/pipelines/ingestion/sentinel1_sar.py) | Haor basin bounding polygons | Backscatter $\sigma_0$ (dB) & water fraction | Spatial intersection against pilot polygons |
| **Feature Transformer** | [feature_prep.py](file:///Users/kazi/Projects/RITUCAST/pipelines/processing/feature_prep.py) | Ingested raw weather/soil/radar records | Clean feature DataFrames | Schema type coercion, null threshold checks |
| **Spatial Processing** | [spatial.py](file:///Users/kazi/Projects/RITUCAST/pipelines/processing/spatial.py) | Point coordinates & administrative polygons | Upazila zonal statistics | Coordinate system sanity checks (WGS84 EPSG:4326) |
| **Temporal Processing** | [temporal.py](file:///Users/kazi/Projects/RITUCAST/pipelines/processing/temporal.py) | Multi-day observation series | Rolling 7-day and 48-hour aggregates | Strictly causal time windows (no future leakage) |

---

## 3. Agricultural Analytics Interface Inventory

| Model / Service | Source File Path | Input Contract | Output Contract | Scientific Governance |
| :--- | :--- | :--- | :--- | :--- |
| **FAO-56 Water Balance** | [penman_monteith.py](file:///Users/kazi/Projects/RITUCAST/analytics/indicators/penman_monteith.py) | Weather time series, crop $K_c$, soil TAW/RAW | Daily $ET_0$, $ET_c$, deficit $D_t$, AWD status | Penman-Monteith equation (`EQN-ET0-01`); FAO-56 dual crop coeff |
| **Soil Water Deficit** | [soil_water_deficit.py](file:///Users/kazi/Projects/RITUCAST/analytics/indicators/soil_water_deficit.py) | Daily $ET_c$, effective rain $P_{\text{eff}}$, irrigation $I_t$ | Daily soil water deficit $D_t$ | FAO-56 mass-balance water budget |
| **Haor Flood Hazard** | [haor_flood_index.py](file:///Users/kazi/Projects/RITUCAST/analytics/indicators/haor_flood_index.py) | Meghalaya rain ($f_P$), Surma stage ($f_S$), SAR inundation ($f_I$), soil sat ($f_M$) | Composite $I_{\text{flood}} \in [0, 1]$, hazard tier, alert flag | Weighted linear hazard model (`IDX-FLD-01`); early harvest threshold |
| **Advisory Engine** | [advisory_engine.py](file:///Users/kazi/Projects/RITUCAST/analytics/engine/advisory_engine.py) | Upazila ID, Crop, Stage, Indicators, Weather | Tier 4 Recommendation object, confidence score | Gating (`DEC-17`), suppression (`DEC-10`), field copy |
| **Irrigation Rule (AWD)** | [rule_irr_01.py](file:///Users/kazi/Projects/RITUCAST/analytics/rules/rule_irr_01.py) | Soil deficit $D_t$, 48h QPF rain, stage sensitivity | Postpone / light / normal irrigation action | Threshold gating with fuel/electricity savings |
| **Flood Rule (Harvest)**| [rule_fld_01.py](file:///Users/kazi/Projects/RITUCAST/analytics/rules/rule_fld_01.py) | $I_{\text{flood}} \ge 0.75$, Boro rice ripening stage | Emergency harvest directive (80% ripe) | High-urgency warning with disaster mitigation copy |

---

## 4. Backend REST API Endpoints Inventory

All endpoints operate under FastAPI ([api/main.py](file:///Users/kazi/Projects/RITUCAST/api/main.py)) mounted with prefix `/api/v1` and health/readiness endpoints at root:

| HTTP Verb | Path | Request Parameters / Body | Response Schema Class | Status Codes | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | None | `HealthResponse` | 200 | Liveness probe returning status & service uptime. |
| `GET` | `/ready` | None | `ReadinessResponse` | 200, 503 | Readiness probe verifying feature tables & model availability. |
| `GET` | `/api/v1/upazilas` | None | `UpazilaListResponse` | 200 | Returns the 4 verified pilot Upazilas (Godagari, Tanore, Tahirpur, Sunamganj Sadar). |
| `GET` | `/api/v1/upazilas/{id}` | Path: `id` (e.g. `BD-50-20-30`) | `UpazilaDetail` | 200, 404 | Returns centroid, AEZ code, primary risks, and district metadata. |
| `GET` | `/api/v1/crops` | None | `CropListResponse` | 200 | Supported pilot crops (Boro Rice, *Oryza sativa L.*). |
| `GET` | `/api/v1/crops/{crop_id}` | Path: `crop_id` (`boro_rice`) | `CropDetail` | 200, 404 | Supported phenological stages, duration, and calibration metadata. |
| `GET` | `/api/v1/seasons` | None | `SeasonListResponse` | 200 | Agricultural seasons (Rabi / Boro rice cycle). |
| `GET` | `/api/v1/upazilas/{id}/weather` | Path: `id` | `WeatherFeedResponse` | 200, 404 | Tier 1 24h observations and Tier 3 72h probabilistic forecasts. |
| `GET` | `/api/v1/upazilas/{id}/water-balance` | Path: `id`, Query: `crop`, `stage` | `WaterBalanceResponse` | 200, 404, 422 | Tier 2 FAO-56 Penman-Monteith water balance and AWD indicators. |
| `GET` | `/api/v1/upazilas/{id}/flood-hazard` | Path: `id` | `FloodHazardResponse` | 200, 404 | Tier 2 Sentinel-1 SAR & hydrological Haor flood hazard index. |
| `GET` | `/api/v1/upazilas/{id}/advisories` | Path: `id`, Query: `crop`, `stage` | `AdvisoryResponse` | 200, 404, 422 | Tier 1–4 advisory package governed by DEC-08, DEC-10, DEC-17. |
| `POST` | `/api/v1/risk/evaluate` | Body: `RiskEvaluationRequest` | `RiskEvaluationResponse` | 200, 422 | Physical hazard evaluation across drought and flash-flood domains. |
| `GET` | `/api/v1/provenance` | None | `SystemProvenanceResponse` | 200 | Model equations, data sources, citations, and DEC-06 non-goals. |

---

## 5. Frontend Client Integration Inventory

The frontend client is implemented in React 19 + TypeScript ([frontend/](file:///Users/kazi/Projects/RITUCAST/frontend/)) consuming the backend via `apiClient`:

| View Component | Source File Path | Consumed API Endpoints | Key Interactive Features |
| :--- | :--- | :--- | :--- |
| **App** | [App.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/App.tsx) | `/ready`, `/api/v1/upazilas`, `/api/v1/crops`, `/api/v1/provenance` | Context coordination, tab routing, system readiness status pill. |
| **ContextSelector** | [ContextSelector.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/ContextSelector.tsx) | None (receives state from App) | Strict contextual gating (`DEC-17`): pilot Upazila, crop, growth stage. |
| **AdvisoryHubView** | [AdvisoryHubView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/AdvisoryHubView.tsx) | `/api/v1/upazilas/{id}/advisories`, `/api/v1/risk/evaluate` | Tier 4 actionable recommendation, 3-tier evidence breakdown, suppression fallback. |
| **WeatherFeedView** | [WeatherFeedView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/WeatherFeedView.tsx) | `/api/v1/upazilas/{id}/weather` | Tier 1 24h observations and Tier 3 72h forecast probability bands. |
| **WaterBalanceView** | [WaterBalanceView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/WaterBalanceView.tsx) | `/api/v1/upazilas/{id}/water-balance` | AWD permissible status badge, $D_t$ root zone depletion progress gauge. |
| **FloodHazardView** | [FloodHazardView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/FloodHazardView.tsx) | `/api/v1/upazilas/{id}/flood-hazard` | $I_{\text{flood}}$ gauge, early harvest alert banner, AEZ-26 not-applicable guard. |
| **ProvenanceView** | [ProvenanceView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/ProvenanceView.tsx) | `/api/v1/provenance` | Transparency audit table, equation references, DEC-06 non-goal declarations. |
