# Phase 14 CI/CD Architecture: Ritucast Agricultural Intelligence Platform

## 1. Executive Summary

This document establishes the Continuous Integration (CI), Continuous Delivery (CD), and Release Management architecture for **Ritucast**, an evidence-based agricultural intelligence platform operating across the High Barind Tract and Haor Basin testbeds in Bangladesh.

The architecture addresses three core operational mandates:
1. **Safety & Agronomic Integrity (`DEC-08`, `DEC-17`)**: Preventing unvalidated code, uncalibrated thresholds, or broken models from reaching rural smallholders and agricultural extension workers.
2. **Deterministic Isolation (`DEC-48`)**: Separating routine pull-request regression tests from unpredictable upstream public satellite APIs (NASA POWER, Open-Meteo, CDSE).
3. **Approval-Gated Continuous Delivery**: Automating release packaging and container image tagging while enforcing explicit human authorization gates for production deployment to Google Cloud Run (`asia-south1`).

---

## 2. CI/CD Architecture Overview

Ritucast deploys a modular, three-tier workflow structure implemented natively on **GitHub Actions**:

```
                                [ Developer / Contributor Git Actions ]
                                                  │
                 ┌────────────────────────────────┼────────────────────────────────┐
                 │ PR to main / Push to main      │ Daily Cron (02:00 UTC)         │ Version Tag (v*.*.*)
                 ▼                                ▼                                ▼
   ┌───────────────────────────┐    ┌───────────────────────────┐    ┌───────────────────────────┐
   │ .github/workflows/ci.yml  │    │ live-data-smoke.yml       │    │ release.yml               │
   │ (Continuous Integration)  │    │ (Upstream Data Health)    │    │ (Continuous Delivery)     │
   ├───────────────────────────┤    ├───────────────────────────┤    ├───────────────────────────┤
   │ 1. Code Quality & Lint    │    │ 1. Live NASA POWER Probe  │    │ 1. Full Regression Gate   │
   │    - Flake8 syntax check  │    │ 2. Live Open-Meteo Probe  │    │ 2. OpenAPI Spec Extract   │
   │    - Oxlint + tsc -b      │    │ 3. Schema Drift Alert     │    │ 3. Release Tarball Bundle │
   │ 2. Deterministic Pytest   │    │ (Non-blocking for PRs)    │    │ 4. GitHub Release Assets  │
   │    - pytest -m "not smoke"│    └───────────────────────────┘    │ 5. Container Image Push   │
   │    - Parquet & math tests │                                     │    - Immutable SHA tag    │
   │ 3. Frontend Vitest & Build│                                     │    - SemVer tag           │
   │    - Vitest unit/journey  │                                     │ 6. Production Deploy Gate │
   │    - Production bundle    │                                     │    - Reviewer Approval    │
   │ 4. Security & Secret Audit│                                     │    - Cloud Run deploy.sh  │
   │    - pip-audit & npm audit│                                     │    - Post-deploy smoke    │
   │    - Private key grep     │                                     └───────────────────────────┘
   │ 5. Container Build Check  │
   │    - Docker Buildx verify │
   └───────────────────────────┘
```

---

## 3. Workflow Taxonomy

| Workflow File | Trigger Conditions | Primary Responsibility | Failure Consequence |
| :--- | :--- | :--- | :--- |
| **`ci.yml`** | PR to `main`, Push to `main`, `workflow_dispatch` | Validates code quality, deterministic backend logic, frontend bundle, and container reproducibility. | Blocks pull request merge; notifies developer. |
| **`live-data-smoke.yml`** | Scheduled daily at 02:00 UTC (08:00 BST), `workflow_dispatch` | Probes live external weather and satellite APIs for upstream connectivity and contract drift. | Generates warning annotation; triggers telemetry alert; does NOT block PR merges. |
| **`release.yml`** | Push tags `v*.*.*`, `workflow_dispatch` | Packages release archives, extracts OpenAPI schema, builds tagged container images, and executes approval-gated production deploy. | Release publication paused; production container rollback available. |

---

## 4. Key Architectural Invariants

1. **Deterministic Test Priority (`DEC-48`)**: Standard CI jobs execute in $<25\text{ seconds}$ without making external network calls to third-party APIs. Tests use version-controlled sample fixtures (`data/sample/`).
2. **Zero In-Repo Credentials**: Workflows use GitHub Secrets and Google Cloud Workload Identity Federation (OIDC tokens). No long-lived service account JSON keys or passwords are stored in the repository.
3. **Artifact Immutability**: Production container images are tagged with both the semantic version (`v1.0.0`) and the immutable Git commit SHA (`git rev-parse --short HEAD`).
4. **Human Approval for Production**: Production deployments require manual sign-off within the GitHub Actions `production` environment before invoking `deploy/cloudrun/deploy.sh`.
