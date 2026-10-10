# Phase 14 to Phase 15 Handoff Specification: Ritucast

## 1. Executive Summary

This handoff document formally concludes **Phase 14: CI/CD Automation and Release Management** and establishes the automated verification baseline, release standards, and quality contracts for **Phase 15**.

All CI/CD workflow definitions, test suite markings, security audits, release packaging scripts, and deployment gates have been validated and frozen.

---

## 2. Verified Phase 14 Deliverables & Automation Assets

### 2.1 Workflow Infrastructure
- **Continuous Integration (`.github/workflows/ci.yml`)**:
  - Code Quality: Flake8 syntax checks, frontend oxlint, and TypeScript compilation (`tsc -b`).
  - Deterministic Backend Testing: `pytest -m "not smoke"` generating `coverage.xml`.
  - Frontend Verification: Vitest component and journey tests + `npm run build` bundle check.
  - Security Audit: `pip-audit`, `npm audit`, and working tree secret pattern scanning.
  - Container Image Verification: Multi-stage Docker Buildx compilation check.
- **Live Upstream Smoke Monitoring (`.github/workflows/live-data-smoke.yml`)**:
  - Daily scheduled cron (02:00 UTC) probing NASA POWER and Open-Meteo live endpoints.
  - Non-blocking telemetry reporting for external provider status.
- **Continuous Delivery & Release Management (`.github/workflows/release.yml`)**:
  - Triggered by `v*.*.*` tags or workflow dispatch.
  - Generates `ritucast-${TAG}.tar.gz` and extracts canonical `openapi.json`.
  - Builds and pushes tagged container images to Google Artifact Registry.
  - Production deployment gate requiring manual approver review.

### 2.2 Project Configuration & Test Assets
- `pytest.ini`: Explicit mark registration for `smoke`, `integration`, and `unit`.
- `.flake8`: Configured line length (120) and critical syntax rule filters.
- `CHANGELOG.md`: Standard Keep a Changelog document tracking release `v1.0.0`.
- 11 CI/CD specifications under `docs/ci-cd/` and 5 release specifications under `docs/releases/`.

---

## 3. Operational Guarantees & Contracts Frozen for Phase 15

Phase 15 must preserve the following operational and CI/CD invariants:

1. **Deterministic Test Isolation (`DEC-48`, `DEC-54`)**:
   - Any new test added in Phase 15 that requires an active internet connection must be marked `@pytest.mark.smoke`.
   - Routine regression tests must execute offline against `data/sample/` fixtures or mocks in $<10\text{ seconds}$.
2. **Quality Gate Pass Requirement**:
   - All proposed PRs must pass `ci.yml` before merging to `main`.
   - TypeScript must compile with zero errors (`tsc -b`).
   - Frontend bundle payload must stay within the $1.5\text{MB}$ `DEC-09` ceiling.
3. **Semantic Versioning & Release SOP**:
   - All version increments must follow SemVer 2.0.0 guidelines documented in [versioning-strategy.md](file:///Users/kazi/Projects/RITUCAST/docs/releases/versioning-strategy.md).
   - Release notes must be added to [CHANGELOG.md](file:///Users/kazi/Projects/RITUCAST/CHANGELOG.md).
4. **Approval Gate for Production**:
   - Production deployments can never occur automatically from unreviewed commits; manual sign-off in the GitHub Actions `production` environment is required.

---

## 4. Next Steps for Phase 15

Phase 15 will proceed in strict accordance with project governance.
**Do not execute Phase 15 until the user explicitly issues the Phase 15 directive.**
