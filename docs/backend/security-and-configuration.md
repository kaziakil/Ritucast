# Ritucast: Security & Configuration Standards

## 1. Configuration Management (`api/config.py`)

Configuration is managed via Pydantic Settings (`pydantic_settings.BaseSettings`). Settings can be overridden by environment variables or a local `.env` file without altering codebase artifacts.

### Key Configuration Variables:
| Variable Name | Default Value | Purpose |
| :--- | :--- | :--- |
| `PROJECT_NAME` | `Ritucast Agricultural Intelligence API` | OpenAPI application title |
| `API_V1_PREFIX` | `/api/v1` | URL route prefix |
| `ENVIRONMENT` | `development` | Deployment environment flag |
| `DEBUG` | `False` | Debug mode (disabled in production) |
| `HOST` | `0.0.0.0` | Server bind interface |
| `PORT` | `8000` | Server bind port |
| `CORS_ORIGINS` | `["http://localhost:3000", ...]` | Permitted client origin whitelist |
| `CACHE_TTL_SECONDS`| `3600` | In-memory table caching duration |
| `DEFAULT_DANGER_LEVEL_M`| `8.25` | Surma river stage danger benchmark |

---

## 2. CORS Policy

The API configures strict CORS origins restricting cross-origin requests to known local development ports (`3000`, `5173`) and the official production domain (`https://ritucast.app`). Wildcard `*` origins are strictly forbidden in production.

---

## 3. Threat Model & Safeguards

### 3.1 Data Leakage Prevention
- Health and error endpoints never return stack traces, operating system versions, or internal absolute file paths.
- Operational logs are sanitized to prevent capturing PII or credentials.

### 3.2 Denial of Service & Resource Exhaustion
- Parquet tables are loaded lazily and cached in-memory; repeated requests do not trigger repeated disk reads.
- Input models limit string lengths and array sizes.

### 3.3 Authentication Boundary Declaration
- The current Phase 10 API exposes public agricultural advisories and environmental observations designed for open access by rural farmers and extension agents.
- Future phases may introduce token-based authentication (e.g. JWT) for administrative data ingestion triggers; however, decision-support endpoints remain unauthenticated to maximize accessibility in rural environments (`NFR-USE-01`).

---

## 4. Related Documentation

- Architecture: [phase-10-backend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md)
- Local Development: [local-development.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/local-development.md)
