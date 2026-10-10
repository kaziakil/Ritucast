# Containerization Architecture & Specifications: Ritucast

## 1. Overview

Ritucast utilizes standard Open Container Initiative (OCI) images to deliver reproducible, secure, and lightweight application runtimes across both local and production cloud environments.

Container configurations follow the principle of least privilege, multi-stage artifact compilation, and non-root execution.

---

## 2. Backend Container Specification (`deploy/docker/Dockerfile.backend`)

### Multi-Stage Build Architecture
1. **Stage 1 (`builder`)**:
   - Base image: `python:3.10-slim-bookworm`
   - Purpose: Installs compilation toolchains (`build-essential`, `gcc`), upgrades `pip`, and builds wheels for numerical dependencies (`numpy`, `pandas`, `pyarrow`, `scipy`) into a separate `/install` root.
2. **Stage 2 (`runtime`)**:
   - Base image: `python:3.10-slim-bookworm` (clean, unbloated)
   - Copies `/install` packages to `/usr/local`.
   - Copies only necessary source directories: `api/`, `analytics/`, `pipelines/`, `data/processed/`, and `data/sample/`.
   - Creates unprivileged system user `ritucast` (UID: 10001, GID: 10001).
   - Injects native Python healthcheck probe.
   - Launches `uvicorn` using dynamic `$PORT` expansion.

### Container Security Features
- **Non-Root Execution**: Runs strictly under unprivileged user `ritucast` (UID 10001).
- **Minimal Attack Surface**: Build dependencies (`gcc`, `make`, build headers) are completely discarded from the final runtime image.
- **Strict `.dockerignore`**: Excludes `.git`, `.venv`, test caches, `.env` secrets, node modules, and raw interim geospatial data.
- **Read-Only Data Mounts**: Parquet and GeoJSON files are owned by `ritucast` with read-only permissions in production.

---

## 3. Frontend Container Specification (`deploy/docker/Dockerfile.frontend`)

### Multi-Stage Build Architecture
1. **Stage 1 (`builder`)**:
   - Base image: `node:20-alpine`
   - Uses `npm ci` for deterministic lockfile resolution.
   - Injects `VITE_API_BASE_URL` at compile time.
   - Executes `npm run build` (`tsc -b && vite build`) to generate static assets in `/app/dist`.
2. **Stage 2 (`runtime`)**:
   - Base image: `nginx:alpine` ($<45\text{MB}$ total image size).
   - Copies `/app/dist` static assets to `/usr/share/nginx/html`.
   - Installs hardened `nginx.conf` listening on both port 80 and port 8080.
   - Configures Gzip compression and strict CSP/HSTS/X-Frame-Options headers.

---

## 4. Local Multi-Service Orchestration (`docker-compose.yml`)

The root `docker-compose.yml` provides a unified developer and staging environment:

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: deploy/docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
      - PORT=8000
      - CORS_ORIGINS=["http://localhost:8080","http://localhost:5173"]

  frontend:
    build:
      context: .
      dockerfile: deploy/docker/Dockerfile.frontend
      args:
        - VITE_API_BASE_URL=http://localhost:8000
    ports:
      - "8080:8080"
    depends_on:
      backend:
        condition: service_healthy
```

Both containers spin up with automated health synchronization and zero manual configuration.
