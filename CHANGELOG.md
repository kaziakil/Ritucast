# Changelog

All notable changes to the **Ritucast** Agricultural Intelligence Platform are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-10

### Added
- **Pilot Geography & Boro Rice Decision Support**:
  - High Barind Tract (Godagari, Tanore Upazilas) for drought monitoring, AWD irrigation scheduling, and soil water deficit estimation.
  - Haor Basin (Sunamganj Sadar, Tahirpur Upazilas) for pre-monsoon transboundary flash-flood early warnings and early harvest advisories.
- **Scientific Indicators & Analytics Engine**:
  - FAO-56 Penman-Monteith reference evapotranspiration ($ET_0$) calculation module.
  - Crop water demand ($ET_c$) using BRRI phenological stage crop coefficients ($K_c$).
  - Daily mass-balance soil water deficit ($D_t$) and Alternating Wetting and Drying (AWD) thresholds.
  - Flash-flood hazard index ($I_{\text{flood}}$) coupling satellite precipitation, river stage, rate-of-rise, and catchment rainfall.
- **Backend API & Service Layer (`api/`)**:
  - FastAPI modular service exposing RESTful endpoints for Upazilas, Meteorology, Water Balance, Flood Hazard, and Advisories.
  - OpenAPI 3.0 interactive documentation at `/docs` and schema at `/openapi.json`.
  - Decoupled health probes: `/health` (liveness) and `/ready` (dependency and data integrity).
  - Centralized exception translation and strict input validation via Pydantic v2 schemas.
- **Frontend Web Application (`frontend/`)**:
  - React 19 SPA built with TypeScript and Vite 6.
  - Custom high-contrast Bangla design system with Vanilla CSS tokens and mobile-first layout.
  - 4-Tier information taxonomy display (Observations, Indicators, Predictions, Recommendations).
  - Contextual gating confirmation for Upazila, Crop (`boro_rice`), and Growth Stage.
  - Automated advisory suppression alert banner for stale data ($>36\text{h}$) or high forecast uncertainty ($>50\%$).
- **Deployment Architecture & Containerization (`deploy/`)**:
  - Multi-stage `Dockerfile.backend` executing as unprivileged user `ritucast` (UID 10001).
  - Multi-stage `Dockerfile.frontend` using `nginx:alpine` with Gzip compression and strict CSP/HSTS headers.
  - Local multi-service orchestration via `docker-compose.yml`.
  - Serverless Google Cloud Run Knative manifests (`service-backend.yaml`, `service-frontend.yaml`).
  - Automated deployment script `deploy/cloudrun/deploy.sh`.
- **CI/CD Automation & Release Management (`.github/workflows/`)**:
  - Multi-job continuous integration pipeline (`ci.yml`) covering code quality, deterministic backend tests, frontend tests, security audit, and container builds.
  - Scheduled and manual live data smoke testing workflow (`live-data-smoke.yml`).
  - Release packaging and production delivery workflow with approval gates (`release.yml`).
  - Separation of deterministic regression tests from live external API checks via `pytest -m "not smoke"`.

### Changed
- Refactored workflow triggers to isolate pull-request validation from release delivery.
- Added explicit mark registration in `pytest.ini` for `smoke`, `integration`, and `unit` test suites.

### Security & Governance
- Zero secrets committed to source control; configuration managed via `.env.example` and environment variables.
- Non-root container execution enforced.
- Client payload budget enforced: total production JS/CSS assets compress to $220.65\text{ kB}$ ($<15\%$ of $1.5\text{MB}$ `DEC-09` ceiling).

### Known Limitations
- Live cloud deployment to Google Cloud Run requires external GCP credentials to be supplied by platform administrators.
- Automated daily satellite data refresh via Cloud Scheduler is planned for Phase 15/16.
