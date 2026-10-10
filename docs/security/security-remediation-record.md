# Security Remediation Record — Ritucast

## 1. Overview

This document provides a detailed record of the engineering fixes, code modifications, and configuration hardening applied during **Phase 15: Security, Privacy, and Responsible Agricultural Intelligence**.

---

## 2. Remediated Findings Matrix

| Finding ID | Severity | File Modified | Git Commit | Verification Method |
| :--- | :--- | :--- | :--- | :--- |
| `SEC-15-01` | Medium | [`api/middleware/security.py`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py)<br>[`api/main.py`](file:///Users/kazi/Projects/RITUCAST/api/main.py) | Pending Commit | `test_http_security_headers_present` |
| `SEC-15-02` | Medium | [`api/middleware/security.py`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py)<br>[`api/config.py`](file:///Users/kazi/Projects/RITUCAST/api/config.py) | Pending Commit | `test_payload_size_limit_returns_413` |
| `SEC-15-03` | Medium | [`api/middleware/security.py`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py)<br>[`api/main.py`](file:///Users/kazi/Projects/RITUCAST/api/main.py) | Pending Commit | `test_rate_limiting_enforcement_returns_429` |
| `SEC-15-04` | Medium | [`api/data_access/repository.py`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L192) | Pending Commit | `test_path_traversal_protection_in_repository` |
| `SEC-15-05` | Low | [`api/schemas/advisories.py`](file:///Users/kazi/Projects/RITUCAST/api/schemas/advisories.py)<br>[`api/schemas/risk.py`](file:///Users/kazi/Projects/RITUCAST/api/schemas/risk.py) | Pending Commit | Pydantic Schema Serialization & Validation |
| `SEC-15-07` | Low | [`api/data_access/repository.py`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L571) | Pending Commit | `test_suppression_safeguard_dec10_ensemble_uncertainty` |

---

## 3. Detailed Change Log by Component

### 3.1 Security Middleware Addition (`SEC-15-01`, `SEC-15-02`, `SEC-15-03`)
- **Created**: [`api/middleware/security.py`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py)
  - `SecurityHeadersMiddleware`: Injects `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`, `Referrer-Policy: strict-origin-when-cross-origin`, `Content-Security-Policy: default-src 'self'; frame-ancestors 'none';`, `Permissions-Policy: camera=(), microphone=(), geolocation=()`, and HSTS.
  - `RequestSizeLimitMiddleware`: Enforces `MAX_REQUEST_SIZE_BYTES = 1048576` (1 MB) ceiling, returning HTTP 413 `PAYLOAD_TOO_LARGE`.
  - `RateLimitMiddleware`: Enforces in-memory sliding-window request throttling (60 rpm default) per client IP address, appending `X-RateLimit-*` headers and returning HTTP 429 when breached.
- **Updated**: [`api/main.py`](file:///Users/kazi/Projects/RITUCAST/api/main.py#L52) to register all three security middlewares on application initialization.
- **Updated**: [`api/middleware/__init__.py`](file:///Users/kazi/Projects/RITUCAST/api/middleware/__init__.py) to cleanly export new middleware classes.
- **Updated**: [`api/middleware/error_handlers.py`](file:///Users/kazi/Projects/RITUCAST/api/middleware/error_handlers.py#L62) to map HTTP 413 to `PAYLOAD_TOO_LARGE`.

### 3.2 Path Traversal Hardening (`SEC-15-04`)
- **Updated**: [`api/data_access/repository.py`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L192) in `load_parquet_table(filename: str)`:
  - Added check: if filename contains `..`, `/`, or `\`, raises `ValueError("Path traversal or invalid filename rejected")`.
  - Added check: if filename does not end with `.parquet`, raises `ValueError("Unauthorized non-parquet file access")`.
  - Verified that resolved path starts with `self.processed_dir.resolve()`.

### 3.3 Schema Bounds Enforcement (`SEC-15-05`)
- **Updated**: [`api/schemas/advisories.py`](file:///Users/kazi/Projects/RITUCAST/api/schemas/advisories.py#L74) in `AdvisoryEvaluateRequest`:
  - `upazila_id`: `max_length = 50`
  - `crop_name`, `growth_stage`: `max_length = 100`
  - `data_timestamp_utc`: `max_length = 50`
  - `ensemble_spread_pct`, `rain_prob_pct`: `ge = 0.0, le = 100.0`
- **Updated**: [`api/schemas/risk.py`](file:///Users/kazi/Projects/RITUCAST/api/schemas/risk.py#L11) in `RiskEvaluationRequest`:
  - `upazila_id`: `max_length = 50`
  - `crop_id`, `growth_stage`: `max_length = 100`

### 3.4 Suppression Reason Propagation (`SEC-15-07`)
- **Updated**: [`api/data_access/repository.py`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L571):
  - Changed `tier4_rec["suppression_reason"]` from static string `"DATA_AGE_EXCEEDED"` to `primary_card.suppression_reason if is_supp else None`.

### 3.5 Frontend Security & TypeScript Compilation Hardening
- **Created**: [`frontend/src/test/security.test.tsx`](file:///Users/kazi/Projects/RITUCAST/frontend/src/test/security.test.tsx) testing absence of `dangerouslySetInnerHTML`, absence of `eval`/`innerHTML`, zero leaked API keys, and anti-deception error handling in `apiClient.ts`.
- **Updated**: [`frontend/tsconfig.app.json`](file:///Users/kazi/Projects/RITUCAST/frontend/tsconfig.app.json#L7) to include `"node"` in compiler `types`.

Related documentation:
- [`docs/security/security-findings-register.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/security-findings-register.md)
- [`docs/security/remaining-risks.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/remaining-risks.md)
- [`docs/security/security-test-plan.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/security-test-plan.md)
