# Error Handling and Recovery — Ritucast Operations

## 1. Principles of Agronomic Safety in Failure Handling

Agricultural decision-support platforms face unique safety considerations: **an uncaught software error or silently hallucinated number can cause a farmer to withhold life-saving irrigation or prematurely harvest an immature crop**.

Ritucast follows five core principles:
1. **Never substitute unrelated data silently**.
2. **Never turn errors or NaNs into zero unless physically justified**.
3. **Never generate uncontextualized recommendations** (`DEC-17`).
4. **Always suppress stale or uncertain outputs** (`DEC-10`).
5. **Always sanitize public error envelopes to prevent stack trace leakage**.

---

## 2. Failure Scenarios and System Recovery Matrix

| Failure Mode | Detection Point | System Behavior | User Experience | Recovery Procedure |
| :--- | :--- | :--- | :--- | :--- |
| **Missing Gating Context** | FastAPI Request Validation (`api/routes/advisories.py`) | Returns HTTP 422 with code `REQUEST_VALIDATION_ERROR`. | Frontend highlights missing stage or crop in Bengali dropdown. | User selects active growth stage; client retries request. |
| **Invalid Upazila ID** | Data Access Repository (`api/data_access/repository.py`) | Returns HTTP 404 with code `RESOURCE_NOT_FOUND`. | Safe banner stating location is outside pilot testbeds. | Client defaults to Godagari (`BD-50-20-30`). |
| **Upstream API Outage** | Ingestion Adapter / Pipeline | Retries 3 times with exponential backoff; logs error; skips upstream pull. | System uses cached Parquet records or sample fallback. | Pipeline runner alerts admin; fallback provenance displayed. |
| **Stale Weather Data (>36h)** | Advisory Safety Filter (`models/recommendation.py`) | `is_suppressed = true`; suppression reason injected (`DEC-10`). | Advisory card replaced by amber suppression notice with SAAO contact recommendation. | Automatic resumption when newer forecast is ingested. |
| **Ensemble Spread >50% (40-60% rain)** | Multi-model Spread Checker | Advisory suppressed; probabilistic uncertainty flag raised. | Farmer advised to monitor soil directly and check with extension officer. | Next NWP cycle with tighter ensemble spread clears suppression. |
| **Backend Service Unavailable** | Client Fetch Failure (`apiClient.ts`) | Caught by `Promise.allSettled`; error banner rendered. | Red error box: *"সার্ভার থেকে তথ্য পাওয়া যায়নি। অনুগ্রহ করে ব্যাকএন্ড সংযোগ পরীক্ষা করুন।"* | Retry button; automatic reload on reconnect. |

---

## 3. Client Resilience Verification

The frontend client integrates `Promise.allSettled` across all simultaneous endpoint requests. If an ancillary endpoint (such as Weather Feed or Flood Hazard) fails or returns 404, the primary Advisory Hub continues rendering safely without cascading UI crashes.
