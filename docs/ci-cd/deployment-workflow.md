# Automated Deployment Workflow Specification: Ritucast

## 1. Overview

This document specifies the continuous delivery and automated deployment mechanisms governing how approved release artifacts are published and rolled out to Google Cloud Run.

---

## 2. Deployment Architecture in CI/CD

Deployment is executed exclusively through the **`release.yml`** workflow, triggered by semantic version tags (`v*.*.*`) or manual maintainer dispatch with required parameters.

```
[ Tag v1.0.0 pushed to main ]
              │
              ▼
    Job 1: verify-and-package
    - Pytest deterministic check
    - OpenAPI JSON schema extraction
    - ritucast-v1.0.0.tar.gz generation
    - GitHub Release published
              │
              ▼
    Job 2: build-and-publish-containers
    - Google Cloud Auth via Workload Identity (OIDC)
    - Build Backend & Frontend Docker images
    - Tag: :v1.0.0, :COMMIT_SHA, :latest
    - Push to Artifact Registry (asia-south1)
              │
              ▼
    Job 3: deploy-production
    ┌──────────────────────────────────────────────┐
    │  GitHub Environment: 'production'            │
    │  REQUIRES MANUAL APPROVER REVIEW / SIGN-OFF  │
    └──────────────────────┬───────────────────────┘
                           │ (Approved)
                           ▼
    - Execute deploy/cloudrun/deploy.sh
    - Cloud Run rolling revision update
    - Post-deployment /health & /ready probes
```

---

## 3. Environment Protection & Approval Gate

The `deploy-production` job is bound to the GitHub Actions **`production` environment**:
1. **Required Reviewers**: Before the job begins, GitHub Actions sends an approval notification to designated release engineers.
2. **Deployment URL**: Automatically registers `https://ritucast.app` in GitHub deployment history.
3. **Audit Trail**: Every deployment record contains the exact Git tag, commit SHA, approver identity, and timestamp.

---

## 4. Post-Deployment Verification & Smoke Testing

Immediately following deployment, `deploy/cloudrun/deploy.sh` executes automated HTTP smoke probes:
1. `GET https://api.ritucast.app/health` $\rightarrow$ verifies process liveness (HTTP 200).
2. `GET https://api.ritucast.app/ready` $\rightarrow$ verifies Parquet feature store and analytical engine availability (HTTP 200).
3. `GET https://ritucast.app/health` $\rightarrow$ verifies frontend NGINX server availability (HTTP 200).

If any probe fails, the deployment script emits an error, and the operator can invoke the instant revision rollback command (`gcloud run services update-traffic ritucast-backend --to-revisions=...`).
