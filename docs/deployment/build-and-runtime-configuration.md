# Build and Runtime Configuration: Ritucast Agricultural Intelligence Platform

## 1. Overview

This document provides the canonical build, packaging, and startup instructions for Ritucast backend and frontend services.

---

## 2. Backend Service (FastAPI)

### Runtime Specifications
- **Python Version**: 3.10.x
- **Framework**: FastAPI 0.115+, Starlette, Uvicorn 0.34+
- **System User**: `ritucast` (UID 10001, GID 10001, non-root)
- **Default Port**: 8000 (Local) / 8080 (Cloud Run container via dynamic `$PORT`)

### Build Procedure
```bash
# 1. Local environment setup
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 2. Container Image Build
docker build -t ritucast-backend:latest -f deploy/docker/Dockerfile.backend .
```

### Startup Commands
```bash
# Local development (with auto-reload)
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Container / Production execution
# Note: $PORT dynamically defaults to 8080 if not set by runtime environment
uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1 --proxy-headers
```

### Critical Environment Settings
| Variable | Production Value | Development Value | Description |
| :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | `production` | `development` | Operating mode |
| `DEBUG` | `false` | `true` | Suppresses verbose stack traces |
| `PORT` | `8080` | `8000` | HTTP listening port |
| `CORS_ORIGINS` | `["https://ritucast.app"]` | `["http://localhost:5173"]`| Permitted origins (JSON array) |
| `MAX_WEATHER_AGE_HOURS` | `36.0` | `36.0` | Ingestion staleness threshold (DEC-10) |
| `DEFAULT_DANGER_LEVEL_M` | `8.25` | `8.25` | Tahirpur flood danger mark (DEC-38) |

---

## 3. Frontend Service (Vite React SPA)

### Runtime Specifications
- **Node.js Build Version**: 20.x Alpine
- **Runtime Host**: NGINX 1.25+ Alpine
- **Bundler**: Vite 6.x
- **UI Framework**: React 19.x, TypeScript 5.8x

### Build Procedure
```bash
# 1. Local development build
cd frontend
npm ci
npm run build

# 2. Container Multi-Stage Build
docker build \
  --build-arg VITE_API_BASE_URL="https://api.ritucast.app" \
  -t ritucast-frontend:latest \
  -f deploy/docker/Dockerfile.frontend .
```

### Startup Commands
```bash
# Local Vite dev server
cd frontend && npm run dev -- --host

# Container runtime (NGINX Alpine)
nginx -g 'daemon off;'
```

### Bundle Size Output Verification
The production build produces:
- `dist/index.html`: $1.39\text{kB}$ ($0.66\text{kB}$ gzip)
- `dist/assets/index-[hash].css`: $130.34\text{kB}$ ($20.69\text{kB}$ gzip)
- `dist/assets/index-[hash].js`: $637.38\text{kB}$ ($199.30\text{kB}$ gzip)
Total gzipped payload across the wire: $\approx 220.65\text{kB}$ ($<15\%$ of the $1.5\text{MB}$ `DEC-09` ceiling).
