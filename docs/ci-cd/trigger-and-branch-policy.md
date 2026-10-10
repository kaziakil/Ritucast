# Trigger and Branching Policy Specification: Ritucast

## 1. Overview

This document specifies the Git branching strategy, trigger policies, path filters, and merge rules for the Ritucast platform.

---

## 2. Git Branching Strategy

Ritucast follows a **Trunk-Based Development** model optimized for high-reliability, rapid iteration:

- **Primary Branch (`main`)**: The production-ready integration branch. Direct pushes to `main` are restricted in production teams; all code changes must arrive via reviewed pull requests.
- **Short-Lived Feature / Phase Branches (`feature/*`, `phase-*`)**: Created from `main` and merged back via pull request after passing all automated CI quality gates.
- **Release Tags (`v*.*.*`)**: Immutable annotated Git tags created on `main` when a version milestone is reached (e.g., `v1.0.0`).

---

## 3. Workflow Trigger Matrix

| Event | Source Branch / Tag | Triggered Workflows | Purpose & Policy |
| :--- | :--- | :--- | :--- |
| **Pull Request** | PR targeting `main` | `ci.yml` | Validates proposed changes. Must achieve 100% PASS on all jobs before merging. |
| **Push to Main** | `main` | `ci.yml` | Validates integrated mainline code. Prepares build artifacts. |
| **Daily Cron** | N/A (Scheduled at 02:00 UTC) | `live-data-smoke.yml` | Probes live external weather and satellite data feeds. |
| **Version Tag Push** | `v[0-9]+.[0-9]+.[0-9]+*` | `release.yml` | Triggers official release packaging, container publishing, and staged deployment. |
| **Manual Dispatch** | Any branch | `ci.yml`, `live-data-smoke.yml`, `release.yml` | Allows manual regression checks or release rollouts by authorized maintainers. |

---

## 4. Path Filtering Rules

To optimize CI runner time and avoid redundant builds, `ci.yml` excludes documentation-only changes:

```yaml
paths-ignore:
  - 'docs/**'
  - '*.md'
  - '.gitignore'
```

If a commit touches only Markdown documentation files, the heavy container build and test jobs are skipped. However, if any code file (`api/**`, `frontend/**`, `analytics/**`, `pipelines/**`, `data/**`, `tests/**`, `deploy/**`, `Dockerfile*`, `requirements*.txt`) is modified alongside documentation, the entire CI suite executes.

---

## 5. Protected Branch Rules for `main`

The following GitHub branch protection rules must be configured in repository settings:
1. **Require pull request reviews before merging**: At least 1 approving review from code owners.
2. **Require status checks to pass before merging**:
   - `Code Quality & Linting`
   - `Backend Tests (Deterministic)`
   - `Frontend Tests & Production Build`
   - `Dependency & Secret Security Audit`
   - `Container Build Verification`
3. **Require branches to be up to date before merging**.
4. **Include administrators**: Protections apply to all maintainers.
5. **No force pushes or branch deletions**.
