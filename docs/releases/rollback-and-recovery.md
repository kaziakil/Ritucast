# Rollback and Release Recovery Strategy: Ritucast

## 1. Overview

In an agricultural decision-support system, an incorrect release (e.g., miscalculated flood risk or broken irrigation guidance) requires immediate remediation.

This document specifies the rollback procedures, recovery protocols, and post-incident review requirements for release failures.

---

## 2. Immediate Production Rollback SOP

Google Cloud Run retains previous container revisions automatically. In the event of an operational anomaly, rollback is executed via traffic shifting without redeploying code:

### Step 1: Immediate Cloud Run Traffic Rollback
```bash
# 1. Identify previous known-good revision
gcloud run revisions list \
  --service=ritucast-backend \
  --region=asia-south1

# 2. Shift 100% of live traffic back to the known-good revision
gcloud run services update-traffic ritucast-backend \
  --to-revisions=ritucast-backend-PREVIOUS_REVISION=100 \
  --region=asia-south1

# 3. Shift frontend traffic if frontend assets were modified
gcloud run services update-traffic ritucast-frontend \
  --to-revisions=ritucast-frontend-PREVIOUS_REVISION=100 \
  --region=asia-south1
```
**Execution Latency**: $< 2\text{ seconds}$. Traffic shift occurs globally at Google's edge.

### Step 2: Verification of Reverted Revision
```bash
curl -sI https://api.ritucast.app/health
curl -sI https://ritucast.app/health
```
Verify that both endpoints return HTTP 200 OK and report the previous version tag.

---

## 3. Git Release Recovery Procedure
1. Create a hotfix patch branch from the previous stable tag:
   ```bash
   git checkout -b hotfix/v1.0.1 v1.0.0
   ```
2. Apply the minimal necessary bug fix.
3. Verify all deterministic tests pass: `pytest -m "not smoke"` and `npm run test`.
4. Merge back into `main` and tag as `v1.0.1`.
5. Re-run `release.yml` with the updated patch version.

---

## 4. Post-Incident Review Protocol
Every release rollback requires:
1. Incident timeline log documenting when the defect was identified and when rollback occurred.
2. Root-cause analysis (RCA) explaining why CI/CD quality gates did not catch the issue.
3. Addition of a new automated regression test in `tests/` or `frontend/src/test/` to prevent future regressions.
