# Environment Separation & Configuration Strategy: Ritucast

## 1. Overview

Ritucast strictly isolates runtime environments to ensure that development testing, continuous integration, staging pre-flight checks, and production advisory delivery cannot cross-contaminate configurations or data.

---

## 2. Environment Taxonomy

| Environment Parameter | Local Development | GitHub Actions (CI) | Hosted Staging | Hosted Production |
| :--- | :--- | :--- | :--- | :--- |
| **Execution Host** | Local machine / Docker Compose | GitHub Hosted Ubuntu Runner | Google Cloud Run (`asia-south1`) | Google Cloud Run (`asia-south1`) |
| **API Base URL** | `http://localhost:8000` | N/A (Isolated test runners) | `https://staging-api.ritucast.app` | `https://api.ritucast.app` |
| **Frontend URL** | `http://localhost:3000` | N/A (Static build check) | `https://staging.ritucast.app` | `https://ritucast.app` |
| **Allowed CORS** | `["http://localhost:3000","http://localhost:5173"]`| Local test clients | `["https://staging.ritucast.app"]` | `["https://ritucast.app"]` |
| **Data Source** | `data/sample/` & local Parquet | `data/sample/` (Deterministic) | Bundled Parquet (`/app/data/`) | Bundled Parquet (`/app/data/`) |
| **Debug Mode** | `DEBUG=true` | `DEBUG=true` | `DEBUG=false` | `DEBUG=false` |
| **Logging Level** | `DEBUG` / `INFO` | `INFO` | `INFO` | `INFO` |
| **Scale Limits** | 1 instance | 1 container | `minScale: 0`, `maxScale: 2` | `minScale: 0`, `maxScale: 5` |

---

## 3. Configuration Guardrails

1. **No Localhost in Production**: Production builds enforce `VITE_API_BASE_URL="https://api.ritucast.app"`. The CI build job explicitly sets this environment variable during bundle creation.
2. **Strict CORS Policy**: Production backend rejects wildcard origins (`*`) and validates against explicit domains.
3. **No Mock Data Fallback in Production**: While development can use local mocks, the production backend strictly validates against verified Parquet feature stores; missing data triggers formal automated suppression (`DEC-10`) rather than synthetic mock substitution.
