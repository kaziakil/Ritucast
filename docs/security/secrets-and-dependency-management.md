# Secrets and Software Supply-Chain Security — Ritucast

## 1. Overview

This document specifies Ritucast's secret management standards, software supply-chain controls, dependency vulnerability tracking, and container image hardening.

---

## 2. Secret & Credential Hygiene Policies

Ritucast enforces a strict zero-credential-in-repository policy:

### 2.1 Version Control Safeguards
1. **No `.env` Commits**: All local `.env` and `.env.local` files are ignored in [`.gitignore`](file:///Users/kazi/Projects/RITUCAST/.gitignore).
2. **Template Sanitization**: Only [`.env.example`](file:///Users/kazi/Projects/RITUCAST/.env.example) and [`.env.production.example`](file:///Users/kazi/Projects/RITUCAST/.env.production.example) are checked in, containing placeholder values and documentation comments only.
3. **No Private Keys**: Automated pattern scanning verifies zero `.pem`, `.key`, or RSA private keys in the Git working tree.

### 2.2 CI/CD Least-Privilege Credentials (`DEC-56`)
Workflows in [`.github/workflows/`](file:///Users/kazi/Projects/RITUCAST/.github/workflows) enforce granular permissions:
- Continuous Integration ([`.github/workflows/ci.yml`](file:///Users/kazi/Projects/RITUCAST/.github/workflows/ci.yml)):
  ```yaml
  permissions:
    contents: read
  ```
  Runs validation tests without access to production deployment secrets.
- Production Release ([`.github/workflows/release.yml`](file:///Users/kazi/Projects/RITUCAST/.github/workflows/release.yml)):
  Deployment jobs require the `production` GitHub Environment, triggering mandatory human approval gates before accessing GCP workload identity tokens.

---

## 3. Dependency Vulnerability Analysis

### 3.1 Python Dependencies ([`requirements.txt`](file:///Users/kazi/Projects/RITUCAST/requirements.txt))
Audited with `pip-audit` against the Python Packaging Advisory Database (PyPA):

| Package | Resolved Version | Advisory ID | Summary | Reachability & Exploitability Analysis |
| :--- | :--- | :--- | :--- | :--- |
| `starlette` | `0.46.2` | `PYSEC-2026-1941`<br>`PYSEC-2026-1942` | Multipart boundary parsing denial of service | **Unreachable**: Ritucast does not expose file upload endpoints. All endpoints accept JSON only. |
| `starlette` | `0.46.2` | `PYSEC-2026-161` | WebSocket frame memory exhaustion | **Unreachable**: Ritucast does not use WebSockets. |
| `starlette` | `0.46.2` | `PYSEC-2026-2281` | Static file Range header DoS | **Unreachable**: Backend does not serve static files; NGINX serves all static assets directly. |

*Conclusion*: Starlette transitive CVEs do not impact the active application surface. Pinned minor bounds on FastAPI (`fastapi>=0.111.0,<0.116.0`) will be updated when FastAPI releases a patched minor version.

### 3.2 Frontend Dependencies ([`frontend/package.json`](file:///Users/kazi/Projects/RITUCAST/frontend/package.json))
Audited with `npm audit`:
- **Result**: `found 0 vulnerabilities`.
- Lockfile integrity enforced via `package-lock.json`.

---

## 4. Container Image Hardening

Both production containers follow defense-in-depth hardening practices:

### 4.1 Backend Container ([`deploy/docker/Dockerfile.backend`](file:///Users/kazi/Projects/RITUCAST/deploy/docker/Dockerfile.backend))
1. **Base Image**: `python:3.10-slim` (minimal operating system footprint).
2. **Multi-Stage Build**: Wheel compilation occurs in builder stage; production image excludes compilers and build tools (`gcc`, `build-essential`).
3. **Non-Root Execution**:
   ```dockerfile
   RUN groupadd -g 10001 appgroup && \
       useradd -u 10001 -g appgroup -s /sbin/nologin -M appuser
   USER 10001:10001
   ```
4. **Read-Only Code**: Application source in `/app` is owned by `root:root` with read-only permissions for `appuser`.
5. **Pre-Packaged Data Architecture (`DEC-52`)**: Feature tables reside inside `/app/data/processed/` ($<110\text{KB}$ total), eliminating runtime download dependencies.

### 4.2 Frontend Gateway Container ([`deploy/docker/Dockerfile.frontend`](file:///Users/kazi/Projects/RITUCAST/deploy/docker/Dockerfile.frontend))
1. **Base Image**: `nginx:1.25-alpine` (lightweight, minimal attack surface).
2. **Dropped Privileges**: Runs with unprivileged worker processes; root directory `/usr/share/nginx/html` is immutable at runtime.

---

## 5. Software Supply-Chain Verification Tools

Automated verification is integrated into CI:
- **`pip-audit`**: Runs as part of `security-audit` job in [`.github/workflows/ci.yml`](file:///Users/kazi/Projects/RITUCAST/.github/workflows/ci.yml).
- **`npm audit`**: Enforced on every pull request and push to `main`.
- **`flake8`**: Enforces Python syntax and code safety standards ([`.flake8`](file:///Users/kazi/Projects/RITUCAST/.flake8)).

Related documentation:
- [`docs/security/api-security.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/api-security.md)
- [`docs/security/secure-configuration.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/secure-configuration.md)
- [`docs/ci-cd/security-scanning.md`](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/security-scanning.md)
