# Operational Troubleshooting Runbook: Ritucast Agricultural Intelligence Platform

## 1. Overview

This runbook outlines diagnosis and remediation steps for the most common operational and deployment issues encountered in Ritucast.

---

## 2. Common Scenarios and Remediation

### Scenario 1: Backend Container Reports `503 Service Unavailable` on `/ready`
- **Symptom**: Cloud Run does not route traffic to the backend, or the frontend shows a persistent "System Degraded" banner.
- **Cause**: One or more required Parquet feature files are missing or unreadable in `/app/data/processed/` or `/app/data/sample/`.
- **Diagnosis**:
  ```bash
  curl -s https://api.ritucast.app/ready
  ```
  Inspect `missing_dependencies` in the JSON response.
- **Remediation**:
  1. Inspect the build context to verify Parquet files exist locally.
  2. Ensure `.dockerignore` did NOT accidentally exclude `data/processed/` or `data/sample/`.
  3. Rebuild and push the backend container image.

---

### Scenario 2: Frontend Shows CORS Errors in Browser Console
- **Symptom**: API queries fail with `Access to XMLHttpRequest has been blocked by CORS policy`.
- **Cause**: Backend `CORS_ORIGINS` environment variable does not match the frontend's origin URL.
- **Diagnosis**:
  ```bash
  curl -I -H "Origin: https://ritucast.app" https://api.ritucast.app/health
  ```
  Check if `Access-Control-Allow-Origin: https://ritucast.app` is returned.
- **Remediation**:
  Update backend environment variable via gcloud:
  ```bash
  gcloud run services update ritucast-backend \
    --update-env-vars='CORS_ORIGINS=["https://ritucast.app"]' \
    --region=asia-south1
  ```

---

### Scenario 3: Cold Start Latency Exceeds 5 Seconds
- **Symptom**: First request after idle takes $>5\text{s}$ on 3G network.
- **Cause**: Container image size too large or CPU throttling during startup.
- **Diagnosis**:
  Review Cloud Run startup latency logs in Google Cloud Logging.
- **Remediation**:
  1. Ensure backend container uses the multi-stage build (`deploy/docker/Dockerfile.backend`).
  2. Set `min-instances=1` during critical morning advisory windows (06:00–08:00 BST) if immediate zero-cold-start performance is prioritized over free-tier compute.

---

### Scenario 4: Automated Advisory Suppression Displayed Unexpectedly
- **Symptom**: User receives notice: *"পূর্বাভাস ডেটা ৩৬ ঘণ্টার বেশি পুরনো হওয়ায় সাময়িকভাবে সতর্কতা স্থগিত রয়েছে"* (`DEC-10`).
- **Cause**: Ingested weather observations have a timestamp $>36\text{ hours}$ old.
- **Diagnosis**:
  Check `/api/v1/context/summary` timestamp metadata against current UTC time.
- **Remediation**:
  Trigger meteorological data refresh pipeline (`python -m pipelines.ingest`).
