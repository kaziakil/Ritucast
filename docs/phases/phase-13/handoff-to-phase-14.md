# Phase 13 to Phase 14 Handoff Specification: Ritucast

## 1. Executive Summary

This handoff document formally concludes **Phase 13: Deployment Architecture and Production Readiness** and establishes the operational baseline and architectural contracts for **Phase 14**.

All containerization manifests, build pipelines, environment configurations, security policies, and local multi-service orchestration environments have been verified and frozen.

---

## 2. Verified Phase 13 Deliverables & Baseline State

### 2.1 Container & Deployment Artifacts
- **Backend Container (`deploy/docker/Dockerfile.backend`, `Dockerfile`)**: Multi-stage build (`python:3.10-slim-bookworm`), executes under unprivileged UID 10001 (`ritucast`), binds dynamically to `$PORT` (default 8000/8080), includes native `/health` check.
- **Frontend Container (`deploy/docker/Dockerfile.frontend`)**: Multi-stage build (`node:20-alpine` builder $\rightarrow$ `nginx:alpine` runtime), serves Gzip compressed static assets ($220.65\text{kB}$ gzip), listens on ports 80 and 8080, enforces strict CSP/HSTS/X-Frame-Options headers.
- **Local Multi-Service Orchestration (`docker-compose.yml`)**: Orchestrates backend (`8000:8000`) and frontend (`3000:80`) with automated health check dependency synchronization.
- **Cloud Run Knative Manifests (`deploy/cloudrun/`)**:
  - `service-backend.yaml`: Knative v1 service for `ritucast-backend` in `asia-south1`.
  - `service-frontend.yaml`: Knative v1 service for `ritucast-frontend` in `asia-south1`.
  - `deploy.sh`: End-to-end automated gcloud CLI deployment script.
- **CI/CD Automation (`.github/workflows/ci-cd.yml`)**: Automated GitHub Actions workflow covering backend tests, frontend tests, container build verification, and Cloud Run deployment.
- **Documentation**: 18 comprehensive specifications under `docs/deployment/`.

### 2.2 Test Suite Verification
- Backend pytest suite: **95 passed, 0 failed**.
- Frontend Vitest suite: **17 passed, 0 failed**.
- Frontend production bundle: **Compiled cleanly via `npm run build` ($220.65\text{kB}$ gzipped)**.

---

## 3. Interfaces & Contracts Frozen for Phase 14

Phase 14 must preserve the following operational interfaces and invariants:

1. **Port & Interface Contract**:
   - Backend must bind to `0.0.0.0` and respect the `$PORT` environment variable.
   - Frontend NGINX listens on ports 80 and 8080.
2. **Health Check Probes**:
   - `/health`: Liveness probe (must return HTTP 200 within $<10\text{ms}$).
   - `/ready`: Readiness probe (validates Parquet datasets and analytical models).
3. **Information Taxonomy (`DEC-08`) & Non-Goals (`DEC-06`)**:
   - 4-tier visual separation (Observation, Indicator, Prediction, Recommendation).
   - Contextual gating (`DEC-17`) on Upazila, Crop (`boro_rice`), and Growth Stage.
   - Automated suppression (`DEC-10`) on stale data ($>36\text{h}$) or high forecast spread ($>50\%$).
4. **Client Hardware & Bundle Budget (`DEC-09`)**:
   - Combined JavaScript and CSS bundle must not exceed $1.5\text{MB}$ uncompressed payload.

---

## 4. Pending Cloud Credentials Notice

- **Operational Status**: The application is **Deployment Ready and Locally Validated**.
- **Pending Step**: Live deployment to GCP Cloud Run requires the platform operations team to run `deploy/cloudrun/deploy.sh` with active `GCP_PROJECT_ID` and GCP credentials.

---

## 5. Next Steps for Phase 14

Phase 14 will proceed in strict accordance with project governance.
**Do not execute Phase 14 until the user explicitly issues the Phase 14 directive.**
