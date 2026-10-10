# API and Backend Security Specification — Ritucast

## 1. Overview

This document details the security architecture, input validation standards, error sanitization policies, and resource controls implemented across the Ritucast FastAPI backend service ([`api/main.py`](file:///Users/kazi/Projects/RITUCAST/api/main.py)).

---

## 2. Input Validation & Parameter Boundaries

Ritucast operates on a strict allowlist and validated bounds model:

### 2.1 Upazila Identifier Validation
- **Requirement**: Client requests query Upazilas via canonical BBS codes (e.g., `BD-50-20-30` for Godagari, `BD-60-90-89` for Tahirpur) or recognized aliases (`BD-50-28`, `BD-60-90`).
- **Enforcement**: [`AgriculturalDataRepository.resolve_upazila_id`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L86) resolves aliases and validates membership in [`PILOT_UPAZILAS_META`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L29).
- **Behavior on Unknown Code**: Returns HTTP 404 with structured error envelope:
  ```json
  {
    "status": "error",
    "code": "RESOURCE_NOT_FOUND",
    "message": "Upazila 'BD-99-99-99' not found or outside active pilot testbeds.",
    "timestamp_utc": "2026-10-10T11:50:00Z"
  }
  ```

### 2.2 Contextual Gating Validation (`DEC-17`)
- **Requirement**: No advisory endpoint may generate advice without verified Upazila, Crop, and Phenological Stage.
- **Enforcement**: Implemented in [`api/routers/advisories.py`](file:///Users/kazi/Projects/RITUCAST/api/routers/advisories.py#L37) and [`analytics/engine/context_gate.py`](file:///Users/kazi/Projects/RITUCAST/analytics/engine/context_gate.py).
- **Behavior on Violation**: Rejects with HTTP 422 `CONTEXT_GATING_FAILED`:
  ```json
  {
    "status": "error",
    "code": "CONTEXT_GATING_FAILED",
    "message": "Fields 'crop' and 'stage' are mandatory for advisory generation (DEC-17).",
    "details": { "rule": "DEC-17", "path": "/api/v1/upazilas/BD-50-20-30/advisories" }
  }
  ```

### 2.3 Numerical Range & Payload Bounds
- Numerical input variables in POST `/api/v1/advisories/evaluate` are constrained by Pydantic:
  - `ensemble_spread_pct`: $0.0 \le x \le 100.0$
  - `rain_prob_pct`: $0.0 \le x \le 100.0$
  - `upazila_id`: `max_length = 50`
  - `crop_name`, `growth_stage`: `max_length = 100`

---

## 3. Defense-in-Depth HTTP Security Middleware

The application factory in [`api/main.py`](file:///Users/kazi/Projects/RITUCAST/api/main.py) registers three dedicated security middlewares ([`api/middleware/security.py`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py)):

### 3.1 `SecurityHeadersMiddleware`
Injects OWASP-recommended HTTP response headers into every request:
- `X-Content-Type-Options: nosniff`: Prevents browsers from MIME-sniffing responses away from the declared content-type.
- `X-Frame-Options: DENY`: Blocks clickjacking by preventing any third-party domain from embedding Ritucast inside an iframe.
- `X-XSS-Protection: 1; mode=block`: Enables browser XSS filtering defense.
- `Referrer-Policy: strict-origin-when-cross-origin`: Restricts referrer data leakage when navigating away.
- `Content-Security-Policy: default-src 'self'; frame-ancestors 'none';`: Restricts resources to trusted origins and blocks framing.
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`: Disables high-privilege browser device APIs.
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`: Enforced in production or when accessed via HTTPS.

### 3.2 `RequestSizeLimitMiddleware`
- Prevents memory exhaustion attacks and large buffer exploits.
- Checks the `Content-Length` header against `settings.MAX_REQUEST_SIZE_BYTES` (default: 1,048,576 bytes / 1 MB).
- Immediately halts oversized payloads with HTTP 413 `PAYLOAD_TOO_LARGE`.

### 3.3 `RateLimitMiddleware`
- Protects compute resources against abusive scraping and automated flooding.
- Tracks requests per client IP address using a sliding 60-second window.
- Configured via `settings.RATE_LIMIT_PER_MINUTE` (default: 60 rpm in dev, 120 rpm in production).
- Exempts container health probes (`/health`, `/ready`) to guarantee reliable platform liveness monitoring.
- Appends diagnostic headers to every response:
  - `X-RateLimit-Limit: 60`
  - `X-RateLimit-Remaining: 59`
- Returns HTTP 429 `RATE_LIMIT_EXCEEDED` with a `Retry-After` header when limit is exceeded.

---

## 4. Error Handling & Information Leakage Prevention

All exceptions are routed through centralized handlers in [`api/middleware/error_handlers.py`](file:///Users/kazi/Projects/RITUCAST/api/middleware/error_handlers.py):
1. **Uncaught Server Errors (500)**: Masked to a sanitized generic error envelope. Python stack traces and file paths are logged server-side via `logging.getLogger("ritucast.api")` but **never** serialized to the client.
2. **Uniform Error Envelope**:
   ```json
   {
     "status": "error",
     "code": "INTERNAL_SERVER_ERROR",
     "message": "An unexpected server error occurred while processing the agricultural request.",
     "timestamp_utc": "2026-10-10T11:55:00Z",
     "details": null
   }
   ```

---

## 5. Path Traversal & Filesystem Hardening

The data access layer loads pre-computed Parquet tables ([`api/data_access/repository.py`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L192)). To prevent arbitrary file read attacks:
- Any filename parameter containing `..`, `/`, or `\` immediately raises `ValueError`.
- Only files with the `.parquet` extension are permitted.
- The resolved absolute path is strictly verified to reside within `settings.PROCESSED_DIR`.

---

## 6. Verification Test Coverage

Backend security controls are tested via automated pytest fixtures in:
- [`tests/api/test_security_hardening.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_security_hardening.py)
- [`tests/api/test_error_handling_and_security.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_error_handling_and_security.py)
- [`tests/api/test_advisories_and_gating.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_advisories_and_gating.py)
