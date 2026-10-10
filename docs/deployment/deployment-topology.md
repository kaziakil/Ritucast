# Deployment Topology: Ritucast Agricultural Intelligence Platform

## 1. System Topology Overview

This document defines the network and runtime topology for the Ritucast platform in production.

```
+-----------------------------------------------------------------------------------------+
|                                    INTERNET (HTTPS)                                     |
+-----------------------------------------------------------------------------------------+
                                             │
                       +─────────────────────┴─────────────────────+
                       │                                           │
                       ▼                                           ▼
          +─────────────────────────+                 +─────────────────────────+
          | Frontend URL            |                 | Backend Direct URL      |
          | https://ritucast.app    |                 | https://api.ritucast.app|
          +─────────────────────────+                 +─────────────────────────+
                       │                                           │
                       │ TLS 1.3 Termination                       │ TLS 1.3 Termination
                       ▼                                           ▼
       +───────────────────────────────+           +───────────────────────────────+
       | ritucast-frontend (Cloud Run) |           | ritucast-backend (Cloud Run)  |
       | Image: frontend:latest        |           | Image: backend:latest         |
       | Port: 8080 (NGINX)            |           | Port: 8080 (Uvicorn / FastAPI)|
       | Scale: 0 -> 5 instances       |           | Scale: 0 -> 5 instances       |
       +───────────────────────────────+           +───────────────────────────────+
                       │                                           │
         Proxy /api/*  │                                           │ Read-only memory map
                       └───────────────────┐                       ▼
                                           │           +───────────────────────────+
                                           │           | Embedded Data Artifacts   |
                                           └──────────>| - data/processed/*.parquet|
                                                       | - data/sample/*.geojson   |
                                                       +───────────────────────────+
```

---

## 2. Network Boundaries & Zones

### Public Zone (Ingress)
- **Frontend FQDN**: `https://ritucast.app` (or `https://ritucast-frontend-[hash]-el.a.run.app`).
  - Publicly accessible over IPv4/IPv6 via Managed Google HTTPS Load Balancer with automated Google-managed SSL certificate (TLS 1.3/1.2).
  - All HTTP requests automatically 301-redirected to HTTPS.
- **Backend FQDN**: `https://api.ritucast.app` (or `https://ritucast-backend-[hash]-el.a.run.app`).
  - Publicly accessible over HTTPS with strict CORS validation restricting access to `https://ritucast.app` and designated staging origins.

### Internal Runtime Zone
- **Container Isolation**: Both services run in isolated gVisor sandboxed environments (`run.googleapis.com/execution-environment: gen2`).
- **Identity & Least Privilege**:
  - Frontend Service Account: `ritucast-frontend-sa@PROJECT_ID.iam.gserviceaccount.com` (Zero Cloud API permissions).
  - Backend Service Account: `ritucast-api-sa@PROJECT_ID.iam.gserviceaccount.com` (Logging Writer permissions only).
- **Communication Path**: The browser requests static assets from the frontend; API requests can either flow directly to `api.ritucast.app` or via the frontend's NGINX reverse-proxy at `/api/*` to avoid cross-origin preflight latency on cellular networks.

---

## 3. Port and Protocol Assignments

| Service | Protocol | External Port | Container Port | Exposure | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ritucast-frontend` | HTTPS (HTTP/2) | 443 | 8080 | Public | Web application UI delivery and static assets |
| `ritucast-backend` | HTTPS (HTTP/2) | 443 | 8080 | Public (CORS-gated) | REST API endpoints, OpenAPI documentation, health probes |
| `frontend` (Docker Compose) | HTTP | 8080 | 8080 | Localhost | Local integration test frontend |
| `backend` (Docker Compose) | HTTP | 8000 | 8000 | Localhost | Local integration test backend API |

---

## 4. Storage and Artifact Topography

Ritucast does not deploy external block storage (Persistent Disks) or cloud relational databases (Cloud SQL). All operational datasets and model lookups are immutable, read-only artifacts bundled directly into the container image:

- `/app/data/processed/barind_pilot_features.parquet` (22 KB)
- `/app/data/processed/haor_pilot_features.parquet` (22 KB)
- `/app/data/sample/bangladesh_pilot_upazilas.geojson` (32 KB)

This topography guarantees:
- Sub-millisecond data access via in-memory Arrow/Pandas zero-copy reads.
- Deterministic reproducibility without risk of external database connection failures.
- Zero storage costs outside of container registry storage ($\approx \$0.02/\text{GB/month}$).
