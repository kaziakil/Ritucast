# Environment Variables Specification: Ritucast Agricultural Intelligence Platform

## 1. Overview

Ritucast follows the Twelve-Factor App methodology for configuration management. All runtime behavior is driven by environment variables injected into the execution context.

This document serves as the canonical reference for all environment variables supported by the backend and frontend services.

---

## 2. Backend Environment Variables

| Variable Name | Type | Default Value | Required? | Secret? | Purpose & Governance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | String | `development` | Yes | No | Runtime tier (`development`, `staging`, `production`). In production, interactive API docs may be restricted. |
| `DEBUG` | Boolean | `false` | No | No | Enables verbose traceback logging when `true`. Must be `false` in production. |
| `PORT` | Integer | `8000` (Local) / `8080` (Cloud) | No | No | The TCP port the Uvicorn HTTP server binds to. Injected automatically by Google Cloud Run. |
| `HOST` | String | `0.0.0.0` | No | No | Interface IP address to bind to. Must be `0.0.0.0` inside containers. |
| `CORS_ORIGINS` | JSON Array (string) | `["http://localhost:5173"]` | Yes | No | List of permitted HTTP/HTTPS origins for CORS. In production, set to `["https://ritucast.app"]`. |
| `MAX_WEATHER_AGE_HOURS` | Float | `36.0` | No | No | Operational data staleness threshold (`DEC-10`, `NFR-REL-03`). Observations older than this threshold trigger automated advisory suppression. |
| `DEFAULT_DANGER_LEVEL_M` | Float | `8.25` | No | No | Hydrological river level danger mark (meters PWD) for Tahirpur Upazila (`DEC-38`). |
| `BWDB_STATION_ID` | String | `SW175` | No | No | Bangladesh Water Development Board station identifier for Sunamganj/Surma monitoring. |

---

## 3. Frontend Environment Variables

Frontend variables are injected during the build step by Vite (`import.meta.env`).

| Variable Name | Type | Default Value | Required? | Secret? | Purpose & Governance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `VITE_API_BASE_URL` | URL String | `http://localhost:8000` | Yes | **NO (Public)** | Target URL for the Ritucast backend REST API. Never place secrets or private keys in this variable as it is compiled into the public client JavaScript bundle. |

---

## 4. Secret Management Architecture

1. **Zero Secret Principle**: Ritucast currently operates exclusively on publicly accessible, scientifically open datasets (NASA POWER, Sentinel-1 SAR, BMD, BWDB). No proprietary external API keys or commercial database passwords are required for runtime operation.
2. **Future Sensitive Credentials**: Any future integration requiring API tokens (e.g., SMS gateways for farmer text alerts) must be managed using **Google Secret Manager**:
   - Reference via Secret Manager resource name: `projects/PROJECT_ID/secrets/NAME/versions/latest`.
   - Injected into Cloud Run via Knative secret volume mount or environment variable reference.
   - **Never committed to version control.**
