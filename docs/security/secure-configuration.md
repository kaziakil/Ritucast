# Secure Configuration and Environment Baseline — Ritucast

## 1. Overview

This document specifies the secure configuration standards across environments (development, staging, production) for Ritucast, ensuring that debug features, permissive CORS policies, and local testing paths are strictly prevented in hosted environments.

---

## 2. Environment Matrix & Secure Defaults

| Setting | Local Development (`.env.example`) | Production Deployment (`.env.production.example`) | Security Rationale |
| :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | `development` | `production` | Enables production HSTS and strict security headers |
| `DEBUG` | `true` (or `false`) | `false` | Disables interactive debuggers, auto-reloading, and verbose error traces |
| `HOST` | `0.0.0.0` | `0.0.0.0` | Binds to container network interface |
| `PORT` | `8000` | `8000` (or Cloud Run `$PORT` default `8080`) | Standard internal HTTP container port |
| `CORS_ORIGINS` | `["http://localhost:3000", "http://127.0.0.1:3000", ...]` | `["https://ritucast.app", "https://www.ritucast.app"]` | Restricts cross-origin requests exclusively to authorized production web client |
| `CORS_ALLOW_CREDENTIALS` | `true` | `false` (or restricted domain only) | Eliminates CSRF risk on unauthenticated public endpoints |
| `CORS_ALLOW_METHODS` | `["GET", "POST", "OPTIONS"]` | `["GET", "POST", "OPTIONS"]` | Blocks dangerous HTTP verbs (`PUT`, `DELETE`, `PATCH`, `TRACE`) |
| `CORS_ALLOW_HEADERS` | `["*"]` | `["Content-Type", "Accept", "Authorization"]` | Minimizes allowable request header surface |
| `RATE_LIMIT_PER_MINUTE` | `60` | `120` | Protects serverless container concurrency |
| `MAX_REQUEST_SIZE_BYTES`| `1048576` (1 MB) | `1048576` (1 MB) | Mitigates buffer and memory exhaustion attacks |
| `MAX_WEATHER_AGE_HOURS` | `36.0` | `36.0` | Enforces scientific suppression rule (`DEC-10`, `NFR-REL-03`) |

---

## 3. Configuration Guardrails

### 3.1 Pydantic Settings Validation ([`api/config.py`](file:///Users/kazi/Projects/RITUCAST/api/config.py))
- Runtime configuration is managed by `pydantic-settings.BaseSettings`.
- Strong type coercion guarantees that malformed port numbers, string booleans, or missing directories fail loudly at server startup rather than causing intermittent runtime crashes.
- `extra="ignore"` ensures extraneous environment variables passed by hosting platforms (e.g. Cloud Run metadata) do not break initialization.

### 3.2 Anti-Leakage Verification
The following dangerous configurations are strictly blocked in production:
1. **No Wildcard CORS in Production**: `CORS_ORIGINS = ["*"]` is prohibited. Only explicitly listed domain origins are permitted.
2. **No Localhost Endpoints in Frontend Bundle**: Frontend API base URL (`VITE_API_BASE_URL`) defaults to relative path `/` in production builds, directing requests through the NGINX reverse proxy rather than hardcoding `http://localhost:8000`.
3. **No Embedded Test Tokens**: All test mocks and fixtures reside exclusively within `tests/` and are never loaded by production startup scripts.

Related documentation:
- [`docs/security/api-security.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/api-security.md)
- [`docs/ci-cd/environment-separation.md`](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/environment-separation.md)
- [`docs/ci-cd/secrets-and-permissions.md`](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/secrets-and-permissions.md)
