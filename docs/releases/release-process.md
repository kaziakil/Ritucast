# Release Process & Governance SOP: Ritucast

## 1. Overview

This document outlines the standard operating procedure (SOP) for preparing, validating, authorizing, and publishing releases of Ritucast.

---

## 2. Release Lifecycle Stages

```
[ 1. Milestone Freeze ] ──> [ 2. Pre-Release QA ] ──> [ 3. Tag & Packaging ] ──> [ 4. Production Rollout ]
        │                           │                         │                          │
        ▼                           ▼                         ▼                          ▼
  Code review closed       All CI gates PASS         Annotated Git tag          Manual Approver Sign-off
  CHANGELOG updated        Deterministic tests       Release tarball created    Rolling Cloud Run deploy
  Version bumped           Bundle budget verified    Container images tagged    Post-deploy smoke test
```

---

## 3. Step-by-Step Release SOP

### Step 1: Pre-Release Verification
1. Ensure `main` branch is clean and all PRs have merged.
2. Verify full local regression test pass:
   ```bash
   pytest -m "not smoke"
   cd frontend && npm run test && npm run build
   ```
3. Update [CHANGELOG.md](file:///Users/kazi/Projects/RITUCAST/CHANGELOG.md) under a new version heading with all added, changed, and fixed items.

### Step 2: Tagging the Release
1. Create and push an annotated Git tag:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0: Initial Pilot Decision Support Platform"
   git push origin v1.0.0
   ```
2. Pushing the tag triggers `.github/workflows/release.yml`.

### Step 3: Automated Artifact Generation & Container Publishing
1. The GitHub Actions runner generates:
   - `ritucast-v1.0.0.tar.gz` (Source code and configs).
   - `openapi.json` (OpenAPI 3.0 specification).
   - Docker container images pushed to Google Artifact Registry:
     - `asia-south1-docker.pkg.dev/PROJECT_ID/ritucast/backend:v1.0.0`
     - `asia-south1-docker.pkg.dev/PROJECT_ID/ritucast/frontend:v1.0.0`
2. Creates the official **GitHub Release** with changelog notes.

### Step 4: Production Deployment Approval
1. Navigate to the GitHub Actions workflow run for `release.yml`.
2. Locate the `deploy-production` job in the `production` environment.
3. The designated release engineer reviews the release notes and clicks **Review Deployments** $\rightarrow$ **Approve and Deploy**.
4. The runner invokes `deploy/cloudrun/deploy.sh` to update Cloud Run revisions without downtime.
5. Automated post-deployment smoke tests execute and confirm HTTP 200 OK across `/health` and `/ready`.
