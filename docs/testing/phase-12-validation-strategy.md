# Phase 12: Validation Strategy — Ritucast

## 1. Strategy Objectives and Scope

The validation strategy for Phase 12 aims to establish absolute confidence in the integrity, correctness, safety, and reproducibility of Ritucast before progressing to subsequent system phases.

The validation spans five testing tiers:
1. **Pipeline Deterministic Validation**: Verifying raw ingestion $\rightarrow$ QC $\rightarrow$ Parquet table transformation.
2. **Model & Agronomic Safeguard Validation**: Verifying FAO-56 Penman-Monteith, Haor $I_{\text{flood}}$, contextual gating (`DEC-17`), and suppression rules (`DEC-10`).
3. **API Contract & Schema Validation**: Verifying all 13 REST endpoints, response codes, and error envelopes.
4. **Frontend End-to-End User Journey**: Verifying browser rendering, bilingual copy, 4-tier visual segregation (`DEC-08`), and network error handling.
5. **Live Upstream Smoke Testing**: Bounded live HTTP connectivity checks against Open-Meteo and NASA POWER with offline resilience.

---

## 2. Test Execution Matrix

| Test Suite | File Location | Tests | Verification Focus | Status |
| :--- | :--- | :--- | :--- | :--- |
| **System E2E Tests** | [test_system_e2e.py](file:///Users/kazi/Projects/RITUCAST/tests/integration/test_system_e2e.py) | 7 | Cross-stack data traversal, API responses, DEC-06/DEC-08/DEC-10/DEC-17 compliance. | **PASS (7/7)** |
| **Live Upstream Smoke** | [test_live_smoke.py](file:///Users/kazi/Projects/RITUCAST/tests/integration/test_live_smoke.py) | 2 | Real HTTP queries to Open-Meteo and NASA POWER APIs. | **PASS (2/2)** |
| **Frontend Journey E2E**| [e2e_user_journey.test.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/test/e2e_user_journey.test.tsx) | 3 | End-to-end user navigation, AWD gauge, flood card, error banner. | **PASS (3/3)** |
| **Backend Unit & API** | `tests/unit/`, `tests/api/` | 86 | Data access repository, Pydantic models, rate limiter, middleware. | **PASS (86/86)** |
| **Frontend Component Tests**| `frontend/src/test/` | 14 | Individual view components, Header, Footer, ContextSelector. | **PASS (14/14)** |
| **Total Automated Tests**| All suites | **112** | Complete system test coverage. | **100% PASS** |

---

## 3. Scientific Quality Gates

To pass Phase 12, the system had to satisfy four invariant scientific quality gates:

1. **Gate 1: Zero Uncalibrated Extrapolation**:
   - Haor flood index strictly returns `hazard_tier: 'NOT_APPLICABLE'` when queried for Barind Upazilas (`AEZ-26`), preventing invalid hazard alerts.
2. **Gate 2: Mandatory Gating Rejection**:
   - Requests without phenological stage are rejected with HTTP 422 before any recommendation logic executes.
3. **Gate 3: Suppression Assurance**:
   - Stale data ($>36\text{h}$) triggers `is_suppressed: true` with a clear explanation, directing farmers to local Sub-Assistant Agriculture Officers (SAAO).
4. **Gate 4: Non-Overconfidence Linguistic Standards**:
   - Every recommendation response includes the mandatory field verification text, with automated assertion confirming 0 banned terms.
