# Rollback Procedures & Release Safety: Ritucast Agricultural Intelligence Platform

## 1. Overview

In agricultural decision support, releasing a faulty model, miscalibrated threshold, or broken UI can directly harm farming operations. Ritucast relies on Google Cloud Run's atomic traffic splitting and revision management to achieve instantaneous zero-downtime rollbacks.

---

## 2. Automated & Instantaneous Cloud Run Rollback

Every deployment to Google Cloud Run creates an immutable, timestamped **Revision** (e.g., `ritucast-backend-00012-xyz`). Traffic can be redirected to any previous revision instantaneously.

### 2.1 One-Command Instant Rollback
To roll back the backend service to the previous healthy revision:
```bash
# List past revisions
gcloud run revisions list \
  --service=ritucast-backend \
  --region=asia-south1

# Roll back 100% of traffic to the known-good revision
gcloud run services update-traffic ritucast-backend \
  --to-revisions=ritucast-backend-PREVIOUS_GOOD_REVISION=100 \
  --region=asia-south1
```

To roll back the frontend service:
```bash
gcloud run services update-traffic ritucast-frontend \
  --to-revisions=ritucast-frontend-PREVIOUS_GOOD_REVISION=100 \
  --region=asia-south1
```

**Rollback Latency**: $< 2\text{ seconds}$. The routing switch occurs at Google's global load balancing edge; zero container rebuilding or redeployment is required.

---

## 3. Canary / Gradual Traffic Migration

For critical releases (e.g., updated flood hazard index or new growth stage algorithms), deploy the revision with canary traffic before full rollout:

```bash
# Deploy new revision without routing traffic
gcloud run deploy ritucast-backend \
  --image=asia-south1-docker.pkg.dev/PROJECT_ID/ritucast/backend:v1.1.0 \
  --no-traffic \
  --region=asia-south1

# Route 10% traffic to new revision for pilot testing
gcloud run services update-traffic ritucast-backend \
  --to-revisions=ritucast-backend-v1-1-0=10,ritucast-backend-v1-0-0=90 \
  --region=asia-south1
```

If error rates increase or validation checks fail, revert traffic to 100% on the old revision immediately.

---

## 4. Local / Docker Rollback Procedure

When running via Docker Compose:
```bash
# Pull previous stable images or check out previous Git release tag
git checkout v1.0.0
docker compose down
docker compose up -d --build
```
