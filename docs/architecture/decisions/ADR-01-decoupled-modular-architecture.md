# ADR-01: Adoption of Decoupled Containerized Modular Architecture

## 1. Status
**Approved** (2026-10-10)

## 2. Context
Ritucast requires a software architecture that supports compute-heavy geospatial data processing (satellite raster manipulation, coordinate transformations, hydrological modeling) while simultaneously serving an ultra-responsive, lightweight ($<1.5\text{MB}$) mobile web application to rural extension workers and farmers operating over volatile 3G networks in Bangladesh.

We evaluated four candidate topologies:
1. *Monolithic Server-Rendered Application* (Django / Rails).
2. *Microservices Mesh* (Kubernetes / Istio).
3. *Pure Serverless Functions* (AWS Lambda / Cloud Functions).
4. *Decoupled Modular Architecture* (Containerized Async REST API + Background Geospatial Workers + PostGIS/Redis + Static PWA Client).

## 3. Decision
We formally adopt the **Decoupled Modular Architecture**:
- A static, offline-capable Progressive Web App (PWA) client built in React/TypeScript, distributed globally via edge Cloud CDN.
- An asynchronous REST API service built in Python with FastAPI, running in lightweight containers on Google Cloud Run.
- Specialized background ingestion and geospatial workers running Celery/Redis tasks for heavy raster manipulation.
- A unified spatial persistence and caching tier powered by PostgreSQL 16 with PostGIS 3.4 and Redis 7.

## 4. Rationale & Trade-Offs
- **Heavy Geospatial Isolation**: Heavy C-libraries (GDAL, Rasterio, GEOS) are confined to background worker containers, keeping the web API container lean and fast ($<150\text{MB}$ image).
- **Mobile Performance**: Distributing the PWA via edge CDN ensures instant App Shell loading even on throttled 3G connections, without server-rendering latency.
- **Operational Simplicity**: Avoids the crushing orchestration complexity, network latency hops, and high costs ($\ge \$400/\text{mo}$) of a Kubernetes microservices mesh during the pilot phase.
- **Cost Efficiency**: Serverless containers (Cloud Run) auto-scale to zero during nighttime low-traffic hours, maintaining pilot operating costs under $\$65/\text{month}$.

## 5. Revisit Triggers
This decision will be revisited if:
- Simultaneous active concurrent users exceed $50,000$, justifying dedicated Kubernetes clusters.
- Nationwide expansion (all 64 districts) introduces regional data sovereignty requirements.
