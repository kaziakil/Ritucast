# Security and Responsible AI Test Plan — Ritucast

## 1. Overview

This document specifies the automated and manual verification strategy for evaluating security hardening, input validation, defensive middleware, dependency supply chain, and responsible AI safeguards in Ritucast.

---

## 2. Test Suites and Coverage Matrix

| Test Suite File | Framework | Scope & Objectives | Executed Test Cases |
| :--- | :--- | :--- | :--- |
| [`tests/api/test_security_hardening.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_security_hardening.py) | pytest / TestClient | HTTP security headers, rate limiting, request size limits, path traversal, DEC-17 gating, DEC-10 suppression, disclaimers, and anti-overconfidence copy | 11 automated test cases |
| [`tests/api/test_error_handling_and_security.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_error_handling_and_security.py) | pytest / TestClient | Uniform error envelopes, HTTP 404, HTTP 422 validation, server exception masking | 4 automated test cases |
| [`frontend/src/test/security.test.tsx`](file:///Users/kazi/Projects/RITUCAST/frontend/src/test/security.test.tsx) | vitest / jsdom | Prohibition of `dangerouslySetInnerHTML`, absence of `eval`/`innerHTML`, secret token leakage check, anti-deception mock fallback check | 4 automated test cases |
| [`pipelines/validation/test_semantic_validator.py`](file:///Users/kazi/Projects/RITUCAST/tests/unit/test_semantic_validator.py) | pytest | Physical sanity validation bounds on sensor data (solar rad, humidity, temp) | 5 automated test cases |

---

## 3. Detailed Security Test Specifications

### 3.1 `test_http_security_headers_present`
- **Objective**: Verify that every API response includes OWASP defensive headers.
- **Assertions**:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `X-XSS-Protection: 1; mode=block`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Content-Security-Policy: default-src 'self' ...`
  - `Permissions-Policy: camera=(), microphone=(), geolocation=()`

### 3.2 `test_rate_limiting_enforcement_returns_429`
- **Objective**: Verify that exceeding the sliding window request threshold throttles the client.
- **Assertions**:
  - Responses 1 and 2 return HTTP 200 with decreasing `X-RateLimit-Remaining`.
  - Response 3 returns HTTP 429 `RATE_LIMIT_EXCEEDED` with `Retry-After` header.

### 3.3 `test_payload_size_limit_returns_413`
- **Objective**: Verify that oversized request bodies are rejected immediately.
- **Assertions**: Request exceeding configured byte limit returns HTTP 413 `PAYLOAD_TOO_LARGE`.

### 3.4 `test_path_traversal_protection_in_repository`
- **Objective**: Verify that `load_parquet_table` blocks directory traversal sequences.
- **Assertions**: Inputs like `../../../etc/passwd` or `..\\secrets.txt` raise `ValueError("Path traversal rejected")`.

### 3.5 `test_context_gating_safeguard_dec17`
- **Objective**: Verify that advice is never generated without Upazila, Crop, and Stage (`DEC-17`).
- **Assertions**: Queries missing crop or stage fail with HTTP 422 `CONTEXT_GATING_FAILED`.

### 3.6 `test_suppression_safeguard_dec10_stale_data`
- **Objective**: Verify that weather data $>36\text{h}$ old triggers advisory suppression.
- **Assertions**: Returns `is_suppressed: true` with reason mentioning 36-hour limit.

### 3.7 `test_suppression_safeguard_dec10_ensemble_uncertainty`
- **Objective**: Verify that high ensemble spread ($>50\%$) with ambiguous rain probability ($40\%\text{--}60\%$) triggers suppression.
- **Assertions**: Returns `is_suppressed: true` with reason mentioning ensemble spread.

### 3.8 `test_anti_overconfidence_linguistic_standards`
- **Objective**: Verify that prohibited deterministic phrases never appear in advisory texts.
- **Assertions**: Asserts absence of *"১০০% নিশ্চিত"*, *"নিশ্চিত বৃষ্টি"*, *"ফলনের নিশ্চয়তা"*.

---

## 4. Test Execution Instructions

Execute full automated security verification locally:
```bash
# 1. Run Python security hardening test suite
pytest tests/api/test_security_hardening.py -v

# 2. Run full deterministic backend test suite (104 tests)
pytest -m "not smoke"

# 3. Run frontend security and component tests (21 tests)
cd frontend && npm test

# 4. Verify frontend production compilation
cd frontend && npm run build
```

Related documentation:
- [`docs/security/security-remediation-record.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/security-remediation-record.md)
- [`docs/security/remaining-risks.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/remaining-risks.md)
- [`docs/phases/phase-15/validation-report.md`](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-15/validation-report.md)
