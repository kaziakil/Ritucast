# Known CI/CD Limitations & Deferred Capabilities: Ritucast

## 1. Overview

This document records the operational limitations, deferred workflow capabilities, and external prerequisites of Ritucast's CI/CD automation.

---

## 2. Environment Limitations & Active Blockers

### Limitation 1: Remote GitHub Actions Workflow Execution Untested Live
- **Description**: All workflow definitions (`ci.yml`, `live-data-smoke.yml`, `release.yml`) are fully authored, syntax-checked, and their underlying commands empirically verified on the local development machine. However, because the repository is operating in a local development environment without an active upstream GitHub remote connection, remote GitHub runner executions cannot be triggered or verified directly.
- **Impact**: Workflows are **Configured & Locally Validated**, but **Awaiting Remote Push to GitHub**.
- **Remediation**: Once pushed to GitHub, GitHub Actions will automatically parse the workflow triggers.

### Limitation 2: Cloud Run Continuous Deployment Paused Pending GCP Secrets
- **Description**: Automated continuous deployment in `release.yml` is conditioned on the presence of `secrets.GCP_PROJECT_ID` and `secrets.GCP_WORKLOAD_IDENTITY_PROVIDER`. Since these secrets are not configured in source control (per security policy), the deployment step skips gracefully if secrets are absent.
- **Remediation**: Repository administrators must add the GCP Workload Identity secrets in GitHub Settings $\rightarrow$ Secrets and Variables $\rightarrow$ Actions.

---

## 3. Deferred Automation Scope

### Limitation 3: Automated Changelog Generation from Commits
- **Description**: `CHANGELOG.md` is currently curated and updated in accordance with the Keep a Changelog standard. Automated conventional-commit changelog tooling (e.g., semantic-release, standard-version) is deferred to future releases to preserve human editorial control over agronomic safety descriptions.

### Limitation 4: Multi-Browser Cross-Platform Matrix Testing
- **Description**: Frontend Vitest journey tests run in standard JSDOM headless environments. End-to-end multi-browser matrices (e.g., real Chrome Android WebViews on physical devices) are scheduled for Phase 15/16 field validation.
