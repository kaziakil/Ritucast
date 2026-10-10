# End-to-End Test Guide — Ritucast System Testing

## 1. Prerequisites and Environment Setup

To execute the complete end-to-end test suite for Ritucast, ensure your environment meets the following baseline:

- **Python**: 3.10+ with `pytest`, `httpx`, `fastapi`, `pydantic`, `pyarrow`, `pandas`, `requests`.
- **Node.js**: v18+ with `npm` (tested with Node 20 / 22).
- **Workspace**: Root directory `/Users/kazi/Projects/RITUCAST`.

---

## 2. Test Execution Commands

### 2.1 Backend System Integration Tests
To run the automated Python end-to-end integration test suite:
```bash
python3.10 -m pytest tests/integration/test_system_e2e.py -v
```
*Expected Result*: 7 passed in ~0.8s.

### 2.2 Live-Source Smoke Tests
To run live external API smoke tests against upstream Open-Meteo and NASA POWER services:
```bash
python3.10 -m pytest tests/integration/test_live_smoke.py -v
```
*Expected Result*: 2 passed in ~2.2s (or gracefully skipped if offline).

### 2.3 Full Backend Test Suite
To run all 95 backend unit, API, model, pipeline, and integration tests:
```bash
python3.10 -m pytest tests/ -q
```
*Expected Result*: `95 passed, 3 warnings in ~6.5s`.

### 2.4 Frontend Integration and Component Tests
To run all 17 frontend Vitest tests:
```bash
cd frontend
npm run test
```
*Expected Result*: `8 passed (8 test files), 17 passed (17 tests) in ~2.6s`.

### 2.5 Frontend Production Build & TypeScript Verification
To verify TypeScript types and production bundle generation:
```bash
cd frontend
npm run build
```
*Expected Result*: `tsc -b && vite build` completes in <250ms with 0 errors.

---

## 3. Running the Integrated Full-Stack System Locally

To verify live browser interactions between frontend and backend:

1. **Start Backend API** (Terminal 1):
   ```bash
   python3.10 -m uvicorn api.main:app --host 127.0.0.1 --port 8000
   ```
2. **Start Frontend Dev Server** (Terminal 2):
   ```bash
   cd frontend
   npm run dev -- --host 127.0.0.1 --port 3000
   ```
3. **Open Browser**:
   Navigate to `http://127.0.0.1:3000`. Vite automatically proxies requests starting with `/api/v1` to `http://127.0.0.1:8000`.
