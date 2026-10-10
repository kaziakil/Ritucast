# Ritucast: Backend API & Service Layer Architecture (Phase 10)

## 1. Executive Summary & Architectural Mission

The **Ritucast Backend API and Service Layer** bridges the processed agricultural data tables ([Phase 8](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-08/validation-report.md)) and physical recommendation engine ([Phase 9](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-09/validation-report.md)) to external consumers, client PWAs, and agricultural extension tools.

The architecture strictly adheres to:
1. **Four-Tier Information Taxonomy (`DEC-08`)**: Rigorous payload separation between empirical observations (Tier 1), derived physical indicators (Tier 2), probabilistic forecasts (Tier 3), and actionable recommendations (Tier 4).
2. **Mandatory Contextual Gating (`DEC-17`)**: Absolute rejection of advisory generation unless Administrative Upazila, Crop, and Phenological Stage are verified.
3. **Automated Suppression Policy (`DEC-10`)**: Automatic suppression when forecast latency $>36\text{ hours}$ or NWP ensemble spread exceeds $50\%$ with rain probability between $40\%\text{--}60\%$.
4. **Zero Uncalibrated Prediction (`DEC-06`)**: Complete exclusion of parcel-level yield predictions or automated pesticide prescriptions.
5. **Client Payload Budget (`DEC-09`)**: All API responses are minified, compressed, and sized under $15\text{KB}$ uncompressed for 3G cellular network constraints.

---

## 2. System Component Topology

```mermaid
graph TD
    Client[Client PWA / Extension Dashboard] -->|HTTP / JSON| FastAPI[FastAPI Application Layer api/main.py]

    subgraph Service_Boundaries[Ritucast Service Layer]
        FastAPI --> CORS[CORS Middleware]
        FastAPI --> ErrH[Error Handlers api/middleware/error_handlers.py]
        FastAPI --> Routers[Modular Routers api/routers/]

        Routers --> R_Health[health.py: /health, /ready]
        Routers --> R_Geo[geo.py: /api/v1/upazilas]
        Routers --> R_Meta[metadata.py: /api/v1/crops, /api/v1/seasons]
        Routers --> R_Weather[weather.py: /api/v1/upazilas/{id}/weather]
        Routers --> R_Water[water_balance.py: /api/v1/upazilas/{id}/water-balance]
        Routers --> R_Flood[flood_hazard.py: /api/v1/upazilas/{id}/flood-hazard]
        Routers --> R_Adv[advisories.py: /api/v1/upazilas/{id}/advisories]
        Routers --> R_Risk[risk.py: /api/v1/risk/evaluate]
        Routers --> R_Prov[provenance.py: /api/v1/provenance]
    end

    subgraph Data_and_Analytics_Integration[Data Access & Analytics Layer]
        Routers --> Repo[AgriculturalDataRepository api/data_access/repository.py]
        Repo --> Cache[(In-Memory Cache)]
        Repo --> ParquetFiles[(Parquet Tables data/processed/)]
        Repo --> P9_Engine[AgriculturalRecommendationEngine analytics/engine/]
        Repo --> P9_ET0[PenmanMonteithCalculator analytics/indicators/]
        Repo --> P9_Etc[CropWaterDemandCalculator analytics/indicators/]
        Repo --> P9_SWD[SoilWaterDeficitCalculator analytics/indicators/]
        Repo --> P9_FLD[HaorFloodIndexCalculator analytics/indicators/]
    end
```

---

## 3. Layer Separation & Responsibilities

### 3.1 Routing & Presentation Layer (`api/routers/`)
- Handles HTTP routing, path and query parameter parsing, and response serialization.
- Declares clear OpenAPI tags, operation summaries, and response models.
- Never performs raw mathematical computations or physical equation evaluations inside route handlers.

### 3.2 Error Handling & Validation Layer (`api/middleware/error_handlers.py`)
- Standardizes all API error responses into an immutable envelope:
  ```json
  {
    "status": "error",
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "timestamp_utc": "2026-10-10T14:30:00Z",
    "details": null
  }
  ```
- Translates `ContextGatingError` into HTTP 422 with `code: "CONTEXT_GATING_FAILED"`.
- Translates `RequestValidationError` into HTTP 422 with `code: "REQUEST_VALIDATION_ERROR"`.
- Translates `StarletteHTTPException` (e.g. 404, 400) into standardized error payloads without leaking raw internal traces.

### 3.3 Data Access & Repository Layer (`api/data_access/repository.py`)
- Provides singleton data access via [dependencies.py](file:///Users/kazi/Projects/RITUCAST/api/dependencies.py).
- Resolves Upazila shorthand aliases (e.g. `BD-50-28` $\rightarrow$ canonical `BD-50-20-30`, `BD-60-90` $\rightarrow$ canonical `BD-60-90-89`).
- Caches loaded Parquet files in memory to eliminate repeated disk I/O per HTTP request.
- Performs audit checks on data store readiness for `/ready` probes.

### 3.4 Analytics Integration Adapter
- Connects the service layer to Phase 9 classes:
  - `PenmanMonteithCalculator` for FAO-56 Reference ET0 (`EQN-ET0-01`).
  - `CropWaterDemandCalculator` for stage-specific Kc and ETc (`EQN-ETC-01`).
  - `SoilWaterDeficitCalculator` for root-zone daily water balance Dt (`EQN-SWD-01`).
  - `HaorFloodIndexCalculator` for composite flash flood index $I_{\text{flood}}$ (`IDX-FLD-01`).
  - `AgriculturalRecommendationEngine` for multi-rule advisory synthesis and automated suppression (`DEC-10`).

---

## 4. Key Architectural Decisions

- **`DEC-40`**: Adoption of FastAPI and Pydantic v2 as the primary REST service framework for asynchronous readiness, automated OpenAPI 3.0 schema generation, and high-performance validation.
- **`DEC-41`**: In-memory caching within `AgriculturalDataRepository` for Parquet tables and boundary GeoJSON, bounding heap usage below $45\text{MB}$ while achieving sub-$20\text{ms}$ query latency.
- **`DEC-42`**: Centralized HTTP exception translation ensuring 100% adherence to standard error envelope schemas across all status codes (400, 404, 422, 500).
- **`DEC-43`**: Explicit Upazila canonicalization mapping shorthand administrative IDs to official BBS/BND codes while maintaining backwards compatibility for field extension apps.

---

## 5. Traceability and Reference Links

- Core Roadmap: [roadmap.md](file:///Users/kazi/Projects/RITUCAST/docs/planning/roadmap.md)
- Phase 9 Completion Report: [validation-report.md](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-09/validation-report.md)
- API Specification: [api-specification.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/api-specification.md)
- Endpoints Documentation: [api-endpoints.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/api-endpoints.md)
