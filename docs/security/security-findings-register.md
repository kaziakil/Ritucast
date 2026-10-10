# Security Findings Register — Ritucast

## 1. Register Overview

This register formally logs all security, privacy, and agronomic safety findings identified, analyzed, remediated, or tracked during **Phase 15: Security, Privacy, and Responsible Agricultural Intelligence**.

---

## 2. Findings Log

### Finding `SEC-15-01`: Missing OWASP Defensive HTTP Headers
- **Affected Component**: FastAPI Backend Service ([`api/main.py`](file:///Users/kazi/Projects/RITUCAST/api/main.py))
- **Description**: While NGINX was configured with security headers in Phase 13, the FastAPI application itself lacked native defensive security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, `Permissions-Policy`, and HSTS). If the API container were deployed directly to Cloud Run or accessed via alternative gateways, responses lacked baseline protection against MIME sniffing, clickjacking, and unauthorized framing.
- **Severity**: **Medium** (CVSS: 5.3)
- **Remediation**: Implemented [`SecurityHeadersMiddleware`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py) and registered it in [`api/main.py`](file:///Users/kazi/Projects/RITUCAST/api/main.py#L56).
- **Verification**: Verified via automated test `test_http_security_headers_present` in [`tests/api/test_security_hardening.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_security_hardening.py).
- **Status**: **RESOLVED**
- **Residual Risk**: Negligible.

---

### Finding `SEC-15-02`: Unbounded Request Payload Size (DoS Risk)
- **Affected Component**: Backend Request Processing Layer ([`api/main.py`](file:///Users/kazi/Projects/RITUCAST/api/main.py), [`api/routers/advisories.py`](file:///Users/kazi/Projects/RITUCAST/api/routers/advisories.py))
- **Description**: POST endpoints such as `/api/v1/advisories/evaluate` and `/api/v1/risk/evaluate` did not enforce a maximum payload byte ceiling on incoming requests. An attacker sending multi-megabyte payloads could trigger excessive memory allocation and degrade Cloud Run container concurrency.
- **Severity**: **Medium** (CVSS: 5.3)
- **Remediation**: Implemented [`RequestSizeLimitMiddleware`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py) enforcing a configurable `MAX_REQUEST_SIZE_BYTES` (default: 1,048,576 bytes / 1 MB) in [`api/config.py`](file:///Users/kazi/Projects/RITUCAST/api/config.py#L53), returning HTTP 413 `PAYLOAD_TOO_LARGE`.
- **Verification**: Verified via automated test `test_payload_size_limit_returns_413` in [`tests/api/test_security_hardening.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_security_hardening.py).
- **Status**: **RESOLVED**
- **Residual Risk**: Negligible.

---

### Finding `SEC-15-03`: Absence of Backend Rate Limiting
- **Affected Component**: Backend API Service Layer ([`api/main.py`](file:///Users/kazi/Projects/RITUCAST/api/main.py))
- **Description**: While `RATE_LIMIT_PER_MINUTE=60` was defined in configuration settings, no middleware was enforcing client request throttling. High-frequency automated polling or scraping could overwhelm compute resources.
- **Severity**: **Medium** (CVSS: 4.8)
- **Remediation**: Implemented [`RateLimitMiddleware`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py) with in-memory sliding-window request tracking per client IP address. Excludes health check probes (`/health`, `/ready`) to avoid liveness failures. Returns HTTP 429 `RATE_LIMIT_EXCEEDED` with `Retry-After` header.
- **Verification**: Verified via automated tests `test_rate_limiting_headers_on_api_endpoints` and `test_rate_limiting_enforcement_returns_429` in [`tests/api/test_security_hardening.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_security_hardening.py).
- **Status**: **RESOLVED**
- **Residual Risk**: In a multi-instance autoscaled Cloud Run deployment, in-memory rate limiting operates per container instance rather than across a globally shared Redis cluster. Given Ritucast's read-only pilot scale, this defense-in-depth boundary is sufficient.

---

### Finding `SEC-15-04`: Potential Path Traversal in Parquet Data Loading
- **Affected Component**: Agricultural Data Repository ([`api/data_access/repository.py`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py))
- **Description**: The `load_parquet_table(filename: str)` method joined input strings with `self.processed_dir / filename` without verifying that the resolved path stayed within `processed_dir`, nor checking for `..` path traversal characters.
- **Severity**: **Medium** (CVSS: 4.3)
- **Remediation**: Added explicit defensive validation in [`api/data_access/repository.py`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L192):
  1. Rejects filenames containing `..`, `/`, or `\`.
  2. Enforces that filenames end with `.parquet`.
  3. Verifies that the resolved absolute path starts with `self.processed_dir.resolve()`.
- **Verification**: Verified via automated test `test_path_traversal_protection_in_repository` in [`tests/api/test_security_hardening.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_security_hardening.py).
- **Status**: **RESOLVED**
- **Residual Risk**: Negligible.

---

### Finding `SEC-15-05`: Missing Input String Bounds in Request Payloads
- **Affected Component**: API Request Schemas ([`api/schemas/advisories.py`](file:///Users/kazi/Projects/RITUCAST/api/schemas/advisories.py), [`api/schemas/risk.py`](file:///Users/kazi/Projects/RITUCAST/api/schemas/risk.py))
- **Description**: String fields (`upazila_id`, `crop_name`, `growth_stage`) and numerical fields (`ensemble_spread_pct`, `rain_prob_pct`) lacked Pydantic validation bounds (`max_length`, `ge`, `le`), allowing arbitrarily large strings or negative probabilities.
- **Severity**: **Low** (CVSS: 3.1)
- **Remediation**: Added `max_length=50` to `upazila_id`, `max_length=100` to crop and stage fields, and `ge=0.0, le=100.0` bounds to probability/spread fields.
- **Verification**: Validated in Pydantic schema serialization and existing schema validation suites.
- **Status**: **RESOLVED**
- **Residual Risk**: Negligible.

---

### Finding `SEC-15-06`: Transitive Dependency CVEs in Starlette (pip-audit)
- **Affected Component**: FastAPI / Starlette dependency tree ([`requirements.txt`](file:///Users/kazi/Projects/RITUCAST/requirements.txt))
- **Description**: `pip-audit` identified vulnerabilities in transitive dependency `starlette` (version `0.46.2` in standard PyPI index resolution: `PYSEC-2026-1941`, `PYSEC-2026-1942`, `PYSEC-2026-161`, `PYSEC-2026-2281`).
- **Technical Analysis**:
  - `PYSEC-2026-1941` / `PYSEC-2026-1942`: Multipart form parser boundary errors and DoS when handling massive file uploads. **Ritucast does not expose file upload or multipart form endpoints.** All endpoints accept application/json or query parameters.
  - `PYSEC-2026-161`: WebSocket denial of service when processing corrupted frames. **Ritucast does not implement WebSockets.**
  - `PYSEC-2026-2281`: Range header parsing in static file serving. **Ritucast backend serves JSON only; static assets are served exclusively by NGINX.**
- **Severity**: **Low** (Effective Exploitability: None on Ritucast surface)
- **Remediation**: Evaluated and documented. Upgrading Starlette independently of FastAPI is constrained by FastAPI's pinned minor requirements (`fastapi>=0.111.0,<0.116.0`). Monitored in dependency register.
- **Status**: **ANALYZED & ACCEPTED AS LOW RISK**
- **Residual Risk**: Low. No affected code path is reachable.

---

### Finding `SEC-15-07`: Statically Hardcoded Suppression Reason in API Envelope
- **Affected Component**: Advisory Response Serialization ([`api/data_access/repository.py`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L571))
- **Description**: When an advisory was suppressed by the recommendation engine (e.g. due to high ensemble spread), the API layer serialized `"DATA_AGE_EXCEEDED"` unconditionally instead of propagating the actual suppression reason from `primary_card.suppression_reason`.
- **Severity**: **Low** (CVSS: 2.5 - Informational / Explainability)
- **Remediation**: Updated [`api/data_access/repository.py`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L571) to serialize `primary_card.suppression_reason if is_supp else None`.
- **Verification**: Verified via `test_suppression_safeguard_dec10_ensemble_uncertainty` in [`tests/api/test_security_hardening.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_security_hardening.py).
- **Status**: **RESOLVED**
- **Residual Risk**: Negligible.

---

### Finding `SEC-15-08`: Secret and Credential Scanning Verification
- **Affected Component**: Entire Git Repository
- **Description**: Audit of all repository files, Git history, CI workflows, and environment templates for hardcoded tokens, passwords, private keys, or cloud credentials.
- **Findings**:
  - No committed `.env` files. Only [`.env.example`](file:///Users/kazi/Projects/RITUCAST/.env.example) and [`.env.production.example`](file:///Users/kazi/Projects/RITUCAST/.env.production.example) exist, containing placeholders only.
  - Zero private keys (`.pem`, `.key`, `id_rsa`) in repository.
  - GitHub Actions workflows use least-privilege tokens (`permissions: contents: read`).
- **Severity**: **Informational** (Pass)
- **Status**: **VERIFIED CLEAN**
- **Residual Risk**: Negligible.
