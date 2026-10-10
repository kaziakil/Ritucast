# Backup, Recovery, and Disaster Recovery: Ritucast Agricultural Intelligence Platform

## 1. Overview

Ritucast operates under a **Stateless Application Architecture** (`DEC-52`). The production deployment does not maintain a mutable database (e.g., PostgreSQL, MySQL) or persistent disk volumes.

This document details how disaster recovery, dataset provenance preservation, and system reconstitution are executed.

---

## 2. Disaster Recovery Strategy

Because the application is stateless and all operational feature tables are bundled into immutable container images, recovery from catastrophic failure (e.g., cloud region outage, container crash, host infrastructure loss) is instantaneous and fully automated:

### 2.1 Recovery Time Objective (RTO) and Recovery Point Objective (RPO)
- **RTO (Recovery Time Objective)**: $< 60\text{ seconds}$ (the time required for Cloud Run to deploy a new container instance or spin up in an alternate region).
- **RPO (Recovery Point Objective)**: $0\text{ seconds}$ (no runtime transactional farmer data is stored or lost).

---

## 3. Data and Code Reconstitution

| Asset Class | Primary Storage Location | Backup Mechanism | Recovery / Reconstitution Procedure |
| :--- | :--- | :--- | :--- |
| **Source Code & Manifests** | GitHub Repository (`main` branch) | Distributed Git clones | `git clone` from any contributor machine. |
| **Container Images** | Artifact Registry (`asia-south1`) | Multi-region image replication / Local build cache | Re-run `deploy/cloudrun/deploy.sh` or build from source Dockerfiles. |
| **Parquet Datasets** | Bundled in repository (`data/processed/`) | Git LFS / Repository commits | Re-run ingestion pipeline scripts (`pipelines/ingest.py`). |
| **Cloud Configuration** | Declarative Knative YAML files | Git version control | `gcloud run services replace deploy/cloudrun/service-backend.yaml`. |

---

## 4. Multi-Region Failover Procedure

In the event of a catastrophic disaster in Google Cloud's Mumbai region (`asia-south1`):
1. Execute the deployment script targeting an alternate low-latency region (e.g., Singapore `asia-southeast1`):
   ```bash
   export GCP_PROJECT_ID="ritucast-prod"
   export GCP_REGION="asia-southeast1"
   ./deploy/cloudrun/deploy.sh
   ```
2. Update DNS A/AAAA records for `ritucast.app` and `api.ritucast.app` to point to the new regional endpoints.
3. Total failover execution time: $< 5\text{ minutes}$.
