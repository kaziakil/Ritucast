# Frontend Local Development & Execution Guide

## 1. Prerequisites

- **Node.js**: v18.0.0+ (Tested on Node.js v20+).
- **Package Manager**: `npm` (v9+).
- **Backend API**: Python 3.10+ FastAPI server running on `http://localhost:8000`.

---

## 2. Quickstart Execution

### Step 1: Start Backend API (Terminal 1)
From the project root:
```bash
python3.10 -m uvicorn ritucast.api.main:app --host 0.0.0.0 --port 8000 --reload
```
Verify the backend responds at `http://localhost:8000/health`.

### Step 2: Start Frontend Application (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
The Vite development server starts at `http://localhost:3000`.
Requests to `/api`, `/health`, and `/ready` are automatically reverse-proxied to `http://localhost:8000`.

---

## 3. Scripts Catalog

| Script | Command | Purpose |
| :--- | :--- | :--- |
| `dev` | `npm run dev` | Starts Vite HMR dev server on port 3000. |
| `build` | `npm run build` | Compiles TypeScript (`tsc -b`) and generates production bundle in `dist/`. |
| `test` | `npm run test` | Runs all 14 Vitest unit and integration tests. |
| `lint` | `npm run lint` | Runs `oxlint` for fast static code analysis. |
| `preview` | `npm run preview` | Previews the local production build in `dist/`. |

---

## 4. Environment Variables

Create `.env` in `frontend/` if custom API configurations are required:
```env
VITE_API_BASE_URL=http://localhost:8000
```
In development mode, leaving `VITE_API_BASE_URL` empty defaults to relative root `/`, which routes seamlessly through Vite's dev proxy without triggering CORS issues.
