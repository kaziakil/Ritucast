# Health Checks, Logging, and Operational Observability: Ritucast

## 1. Overview

Reliable agricultural decision support demands robust, unambiguous operational signals. This document specifies the health check, readiness probe, logging, and observability standards deployed across the Ritucast infrastructure.

---

## 2. Health and Readiness Probe Architecture

Ritucast decouples **Liveness (Health)** from **Readiness (Dependency Availability)** to enable orchestrators (Cloud Run, Docker Compose, Kubernetes) to distinguish process crashes from transient upstream data conditions (`NFR-REL-01`).

### 2.1 Backend Probes

#### Liveness Probe (`GET /health`)
- **Purpose**: Verifies that the Uvicorn event loop and FastAPI application process are alive and responding to HTTP requests.
- **Cost**: Extremely low ($<2\text{ms}$). Zero disk I/O, zero network calls.
- **Response Format**:
  ```json
  {
    "status": "healthy",
    "version": "1.0.0-phase10",
    "timestamp_utc": "2026-10-10T11:32:07.938897+00:00"
  }
  ```
- **HTTP Status**: Always `200 OK`. If the process deadlocks or crashes, the orchestrator restarts the container.

#### Readiness Probe (`GET /ready`)
- **Purpose**: Verifies that all foundational agricultural data dependencies and analytical calculation engines are initialized and ready to compute advisories.
- **Validated Subsystems**:
  1. `data_store_ready`: All 4 verified Parquet feature tables exist and are readable (`meteorology_daily_upazila.parquet`, `forecast_hourly_pilot.parquet`, `catchment_rainfall_daily.parquet`, `hydrology_river_stage.parquet`).
  2. `analytics_ready`: FAO-56 Penman-Monteith ET0, Soil Water Deficit, and Flash-Flood Hazard Index modules are imported and functional.
- **Healthy Response (`200 OK`)**:
  ```json
  {
    "status": "ready",
    "data_store_ready": true,
    "analytics_ready": true,
    "verified_datasets": [
      "meteorology_daily_upazila.parquet",
      "forecast_hourly_pilot.parquet",
      "catchment_rainfall_daily.parquet",
      "hydrology_river_stage.parquet"
    ],
    "missing_dependencies": []
  }
  ```
- **Degraded Response (`503 Service Unavailable`)**:
  ```json
  {
    "status": "degraded",
    "data_store_ready": false,
    "analytics_ready": true,
    "verified_datasets": [],
    "missing_dependencies": ["meteorology_daily_upazila.parquet"]
  }
  ```
- **Orchestrator Behavior**: When `/ready` returns `503`, Cloud Run or load balancers immediately stop routing user requests to that container instance until the readiness check passes.

### 2.2 Frontend Probes

#### Liveness Probe (`GET /health`)
- Direct NGINX synthetic endpoint returning `200 OK` with text payload `healthy\n`.
- Bypasses disk reads and upstream proxying.

---

## 3. Logging Architecture

### 3.1 Structured Logging Standards
- **Format**: JSON-compatible standard log streams written to `stdout` and `stderr`.
- **Log Levels**:
  - `INFO`: Normal operational lifecycle events (startup, shutdown, route requests).
  - `WARNING`: Handled anomalous conditions (e.g., weather observations exceeding 24 hours old, but within 36-hour limit).
  - `ERROR`: Ingestion failures, data corruption, or unhandled exceptions.
  - `CRITICAL`: System failure blocking startup.
- **Anti-Leak Policy**: Secrets, authentication headers, API keys, and end-user PII are strictly excluded from log streams.

### 3.2 Cloud Logging Integration
- In Google Cloud Run, `stdout` and `stderr` logs are automatically ingested by **Google Cloud Logging** without requiring sidecar daemons or third-party log forwarders.
- Log events are correlated by request `trace_id` for end-to-end request tracing.

---

## 4. Key Operational Metrics & Alerts

| Metric | Source | Normal Range | Alert Threshold | Remediation |
| :--- | :--- | :--- | :--- | :--- |
| **HTTP 5xx Error Rate** | Cloud Run Metrics | $< 0.1\%$ | $> 1\%$ for 5 min | Check logs for unhandled calculation exceptions |
| **Readiness Status** | Cloud Run Probes | `200 OK` | `503` for 3 probes | Verify Parquet feature file integrity |
| **P95 Latency** | Cloud Run Metrics | $< 120\text{ms}$ | $> 500\text{ms}$ | Check container CPU/memory throttling |
| **Instance Count** | Cloud Run Autoscaler | 0 to 5 | Sustained 5 | Check for traffic spike or slow queries |
