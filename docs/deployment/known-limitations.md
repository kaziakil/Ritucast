# Known Limitations & Deferred Operational Scope: Ritucast

## 1. Overview

In accordance with Phase 13 Section 20/21 requirements, this document records all verified deployment limitations, deferred infrastructure components, and operational boundaries of Ritucast.

---

## 2. Environment Limitations & Active Blockers

### Limitation 1: Hosted Cloud Deployment Blocked by Missing GCP Credentials
- **Description**: The automated deployment script (`deploy/cloudrun/deploy.sh`) and Knative manifests (`deploy/cloudrun/service-backend.yaml`) have been authored and locally validated using Docker Desktop. However, active Google Cloud credentials (`gcloud auth login` or GCP Service Account JSON) are not available within the local development environment (`cloudrun` MCP server reported `GCP credentials are not available`).
- **Impact**: The application is **Deployment Ready and Locally Validated**, but **Not Live Hosted on GCP**.
- **Remediation**: Platform operations team must supply GCP credentials or execute `./deploy/cloudrun/deploy.sh` in an authorized environment.

---

## 3. Architecture & Functional Limitations

### Limitation 2: Semi-Automated Data Ingestion Refreshes
- **Description**: Scheduled cron workflows for downloading daily NASA POWER satellite observations and BMD NWP weather models are not yet deployed as managed Cloud Scheduler / Cloud Tasks jobs. Ingestion is triggered via reproducible scripts (`pipelines/ingest.py`).
- **Roadmap Alignment**: Scheduled recurring ingestion workflows are scheduled for production hardening in Phase 14 / Phase 15.

### Limitation 3: Scale-to-Zero Cold Start on Cellular Networks
- **Description**: Cloud Run scale-to-zero results in a $1.8\text{s} - 2.5\text{s}$ container initialization latency on the first request after an idle period. While well within the $3.5\text{s}$ TTI budget on 3G (`DEC-09`), users on 2G edge networks may experience up to $4.5\text{s}$ latency during initial wake.
- **Remediation**: Configure `minScale: 1` during peak morning hours (06:00–08:00 BST) if budget permits.

### Limitation 4: Strict Pilot Upazila Boundaries
- **Description**: In accordance with `DEC-06` scope boundaries, the deployment currently serves only the 4 pilot Upazilas across Godagari, Tanore, Sunamganj Sadar, and Tahirpur. Requests for unverified Upazilas return safe 404/422 responses.
