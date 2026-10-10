# Ritucast: Formal Handoff to Phase 11 (Frontend Core Architecture & UI Shell)

## 1. Executive Summary & Handoff Authority

Phase 10 (Backend API and Service Layer) has successfully concluded with all acceptance criteria verified. The backend service layer is fully operational, thoroughly tested, and documented.

The project is now ready for **Phase 11: Frontend Core Architecture & UI Shell**.

---

## 2. Verified Backend Endpoints for Phase 11 Consumption

Phase 11 frontend engineers can consume the following verified REST API endpoints at `http://localhost:8000`:

| Endpoint Path | Method | Key Query / Body Parameters | Frontend Component / Usage |
| :--- | :--- | :--- | :--- |
| `/health` | `GET` | None | Service liveness indicator |
| `/ready` | `GET` | None | Data & analytics readiness badge |
| `/api/v1/upazilas` | `GET` | None | Upazila selection dropdown & bottom sheet |
| `/api/v1/upazilas/{id}` | `GET` | Path: `upazila_id` | Zone summary card & primary hazard tag |
| `/api/v1/crops` | `GET` | None | Crop selection & phenological stage selector |
| `/api/v1/seasons` | `GET` | None | Season calendar pill badges |
| `/api/v1/upazilas/{id}/weather` | `GET` | Path: `upazila_id` | 7-day weather forecast carousel & charts |
| `/api/v1/upazilas/{id}/water-balance` | `GET` | Query: `crop`, `stage` | Root-zone soil water deficit gauge ($D_t$) |
| `/api/v1/upazilas/{id}/flood-hazard` | `GET` | Path: `upazila_id` | Haor flash flood hazard meter ($I_{\text{flood}}$) |
| `/api/v1/upazilas/{id}/advisories` | `GET` | Query: `crop`, `stage` | Primary 4-tier advisory decision cards |
| `/api/v1/risk/evaluate` | `POST` | Body: `RiskEvaluationRequest` | Multi-hazard physical risk overview |
| `/api/v1/provenance` | `GET` | None | Transparency sheet, data freshness, methodology |

Full schema contracts are documented in:
- [api-endpoints.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/api-endpoints.md)
- [openapi.json](file:///Users/kazi/Projects/RITUCAST/docs/backend/openapi.json)

---

## 3. Frontend Integration Guardrails & Instructions for Phase 11

### 3.1 Strict Adherence to Mandatory Contextual Gating (`DEC-17`)
- The UI **must not** attempt to invoke `/api/v1/upazilas/{id}/advisories` or `/api/v1/upazilas/{id}/water-balance` without user-selected `crop` and `stage`.
- Missing parameters return HTTP 422 with `code: "CONTEXT_GATING_FAILED"`. The UI shell must prompt the user to select their crop and growth stage before loading advisories.

### 3.2 Automated Suppression UI Handling (`DEC-10`)
- When `tier_4_recommendation.is_suppressed` is `true`, render the amber suppression banner and display the SAAO contact fallback text. Do not render normal action buttons.

### 3.3 Visual Separation of Information Tiers (`DEC-08`)
- The UI must render distinct visual cards or badges for:
  - **Tier 1 (Empirical Observations)**
  - **Tier 2 (Derived Agronomic Indicators)**
  - **Tier 3 (Probabilistic Forecasts)**
  - **Tier 4 (Actionable Recommendations)**

### 3.4 Client Bundle & Memory Budget (`DEC-09`)
- Initial JS/CSS bundle size: $\le 1.5\text{MB}$.
- Peak client heap memory: $\le 45\text{MB}$.
- Time to Interactive on 3G: $\le 3.5\text{s}$.

---

## 4. Phase 11 Work Authorization Notice

Phase 11 must not begin until the user reviews this report and explicitly issues the authorization prompt.
