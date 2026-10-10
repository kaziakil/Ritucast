# Phase 13 Deployment Architecture: Ritucast Agricultural Intelligence Platform

## 1. Executive Summary

This document specifies the deployment architecture for **Ritucast**, an agricultural intelligence and decision-support platform designed to transform satellite observations, numerical weather predictions, and soil-moisture data into localized, actionable, and explainable farming advice for smallholders and extension workers in Bangladesh.

The deployment architecture is engineered to satisfy the dual operational requirements of Ritucast:
1. **Pilot Focus**: Zero-cost, high-reliability serverless hosting across the two designated testbeds:
   - **High Barind Tract** (Rajshahi Division: Godagari, Tanore Upazilas) for drought monitoring, groundwater deficit, and irrigation scheduling.
   - **Haor Basin** (Sylhet Division: Sunamganj Sadar, Tahirpur Upazilas) for pre-monsoon transboundary flash floods and early harvest alerts.
2. **Client Hardware Budget (`DEC-09`, `ADR-07`)**: Rural target users operating budget Android smartphones (2GB–3GB RAM, Android 8+) on variable 2G/3G cellular networks, requiring bundle sizes $\le 1.5\text{MB}$, TTI $\le 3.5\text{s}$, and client heap memory $\le 45\text{MB}$.

---

## 2. Selected Platform Architecture

Ritucast adopts a **Containerized Decoupled Serverless Architecture** deployed to **Google Cloud Run (asia-south1, Mumbai)**:

```
[ Rural User Browser / Budget Smartphone (3G) ]
                      │
                      ▼ HTTPS (TLS 1.3, HTTP/2)
┌─────────────────────────────────────────────────────────────┐
│  Google Cloud Run (asia-south1)                             │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ ritucast-frontend (NGINX Alpine Container)            │  │
│  │ - Static SPA Asset Hosting (Vite React + TS)          │  │
│  │ - Security Headers (CSP, HSTS, X-Frame-Options)       │  │
│  │ - Immutable Asset Caching (1 Year)                    │  │
│  │ - Reverse Proxy /api/* to Backend                     │  │
│  └──────────────────────────┬────────────────────────────┘  │
│                             │ Internal / Encrypted VPC      │
│                             ▼                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ ritucast-backend (FastAPI / Uvicorn Container)        │  │
│  │ - Python 3.10 Non-Root User (UID 10001)               │  │
│  │ - Bundled Parquet Datasets (<100KB, Zero Cold Start)  │  │
│  │ - FAO-56 Penman-Monteith ET0 Engine                   │  │
│  │ - Soil Water Balance & Flash-Flood Hazard Index       │  │
│  │ - 4-Tier Taxonomy & Decision-Gating (DEC-08, DEC-17)  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Key Architectural Rationale
1. **Zero Database Requirement**: The application analytics layer operates deterministically on curated Parquet feature tables and GeoJSON pilot boundaries totaling $<100\text{KB}$. Storing these directly within the backend container eliminates database provisioning costs, connection-pool latency, and database maintenance overhead.
2. **Scale-to-Zero Efficiency**: Both frontend and backend containers scale to zero when idle (`minScale: 0`), resulting in negligible operational cost during periods between morning/evening advisory access windows ($\approx \$0.00$ to $\$5.00/\text{month}$).
3. **Geographic Proximity**: Deploying to `asia-south1` (Mumbai) ensures low round-trip latency ($\approx 35\text{ms} - 55\text{ms}$) to Bangladesh cellular networks (Grameenphone, Banglalink, Robi, Teletalk).
4. **Standardized Container Contract**: Standard OCI containers ensure 100% portability. The exact same container images run locally via `docker-compose.yml`, on VM instances via Docker, or across any standard Kubernetes/Knative cluster without code changes.

---

## 3. Component Architecture

| Component | Technology | Runtime Specs | Scaling Parameters | Primary Role |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend** | React 19, Vite, TypeScript, NGINX Alpine | 1 vCPU, 256MB RAM | 0 to 5 instances, Concurrency: 80 | Static single-page application delivery, gzip compression, security header injection, client routing fallback. |
| **Backend** | FastAPI, Uvicorn, Python 3.10-slim | 1 vCPU, 1024MB RAM | 0 to 5 instances, Concurrency: 80 | RESTful API, agronomic calculation engine, health/readiness probes, Parquet data access layer. |
| **Local Proxy / Compose** | Docker Compose v2 | Local Docker daemon | 1 frontend, 1 backend | Local integration testing, offline demonstration, reproducible development runtime. |
| **CI/CD** | GitHub Actions | Ubuntu Latest | On-demand workflow | Automated test gates (pytest, vitest), bundle size enforcement, container build verification, automated Cloud Run deploy. |

---

## 4. Architectural Invariants and Safety Gates

All deployment artifacts enforce the governed architectural decisions of Ritucast:
- **`DEC-06` Non-Goals Preservation**: No parcel-level yield models, no automated chemical diagnosis, no remote actuator hardware connections.
- **`DEC-08` Information Taxonomy**: 4-tier visual and data model separation (Empirical Observations, Derived Agronomic Indicators, Probabilistic Predictions, Actionable Recommendations) maintained across API responses.
- **`DEC-09` Client Budgets**: Production JS bundle ($199.3\text{kB}$ gzip) and CSS ($20.7\text{kB}$ gzip) are well within the $1.5\text{MB}$ budget; total static assets compress to $\approx 220\text{kB}$.
- **`DEC-10` Automated Suppression**: In physical anomaly or ensemble spread ($>50\%$), the backend automatically flags advisories as suppressed.
- **`DEC-17` Contextual Gating**: Every advisory endpoint enforces valid Upazila, Crop (`boro_rice`), and active Growth Stage before generating recommendations.
