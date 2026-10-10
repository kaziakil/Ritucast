# CI/CD Automation Workflow Specification: Ritucast

## 1. Overview

Ritucast implements automated continuous integration and continuous deployment via **GitHub Actions** (`.github/workflows/ci-cd.yml`).

The workflow guarantees that no unverified or failing code can be merged to `main` or deployed to cloud runtimes.

---

## 2. Pipeline Stages & Architecture

The pipeline consists of four sequential, gated jobs:

```
[ Push / PR to main ]
          │
          ├──> Job 1: test-backend (Python 3.10, pytest)
          │
          ├──> Job 2: test-frontend (Node 20, vitest, npm run build)
          │
          ▼ (Both must pass)
     Job 3: build-containers (Docker Buildx multi-stage verification)
          │
          ▼ (Main branch push only & secrets configured)
     Job 4: deploy-cloudrun (Google Cloud Run automated deploy via deploy.sh)
```

### Job 1: `test-backend`
- Installs `requirements.txt` and `requirements-dev.txt`.
- Runs full backend unit and integration test suite (`pytest tests/ -v`).
- Gate: 100% test pass required.

### Job 2: `test-frontend`
- Installs dependencies using clean install (`npm ci`).
- Executes Vitest unit and component tests (`npm run test`).
- Verifies production bundle build (`npm run build`).
- Gate: 100% test pass and zero compilation errors required.

### Job 3: `build-containers`
- Depends on `test-backend` and `test-frontend`.
- Executes Docker Buildx to build both backend and frontend images.
- Validates Dockerfile syntax, multi-stage layer caching, and packaging integrity.

### Job 4: `deploy-cloudrun`
- Runs only on pushes to `main`.
- Authenticates using **Google Workload Identity Federation** (zero long-lived service account keys stored in GitHub).
- Invocates `deploy/cloudrun/deploy.sh` to deploy backend and frontend containers to Cloud Run.
- Executes automated smoke tests post-deployment.
