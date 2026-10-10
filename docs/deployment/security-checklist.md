# Security Checklist & Threat Model: Ritucast Agricultural Intelligence Platform

## 1. Overview

Ritucast provides mission-critical agronomic advice to rural smallholder farmers. Erroneous advisories or unauthorized tampering could result in irreversible crop loss (e.g., missed flash-flood evacuations or severe drought desiccation).

This document establishes the security architecture, threat model, and pre-deployment security verification checklist.

---

## 2. Threat Modeling & Risk Mitigation

| Threat Vector | Attack Scenario | Implemented Mitigation | Verification |
| :--- | :--- | :--- | :--- |
| **Tampered Advisories** | Attacker injects malicious advice (e.g., false flood clear). | Immutable container deployment; read-only application root; no mutable database records. | Validated in container build tests. |
| **Credential Exfiltration** | Attacker searches source code or bundles for API secrets. | Zero-secret architecture; no credentials in git or frontend JS (`.env.production.example`). | Validated by secret grep audit. |
| **Denial of Service (DoS)** | Attacker floods compute-intensive Penman-Monteith calculations. | Cloud Run concurrency limits (80 requests/container, max 5 instances); deterministic math runtime ($<5\text{ms}$). | Enforced in `service-backend.yaml`. |
| **Cross-Origin Hijacking** | Malicious third-party website queries backend API. | Strict CORS middleware rejecting all origins except `https://ritucast.app`. | Tested in `tests/test_api_integration.py`. |
| **Container Escape / Privilege Escalation** | Attacker exploits Linux kernel vulnerability to gain host root. | Backend runs as non-root `ritucast` (UID 10001); Cloud Run enforces gVisor kernel sandbox. | Enforced in Dockerfiles. |
| **XSS / Clickjacking** | Attacker embeds Ritucast in an iframe or injects scripts. | NGINX headers: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, strict CSP. | Verified via curl probe test. |

---

## 3. Pre-Deployment Security Checklist

- [x] **Zero Hardcoded Secrets**: Scanned repository history and working tree for private keys, AWS/GCP credentials, database passwords, and tokens.
- [x] **No Secrets in Frontend Bundle**: Verified that `import.meta.env` references only `VITE_API_BASE_URL`.
- [x] **Non-Root Execution**: Verified backend Docker container executes under unprivileged UID `10001` (`ritucast`).
- [x] **Minimal Base Images**: Utilized Debian slim and Alpine Linux base images to eliminate unnecessary shell utilities and compilers.
- [x] **Safe Error Responses**: Verified that production API returns sanitized error messages without exposing Python stack traces or internal server paths.
- [x] **Strict CORS Policy**: Production environment rejects wildcards (`*`) and validates origins against configured domains.
- [x] **HTTP Security Headers**: Verified NGINX serves `Content-Security-Policy`, `X-Frame-Options: DENY`, and `X-Content-Type-Options: nosniff`.
- [x] **Dependency Audit**: Verified Python and npm dependencies using automated security tooling.
