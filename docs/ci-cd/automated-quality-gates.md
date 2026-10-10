# Automated Quality Gates & Acceptance Criteria: Ritucast

## 1. Overview

Quality gates in Ritucast serve as automated checkpoints that prevent substandard code, broken interfaces, or security flaws from reaching staging and production environments.

---

## 2. Quality Gate Inventory

| Gate Identifier | Check Description | Tool & Command | Target Threshold | Blocking Status |
| :--- | :--- | :--- | :--- | :--- |
| **QG-CI-01** | **Python Syntax & Name Binding** | `flake8 --select=E9,F63,F7,F82` | **0 errors** | **BLOCKING** |
| **QG-CI-02** | **Frontend Code Quality** | `npm run lint` (`oxlint`) | **0 errors** | **BLOCKING** |
| **QG-CI-03** | **TypeScript Type Checking** | `npx tsc -b` | **0 errors** | **BLOCKING** |
| **QG-CI-04** | **Backend Pytest Deterministic Suite**| `pytest -m "not smoke"` | **100% Pass (0 failures)** | **BLOCKING** |
| **QG-CI-05** | **Frontend Vitest Test Suite** | `npm run test` (`vitest run`) | **100% Pass (0 failures)** | **BLOCKING** |
| **QG-CI-06** | **Frontend Production Build** | `npm run build` | **0 errors, bundle $\le 1.5\text{MB}$** | **BLOCKING** |
| **QG-CI-07** | **Zero Hardcoded Secrets** | Git working tree grep audit | **0 private keys/tokens** | **BLOCKING** |
| **QG-CI-08** | **High-Severity npm Vulnerabilities** | `npm audit --audit-level=high` | **0 high/critical** | **BLOCKING** |
| **QG-CI-09** | **Python Dependency Security Audit** | `pip-audit -r requirements.txt` | Known advisories flagged | **NON-BLOCKING (Warning)** |
| **QG-CI-10** | **Backend Container Image Build** | Docker Buildx `Dockerfile.backend` | **Exit code 0** | **BLOCKING** |
| **QG-CI-11** | **Frontend Container Image Build** | Docker Buildx `Dockerfile.frontend` | **Exit code 0** | **BLOCKING** |
| **QG-CI-12** | **OpenAPI Schema Extraction** | Python ASGI introspection | **Valid OpenAPI 3.0 JSON** | **BLOCKING (Release)** |

---

## 3. Quality Gate Verification Evidence

During Phase 14 validation, all quality gates were empirically tested against the local repository:

```text
[QG-CI-01] flake8 --select=E9,F63,F7,F82: 0 errors detected.
[QG-CI-02] oxlint: 0 errors detected across 22 frontend files.
[QG-CI-03] tsc -b: TypeScript compilation succeeded with zero type errors.
[QG-CI-04] pytest -m "not smoke": 93 passed, 2 deselected in 4.36s.
[QG-CI-05] vitest run: 17 passed across 8 test suites in 2.23s.
[QG-CI-06] npm run build: Production build succeeded; bundle wire size 220.65 kB.
[QG-CI-07] Secret scan: Zero private keys found in codebase.
[QG-CI-08] npm audit: Found 0 vulnerabilities.
[QG-CI-10] Docker backend build: Exit code 0, non-root user 10001 confirmed.
[QG-CI-11] Docker frontend build: Exit code 0, NGINX Alpine headers confirmed.
[QG-CI-12] OpenAPI introspection: 13 endpoints extracted to JSON.
```
