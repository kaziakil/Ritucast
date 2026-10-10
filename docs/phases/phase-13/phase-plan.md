# Phase 13 Plan: Deployment Architecture and Production Readiness

## 1. Objectives & Scope

Phase 13 establishes a reproducible, secure, cost-effective deployment architecture and production readiness package for Ritucast across the two pilot testbeds: High Barind Tract and Haor Basin.

### In Scope
- Baseline inspection of Phase 1–12 outputs, dependencies, test passes, and data footprints.
- Evaluation and selection of a serverless container hosting architecture (Google Cloud Run in `asia-south1`) meeting `DEC-09` and `ADR-07` budget requirements ($\le \$65/\text{month}$).
- Production containerization implementation: multi-stage `Dockerfile.backend` (and root `Dockerfile`), multi-stage `Dockerfile.frontend` with hardened NGINX Alpine, and `docker-compose.yml`.
- Declarative cloud infrastructure manifests: Knative Cloud Run specs (`deploy/cloudrun/service-backend.yaml`, `deploy/cloudrun/service-frontend.yaml`), and automated deployment script (`deploy/cloudrun/deploy.sh`).
- Environment variable schemas and configuration templates (`.env.example`, `.env.production.example`, `.dockerignore`).
- Automated CI/CD pipeline definition (`.github/workflows/ci-cd.yml`).
- Local container build, healthcheck, and docker-compose runtime validation.
- Comprehensive deployment documentation (18 specifications under `docs/deployment/`).
- Formal phase execution records (6 governance documents under `docs/phases/phase-13/`).
- Master planning register updates (`roadmap.md`, `decision-log.md` with `DEC-51`–`DEC-53`, `risk-register.md` with `RSK-44`–`RSK-46`, `assumptions-register.md` with `ASM-20`, `README.md`).

### Out of Scope
- Commencing Phase 14 or subsequent lifecycle phases.
- Introducing a stateful relational database (e.g., PostgreSQL/Cloud SQL) without architectural need (`DEC-52`).
- Complex Kubernetes cluster orchestration or enterprise mesh infrastructure.
- Incurring unapproved cloud charges (GCP credentials missing in local environment; transparently documented).

---

## 2. Work Breakdown Structure

1. **Step 1: Baseline Review & Readiness Assessment**:
   - Inspect existing tests, build commands, dataset sizes, and runtime dependencies.
2. **Step 2: Platform Architecture Selection**:
   - Compare Cloud Run, AWS Fargate, Render/Fly.io, and VPS. Author `hosting-options-comparison.md` and select Google Cloud Run.
3. **Step 3: Manifest & Container Implementation**:
   - Author `requirements.txt`, `requirements-dev.txt`, `.dockerignore`, `.env.example`, `.env.production.example`.
   - Implement multi-stage `Dockerfile.backend`, root `Dockerfile`, `Dockerfile.frontend`, and `deploy/docker/nginx.conf`.
   - Author `docker-compose.yml`, Knative manifests, `deploy.sh`, and `.github/workflows/ci-cd.yml`.
4. **Step 4: Local Container & Orchestration Validation**:
   - Build backend and frontend images; verify non-root user, health probes, and full-stack compose startup.
5. **Step 5: Architectural & Operational Documentation**:
   - Create 18 architectural, security, operational, and procedure specs under `docs/deployment/`.
6. **Step 6: Governance Documents**:
   - Author `phase-plan.md`, `readiness-assessment.md`, `deliverables-checklist.md`, `validation-report.md`, `phase-13-completion-report.md`, and `handoff-to-phase-14.md`.
7. **Step 7: Master Planning Registers & Verification**:
   - Update `roadmap.md`, `decision-log.md`, `risk-register.md`, `assumptions-register.md`, and `README.md`. Run full verification suite (95 pytest, 17 vitest, build, link checker).
8. **Step 8: Version Control & Safe Commit**:
   - Clean, logically grouped atomic Git commits.
