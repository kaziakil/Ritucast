# Troubleshooting Failed Workflows Runbook: Ritucast

## 1. Overview

This runbook guides engineers through diagnosing, isolating, and resolving CI/CD workflow failures in GitHub Actions.

---

## 2. Common Failure Modes & Remediation

### Failure 1: Code Quality Job Fails on Flake8 Syntax Check
- **Symptom**: Step `Check Python Syntax & Critical Flake8 Rules` fails with exit code 1.
- **Cause**: Unclosed parenthesis, invalid indentation, undefined variable name (`F82`), or import syntax error.
- **Diagnosis**: Review the step log output for the specific file and line number:
  ```bash
  python3.10 -m flake8 api/ analytics/ pipelines/ tests/ --count --select=E9,F63,F7,F82 --show-source
  ```
- **Remediation**: Correct the syntax or name binding error locally and re-commit.

---

### Failure 2: Deterministic Backend Pytest Job Fails
- **Symptom**: Job `test-backend-deterministic` reports test failures.
- **Cause**: Regression in water balance calculations, schema mismatch in Pydantic models, or missing sample fixture file.
- **Diagnosis**:
  ```bash
  pytest -m "not smoke" -v --tb=short
  ```
- **Remediation**: Check if new models modified the mathematical contracts or if a test is making network calls without mocking.

---

### Failure 3: Frontend TypeScript Build Fails (`npx tsc -b`)
- **Symptom**: Step `Verify TypeScript Types` fails with `TS2322` or `TS2339`.
- **Cause**: Frontend interface in `src/types/` drifted out of sync with backend JSON schemas.
- **Diagnosis**:
  ```bash
  cd frontend && npx tsc -b
  ```
- **Remediation**: Update TypeScript types in `frontend/src/types/api.ts` to match the backend schema.

---

### Failure 4: Docker Container Build Job Fails
- **Symptom**: Job `container-verification` fails during `docker/build-push-action`.
- **Cause**: `.dockerignore` accidentally excluded a required file, or a new dependency was added to `requirements.txt` that requires additional C compilation headers.
- **Diagnosis**:
  ```bash
  docker build -t ritucast-backend:test -f deploy/docker/Dockerfile.backend .
  ```
- **Remediation**: Check layer caching and ensure all necessary source files and data directories are copied in the Dockerfile.

---

### Failure 5: Live Smoke Test Fails in `live-data-smoke.yml`
- **Symptom**: Daily cron job fails on `test_live_nasa_power_smoke` or `test_live_open_meteo_forecast_smoke`.
- **Cause**: External API outage, network firewall blocking runner, or rate-limiting.
- **Diagnosis**:
  ```bash
  pytest -m "smoke" -v
  ```
- **Remediation**: Check upstream provider status dashboards (NASA Earthdata, Open-Meteo status). If transient, no code change is required. If permanent schema change, update the ingestion adapter.
