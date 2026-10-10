# Structured Logging & Error Tracking Runbook — Ritucast

## 1. Overview & Logging Philosophy

Logging in **Ritucast** serves two critical functions:
1. **Operational Observability**: Enabling rapid diagnosis of request latencies, network timeouts, and data pipeline disruptions.
2. **Auditability & Epistemic Accountability**: Tracking advisory evaluations, rule firings, and automated suppressions without exposing smallholder personal data or private credentials.

To support automated ingestion by Google Cloud Logging, Grafana Loki, or Datadog, all application logs are emitted as newline-delimited **Structured JSON** to standard output (`stdout`/`stderr`).

---

## 2. Structured JSON Log Schema

Every log entry formatted by [`StructuredJsonFormatter`](file:///Users/kazi/Projects/RITUCAST/api/logging_config.py) adheres to the standard schema:

```json
{
  "timestamp_utc": "2026-10-10T18:45:05.693378+00:00",
  "level": "INFO",
  "logger": "ritucast.api.access",
  "message": "GET /api/v1/advisories?upazila_id=BD-50-20-30&crop=boro_rice&stage=Tillering -> 200 (14.2ms)",
  "correlation_id": "req_5e632db1a713",
  "method": "GET",
  "path": "/api/v1/advisories",
  "http_status": 200,
  "duration_ms": 14.2,
  "client_ip": "192.168.1.50"
}
```

### 2.1 Field Definitions

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `timestamp_utc` | `string` (ISO-8601) | Precise timestamp in UTC when the log event was generated. |
| `level` | `string` | Log severity level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`). |
| `logger` | `string` | Hierarchical Python logger name (e.g., `ritucast.api.access`, `ritucast.pipeline`). |
| `message` | `string` | Human-readable event description. |
| `correlation_id` | `string` | Unique request tracking token matching the HTTP `X-Correlation-ID` header. |
| `duration_ms` | `float` (Optional) | Execution latency in milliseconds. |
| `http_status` | `integer` (Optional) | HTTP status code returned to the client. |
| `exception` | `string` (Optional) | Sanitized Python traceback (included only on `ERROR` and `CRITICAL`). |

---

## 3. Correlation ID Tracking & Propagation

1. **Request Interception**: The [`StructuredLoggingMiddleware`](file:///Users/kazi/Projects/RITUCAST/api/middleware/logging.py) intercepts incoming HTTP requests.
2. **Header Extraction**: If the client provides an `X-Correlation-ID` or `X-Request-ID` header, that token is preserved. If missing, an ID in the format `req_<hex12>` is generated.
3. **Async Context Propagation**: The ID is stored in a Python `ContextVar` (`correlation_id_ctx`) so that all logging statements within the async call stack automatically inherit the same identifier.
4. **Response Injection**: The response header `X-Correlation-ID` is returned to the client, allowing mobile users or SAAOs reporting issues to quote the exact correlation ID for debugging.

---

## 4. Sensitive Data Scrubbing & Privacy Redaction

To adhere to the Zero-PII policy (`DEC-60`) and prevent accidental credential exposure:
1. **Key Pattern Matching**: Any dictionary or JSON key matching `password`, `token`, `secret`, `authorization`, `api_key`, `bearer`, or `private` is automatically replaced with `[REDACTED]`.
2. **Header Sanitization**: Authorization headers and session tokens are stripped prior to access logging.
3. **No PII Stored**: Farmer names, mobile numbers, and parcel-level GPS coordinates are never accepted by the API or logged to standard output.

---

## 5. Log Levels & Error Classification

| Log Level | Usage Criteria | Example Event |
| :--- | :--- | :--- |
| **`DEBUG`** | Verbose diagnostic information; disabled in production by default. | Raw Parquet partition scan duration; mathematical intermediate values. |
| **`INFO`** | Normal operational events; HTTP access records (excluding `/health`). | `GET /api/v1/advisories -> 200 (14.2ms)`. |
| **`WARNING`** | Handled business validation errors or degraded conditions. | Client sent invalid Upazila ID (404); dataset is $>30\text{h}$ old; client rate limit approaching. |
| **`ERROR`** | Unexpected application failures requiring engineering investigation. | Unhandled 500 internal server error; corrupted Parquet file encountered. |
| **`CRITICAL`** | System-wide failures halting advisory service. | All Parquet tables missing; disk out of space; memory allocation failure. |

---

## 6. How to Inspect Logs

### 6.1 Local Development & Docker Compose
```bash
# View live structured logs from local container
docker compose logs -f backend | jq .

# Filter logs by correlation ID
docker compose logs backend | grep "req_5e632db1a713" | jq .

# Filter errors only
docker compose logs backend | jq 'select(.level=="ERROR")'
```

### 6.2 Google Cloud Run (Production)
```bash
# Stream production logs in Google Cloud CLI
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=ritucast-backend" \
  --limit=50 \
  --format="json"

# Search for specific correlation ID in Google Cloud Logging
gcloud logging read 'jsonPayload.correlation_id="req_5e632db1a713"' --limit=10
```
