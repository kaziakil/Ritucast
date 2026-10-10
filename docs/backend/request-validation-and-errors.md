# Ritucast: Request Validation & Error Handling Architecture

## 1. Error Handling Philosophy

In accordance with `DEC-42`, Ritucast ensures that no API consumer receives unformatted error responses, raw Python tracebacks, or database error snippets.

All error responses strictly follow the immutable error envelope:
```json
{
  "status": "error",
  "code": "ERROR_CODE_STRING",
  "message": "Human-readable English description",
  "timestamp_utc": "2026-10-10T14:30:00.000000+00:00",
  "details": null
}
```

---

## 2. Standardized Error Codes & Trigger Criteria

| HTTP Status | Error Code (`code`) | Trigger Condition | Example Cause |
| :--- | :--- | :--- | :--- |
| **`400 Bad Request`** | `BAD_REQUEST_PARAMETER` | Malformed parameter value | Negative precipitation or impossible range |
| **`404 Not Found`** | `RESOURCE_NOT_FOUND` | Queried resource does not exist | Upazila outside pilot testbeds (`BD-99-99`) |
| **`422 Unprocessable Entity`** | `CONTEXT_GATING_FAILED` | `DEC-17` violation | Missing `crop` or `stage` in advisory query |
| **`422 Unprocessable Entity`** | `REQUEST_VALIDATION_ERROR` | Pydantic schema validation failure | String passed where float was expected |
| **`429 Too Many Requests`** | `RATE_LIMIT_EXCEEDED` | Request rate exceeds 60 req/min | Rapid client polling |
| **`500 Internal Server Error`** | `INTERNAL_SERVER_ERROR` | Unhandled system exception | Sanitized fallback message protecting secrets |

---

## 3. Mandatory Contextual Gating Enforcement (`DEC-17`)

Advisory requests must provide:
1. `upazila_id`: Validated against `ContextGator.VALID_PILOT_UPAZILAS`.
2. `crop`: Validated against `ContextGator.VALID_CROPS` (normalized for Boro Rice).
3. `stage`: Validated against the supported phenological growth stage list.

If any parameter is missing, `ContextGatingError` is raised by the engine and intercepted by the `context_gating_exception_handler` in [error_handlers.py](file:///Users/kazi/Projects/RITUCAST/api/middleware/error_handlers.py).

---

## 4. Input Sanitization & Security Defenses

- **Path Traversal Protection**: Upazila identifiers are strictly matched against whitelisted dictionary keys; no dynamic filesystem path lookups are performed using client input.
- **Payload Bound Checking**: Request body payloads are bounded to prevent memory exhaustion attacks.
- **Secret Masking**: The exception handlers never include environment variables, secret keys, or local filesystem paths in response payloads.

---

## 5. Related Documentation

- Architecture: [phase-10-backend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md)
- Security & Configuration: [security-and-configuration.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/security-and-configuration.md)
