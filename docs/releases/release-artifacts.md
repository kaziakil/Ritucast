# Release Artifacts Specification: Ritucast

## 1. Overview

This document specifies the official artifacts generated during a Ritucast release, their naming conventions, contents, provenance, and storage locations.

---

## 2. Release Artifact Inventory

| Artifact | File / Tag Name | Format | Storage Location | Retention | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Release Tarball** | `ritucast-v1.0.0.tar.gz` | Gzip Archive | GitHub Releases & Action Artifact | Permanent | Compressed archive containing all backend code, frontend build output, sample data fixtures, Dockerfiles, and documentation. |
| **OpenAPI Schema** | `openapi.json` | JSON (RFC 8259) | GitHub Releases & Action Artifact | Permanent | Canonical OpenAPI 3.0 specification exported from the FastAPI application. |
| **Backend Container** | `backend:v1.0.0` & `backend:<SHA>` | OCI Docker Image | Google Artifact Registry (`asia-south1`) | Permanent | Hardened Python 3.10-slim backend image with bundled Parquet feature stores and non-root UID 10001 user. |
| **Frontend Container** | `frontend:v1.0.0` & `frontend:<SHA>`| OCI Docker Image | Google Artifact Registry (`asia-south1`) | Permanent | Lightweight NGINX Alpine image with compiled static React 19 SPA assets. |
| **Frontend Static Bundle** | `frontend-production-dist` | Zip / Tarball | GitHub Action Artifact | 14 Days | Standalone static build output from `frontend/dist/`. |
| **Test Coverage Report**| `coverage.xml` | Cobertura XML | GitHub Action Artifact | 14 Days | Machine-readable backend pytest coverage report. |

---

## 3. Immutability and Provenance Verification

To guarantee that release artifacts can never be silently overwritten or modified:
1. **Dual Tagging**: Every container image is pushed with both a mutable semantic version tag (`:v1.0.0`) and an immutable Git commit SHA tag (`:1c7c85d`).
2. **Digest Referencing**: Production Cloud Run deployments can pin the exact container image SHA256 digest (e.g., `backend@sha256:d88d61...`).
3. **Reproducibility Guarantee**: In-image bundled Parquet datasets ensure that rolling back to a previous container digest restores both the application logic and the exact feature store state simultaneously.
