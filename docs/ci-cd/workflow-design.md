# Workflow Design & Job Dependency Specification: Ritucast

## 1. Overview

This document details the internal design, concurrency models, dependency DAGs, and execution steps of the Ritucast CI/CD workflows.

---

## 2. Continuous Integration Workflow (`ci.yml`)

### Job Dependency Graph
```
        ┌──────────────────┐
        │   actions/checkout│
        └────────┬─────────┘
                 │
       ┌─────────┴─────────┬───────────────────┐
       ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌────────────────┐
│ code-quality │   │ test-backend │   │ test-frontend  │
│ (Lint & Type)│   │ (Pytest)     │   │ (Vitest+Build) │
└──────┬───────┘   └──────┬───────┘   └────────┬───────┘
       │                  │                    │
       │                  ▼                    │
       │          ┌────────────────┐           │
       │          │ security-audit │           │
       │          └────────────────┘           │
       │                  │                    │
       └──────────────────┼────────────────────┘
                          ▼
             ┌─────────────────────────┐
             │ container-verification  │
             │ (Docker Buildx verify)  │
             └─────────────────────────┘
```

### Job Step Specifications

#### 1. `code-quality`
- **Runner**: `ubuntu-latest`
- **Steps**:
  1. `actions/checkout@v4`
  2. Setup Python 3.10 with pip cache.
  3. `flake8` syntax and undefined name verification: `flake8 api/ analytics/ pipelines/ tests/ --count --select=E9,F63,F7,F82`.
  4. Setup Node.js 20 with npm cache.
  5. `npm ci` in `frontend/`.
  6. `npm run lint` (`oxlint`).
  7. `npx tsc -b` (full TypeScript project compilation check).

#### 2. `test-backend-deterministic`
- **Runner**: `ubuntu-latest`
- **Steps**:
  1. Setup Python 3.10.
  2. Install `requirements.txt` and `requirements-dev.txt`.
  3. Run deterministic tests: `pytest -m "not smoke" --cov=api --cov=analytics --cov=pipelines --cov-report=xml:coverage.xml`.
  4. Upload `coverage.xml` as a build artifact (retention: 14 days).

#### 3. `test-frontend-deterministic`
- **Runner**: `ubuntu-latest`
- **Steps**:
  1. Setup Node.js 20.
  2. Install dependencies: `npm ci`.
  3. Run Vitest test suite: `npm run test`.
  4. Build production bundle: `npm run build` with `VITE_API_BASE_URL=https://api.ritucast.app`.
  5. Upload `frontend/dist` directory as a build artifact (retention: 14 days).

#### 4. `security-audit`
- **Runner**: `ubuntu-latest`
- **Steps**:
  1. Audit backend dependencies via `pip-audit -r requirements.txt`.
  2. Audit frontend dependencies via `npm audit --audit-level=high`.
  3. Scan commit diffs for accidental private key and token commits.

#### 5. `container-verification`
- **Runner**: `ubuntu-latest`
- **Needs**: `[code-quality, test-backend-deterministic, test-frontend-deterministic]`
- **Steps**:
  1. Set up Docker Buildx via `docker/setup-buildx-action@v3`.
  2. Build backend image: `Dockerfile.backend` (context: `.`).
  3. Build frontend image: `Dockerfile.frontend` (context: `.`).

---

## 3. Continuous Delivery & Release Workflow (`release.yml`)

### Job Execution Sequence
1. **`verify-and-package`**:
   - Re-verifies all deterministic tests.
   - Extracts OpenAPI 3.0 JSON specification directly from the FastAPI application instance.
   - Packages release tarball `ritucast-${TAG}.tar.gz` containing application code, schemas, and configurations.
   - Creates a formal GitHub Release using `softprops/action-gh-release@v2`.
2. **`build-and-publish-containers`**:
   - Authenticates to Google Cloud via Workload Identity Federation.
   - Builds and tags container images with `vX.Y.Z`, short commit SHA, and `latest`.
   - Pushes images to Google Artifact Registry in `asia-south1`.
3. **`deploy-production`**:
   - Environment: `production` with required manual reviewer sign-off.
   - Invocates `deploy/cloudrun/deploy.sh`.
   - Runs post-deployment health check smoke tests against live endpoints.
