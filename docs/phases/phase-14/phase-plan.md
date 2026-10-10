# Phase 14 Plan: CI/CD Automation and Release Management

## 1. Objectives & Scope

Phase 14 establishes an automated, reproducible, and secure continuous integration and delivery architecture for Ritucast, coupled with formal release management and versioning standards.

### In Scope
- Baseline review of Phases 1–13 codebases, dependencies, test passes, and deployment configurations.
- Design and implementation of GitHub Actions continuous integration workflow (`.github/workflows/ci.yml`).
- Separation of deterministic test suites (`pytest -m "not smoke"`) from live external provider smoke tests (`pytest -m "smoke"`).
- Implementation of scheduled and on-demand live data smoke testing workflow (`.github/workflows/live-data-smoke.yml`).
- Design and implementation of release packaging and approval-gated delivery workflow (`.github/workflows/release.yml`).
- Implementation of `pytest.ini` with explicit test markers (`smoke`, `integration`, `unit`).
- Implementation of `.flake8` configuration and integration of code quality checks (`flake8`, `oxlint`, `tsc -b`).
- Implementation of dependency and secret vulnerability scanning (`pip-audit`, `npm audit`, private key pattern matching).
- Formalization of [CHANGELOG.md](file:///Users/kazi/Projects/RITUCAST/CHANGELOG.md) adhering to Keep a Changelog standards.
- Production of 11 CI/CD specifications under `docs/ci-cd/` and 5 release specifications under `docs/releases/`.
- Production of 6 formal phase governance records under `docs/phases/phase-14/`.
- Updating master project registers (`roadmap.md`, `decision-log.md` with `DEC-54`–`DEC-57`, `risk-register.md` with `RSK-47`–`RSK-49`, `assumptions-register.md` with `ASM-21`, `README.md`).

### Out of Scope
- Direct deployment to unapproved cloud providers or incurring unauthorized cloud charges.
- Commencing Phase 15 or subsequent lifecycle phases.
- Modifying underlying agronomic equations or adding unverified predictive ML models.

---

## 2. Work Breakdown Structure

1. **Step 1: Baseline Review & Readiness Audit**:
   - Inspect existing tests, build commands, dataset sizes, and runtime dependencies.
2. **Step 2: CI/CD Architecture & Workflow Implementation**:
   - Create `pytest.ini`, `.flake8`, `CHANGELOG.md`, `requirements-dev.txt`.
   - Implement `.github/workflows/ci.yml`, `live-data-smoke.yml`, and `release.yml`.
3. **Step 3: Local Quality Gate & Tooling Verification**:
   - Execute all linting, type-checking, deterministic pytest, frontend vitest, and bundle build commands locally.
4. **Step 4: CI/CD Documentation Authoring**:
   - Create 11 architectural and operational specifications under `docs/ci-cd/`.
5. **Step 5: Release Management Documentation Authoring**:
   - Create 5 release specifications under `docs/releases/`.
6. **Step 6: Governance Documents**:
   - Author `phase-plan.md`, `readiness-assessment.md`, `deliverables-checklist.md`, `validation-report.md`, `phase-14-completion-report.md`, and `handoff-to-phase-15.md`.
7. **Step 7: Master Planning Registers & Verification**:
   - Update `roadmap.md`, `decision-log.md`, `risk-register.md`, `assumptions-register.md`, and `README.md`.
   - Run link integrity validator script across the entire repository.
8. **Step 8: Version Control & Safe Atomic Commits**:
   - Commit changes cleanly and verify working tree status.
