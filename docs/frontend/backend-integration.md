# Frontend Backend Integration Contract

## 1. Integration Overview

The Ritucast frontend integrates directly with the Phase 10 REST API service running FastAPI. Development mode routes all `/api`, `/health`, and `/ready` requests via Vite's built-in reverse proxy to `http://localhost:8000`. Production configurations override the base URL via the `VITE_API_BASE_URL` environment variable.

---

## 2. Integrated Endpoint Matrix

| # | Endpoint Path | Method | Backend Service | Consumed by Frontend Component |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `/health` | GET | Core Health | System Health Monitor (`apiClient.getHealth`) |
| 2 | `/ready` | GET | Core Readiness | `[Header.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/Header.tsx)` Readiness Badge |
| 3 | `/api/v1/upazilas` | GET | Geo Metadata | `[ContextSelector.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/ContextSelector.tsx)` Location Dropdown |
| 4 | `/api/v1/upazilas/{id}` | GET | Geo Metadata | Location Profile & Regional Elevation |
| 5 | `/api/v1/crops` | GET | Crop Metadata | `[ContextSelector.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/ContextSelector.tsx)` Crop Dropdown |
| 6 | `/api/v1/seasons` | GET | Season Metadata | Season Context Card |
| 7 | `/api/v1/upazilas/{id}/weather` | GET | Indicator Engine | `[WeatherFeedView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/WeatherFeedView.tsx)` Observations & 72h Forecast |
| 8 | `/api/v1/upazilas/{id}/water-balance`| GET | Indicator Engine | `[WaterBalanceView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/WaterBalanceView.tsx)` Deficit & AWD Status |
| 9 | `/api/v1/upazilas/{id}/flood-hazard` | GET | Indicator Engine | `[FloodHazardView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/FloodHazardView.tsx)` $I_{\text{flood}}$ Index |
| 10 | `/api/v1/upazilas/{id}/advisories` | GET | Advisory Engine | `[AdvisoryHubView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/AdvisoryHubView.tsx)` Tier 4 Recommendations |
| 11 | `/api/v1/risk/evaluate` | POST | Risk Engine | `[AdvisoryHubView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/AdvisoryHubView.tsx)` Physical Hazard Assessment |
| 12 | `/api/v1/provenance` | GET | Provenance Engine| `[ProvenanceView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/ProvenanceView.tsx)` Datasets & Equations |

---

## 3. Request Parameters & Query Strings

### 3.1 Water Balance Endpoint (`/api/v1/upazilas/{id}/water-balance`)
- **Path Param**: `id` (e.g., `BD-50-20-30` or `godagari`).
- **Query Params**:
  - `crop` (required): Canonical crop identifier (e.g., `boro_rice`).
  - `stage` (required): Calibrated growth stage (e.g., `Tillering`).
- **Enforcement**: If `crop` or `stage` is omitted, the API responds with `400 Bad Request` or `422 Unprocessable Entity`. The frontend validates these locally before dispatch.

### 3.2 Advisory Endpoint (`/api/v1/upazilas/{id}/advisories`)
- **Path Param**: `id` (e.g., `BD-50-20-30`).
- **Query Params**:
  - `crop` (required): `boro_rice`.
  - `stage` (required): `Tillering`.

### 3.3 Physical Risk Evaluation (`/api/v1/risk/evaluate`)
- **Method**: POST
- **Payload**:
  ```json
  {
    "upazila_id": "BD-50-20-30",
    "crop_id": "boro_rice",
    "growth_stage": "Tillering",
    "hazard_types": ["DROUGHT", "HEAT_STRESS", "COLD_STRESS", "FLASH_FLOOD"]
  }
  ```

---

## 4. Verification and Contract Alignment

1. **Envelope Format**: List endpoints return `{ status: "success", count: N, data: [...] }`. The `apiClient` unboxes `res.data` cleanly.
2. **Detail Endpoints**: Entity endpoints return `{ status: "success", data: { ... } }` or direct JSON objects.
3. **Quality & Freshness Metadata**: Every indicator and advisory payload includes a `provenance` dictionary documenting timestamp, algorithm standard, and latency hours.
