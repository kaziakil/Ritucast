# Deployment Architectural Decisions: Ritucast Agricultural Intelligence Platform

## 1. Overview

This document records the formal Architectural Decision Records (ADRs) and project governance decisions established during **Phase 13: Deployment Architecture and Production Readiness**.

---

## 2. Decision Records

### DEC-51: Containerized Decoupled Serverless Architecture with Google Cloud Run
- **Status**: Approved & Implemented
- **Date**: 2026-10-10
- **Context**: Ritucast requires a high-availability, low-latency deployment for rural Bangladesh agricultural users across two pilot testbeds (Barind Tract and Haor Basin). The platform needs to operate under budget constraints ($\le \$65/\text{month}$) while supporting irregular usage bursts around morning and evening farming decisions.
- **Decision**: Deploy Ritucast as two decoupled OCI container services (frontend NGINX, backend FastAPI) on **Google Cloud Run** in `asia-south1` (Mumbai).
- **Consequences**:
  - Scales to zero instances when idle, incurring zero compute charges outside active traffic.
  - Generous free-tier allocation (2M requests/month) keeps baseline operational hosting cost at $0.00 to $5.00/month.
  - Eliminates Kubernetes cluster overhead, node provisioning, and VM patch management.
  - Retains 100% container portability through Knative standard manifests and Docker Compose.

---

### DEC-52: Immutable In-Image Parquet Storage Over Managed External Database
- **Status**: Approved & Implemented
- **Date**: 2026-10-10
- **Context**: Ritucast operates on verified pilot testbed feature tables and administrative boundaries. Cloud relational databases (e.g., Cloud SQL PostgreSQL) cost a minimum of $30–$60/month, introduce cold-start connection latencies, and create stateful backup/migration liabilities.
- **Decision**: Package the pre-processed, scientifically validated Parquet feature tables (`barind_pilot_features.parquet`, `haor_pilot_features.parquet`) and Upazila GeoJSON polygons directly inside the backend container image (`/app/data/`).
- **Consequences**:
  - Total data footprint is $<100\text{KB}$, adding negligible size to the backend image ($<0.05\%$).
  - Zero database subscription cost and zero network hop latency for dataset queries.
  - Sub-millisecond query execution via in-memory Arrow/Pandas tables.
  - Eliminates SQL injection vulnerabilities and database connection exhaustion risks.
  - Data updates are performed through the reproducible pipeline and deployed via atomic container updates.

---

### DEC-53: NGINX Multi-Stage Frontend Container with Strict Security Headers & Reverse Proxy
- **Status**: Approved & Implemented
- **Date**: 2026-10-10
- **Context**: Budget Android smartphones in rural Bangladesh operate on 2G/3G networks with strict memory and latency limitations (`DEC-09`). The frontend requires high-efficiency compression, immutable asset caching, and strict defense-in-depth security headers.
- **Decision**: Package the production React 19 / TypeScript build inside a lightweight `nginx:alpine` container with:
  1. Gzip compression (level 6) across HTML, CSS, JS, SVG, and JSON.
  2. One-year immutable cache headers (`Cache-Control: public, max-age=31536000, immutable`) for hashed assets.
  3. Strict Content Security Policy (CSP), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`, and `Referrer-Policy: strict-origin-when-cross-origin`.
  4. NGINX reverse-proxy configuration for `/api/` routing to the backend.
- **Consequences**:
  - Gzip compresses the total production bundle to $\approx 220\text{kB}$, well below the $1.5\text{MB}$ payload ceiling.
  - Prevents clickjacking, MIME-sniffing, and inline script injection attacks.
  - Supports clean SPA client-side routing fallback (`try_files $uri $uri/ /index.html`).
