# Backup, Disaster Recovery & Artifact Preservation SOP — Ritucast

## 1. Architecture Context & Storage Reality

In accordance with architectural decisions [`DEC-21`](file:///Users/kazi/Projects/RITUCAST/docs/planning/decision-log.md#dec-21-backend--spatial-datastore-fastapi-python-311-postgresql-16--postgis-34) and [`DEC-52`](file:///Users/kazi/Projects/RITUCAST/docs/planning/decision-log.md#dec-52-in-image-parquet-data-bundling-for-pilot-architecture), Ritucast operates an ultra-lean, stateless serverless architecture:
- **No Heavy Relational Database**: In the pilot phase, processed agricultural feature tables (`<110KB` total) are pre-compiled and bundled directly within the container image or read from immutable file storage.
- **Stateless Backend**: The FastAPI backend container retains zero mutable user session state or database writes.
- **Zero-PII Footprint**: The application does not store farmer profiles, phone numbers, or passwords, completely eliminating customer database corruption or data leak recovery liabilities.

---

## 2. Artifact Preservation & Backup Matrix

| Artifact Category | Storage Location | Backup Mechanism | Retention Policy | Recovery Objective |
| :--- | :--- | :--- | :--- | :--- |
| **Source Code & Manifests** | GitHub (`RITUCAST/main`) | Git commit history with branch protection | Permanent versioned history | Instant checkout ($\text{RTO} < 10\text{s}$) |
| **Container Images** | Google Artifact Registry (`asia-south1`) | Immutable SemVer tags and SHA-256 digests (`DEC-55`) | Latest 20 production release images | $\text{RTO} < 30\text{s}$, $\text{RPO} = 0\text{s}$ |
| **Processed Parquet Tables** | Repository `data/processed/` + GCS Bucket | Git LFS / GitHub release tarball assets | All release version snapshots | $\text{RTO} < 60\text{s}$, $\text{RPO} = 0\text{s}$ |
| **Raw Geospatial Rasters** | Local scratch / GCS raw archive | Ephemeral cache; reproducibly re-downloadable via pipeline | 30 days rolling cache | Re-ingested via pipeline script |

---

## 3. Disaster Recovery (DR) Targets

- **Recovery Point Objective (RPO)**: **$0\text{ seconds}$** (All serving data is bundled with code or versioned as immutable release assets).
- **Recovery Time Objective (RTO)**: **$<60\text{ seconds}$** (Traffic shift to a known-good Cloud Run revision or container redeployment).

---

## 4. Disaster Recovery & Rollback Procedures

### 4.1 Scenario A: Cloud Run Service Rollback (Instant Traffic Shift)
If a newly deployed container revision exhibits runtime defects:
```bash
# 1. Identify previous healthy revision
gcloud run revisions list --service=ritucast-backend --region=asia-south1

# 2. Shift 100% of live traffic back to previous revision (<2s execution)
gcloud run services update-traffic ritucast-backend \
  --region=asia-south1 \
  --to-revisions=ritucast-backend-00014-qwe=100

# 3. Verify service health
curl -s https://api.ritucast.gov.bd/health | jq .
```

### 4.2 Scenario B: Container Re-Deployment from Image Tag
If Cloud Run service configuration was corrupted or deleted:
```bash
# Deploy verified release image from Artifact Registry
gcloud run deploy ritucast-backend \
  --image=asia-south1-docker.pkg.dev/ritucast-pilot/ritucast-backend/app:v1.0.0 \
  --region=asia-south1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=8000 \
  --memory=256Mi \
  --cpu=1
```

### 4.3 Scenario C: Local Container Rebuild and Recovery
To spin up the entire application stack from scratch on a clean machine:
```bash
git clone https://github.com/organization/RITUCAST.git
cd RITUCAST
docker compose up --build -d

# Verify full stack health
curl -s http://localhost:8000/health/deep | jq .status
```

---

## 5. Backup & Recovery Verification Test

To test disaster recovery reproducibly without live cloud dependencies:
```bash
# Execute automated recovery test
pytest tests/failure/test_failure_scenarios.py -v
```
All failure simulation tests assert that missing or corrupted files fail safely, returning HTTP 503 rather than crashing or delivering misleading advice.
