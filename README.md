# Ritucast: Agricultural Intelligence Platform

> **Transforming Earth Observation Satellites, Numerical Weather Predictions, and Soil-Moisture Data into Localized Agronomic Decision Intelligence for Bangladesh.**

---

## 1. Project Overview

**Ritucast** is an agricultural intelligence and decision-support platform designed to address the "last-mile translation gap" in Bangladesh agriculture. By synthesizing multi-source environmental observations (NASA POWER, Sentinel-1 SAR, SMAP, GPM IMERG) with localized crop phenology calendars (BRRI, BARI, BBS), Ritucast delivers clear, explainable, Bangla-first decision support to frontline extension officers and progressive lead farmers.

### Key Capabilities in Initial Scope
- **Crop Water Deficit & Irrigation Scheduling**: Weather-synchronized irrigation postponement saving pumping diesel and electricity in drought-prone areas (Barind Tract).
- **Flash-Flood & Inundation Early Warning**: Upstream catchment precipitation tracking and radar inundation detection protecting pre-monsoon Boro rice harvests in wetland basins (Haor Basin).
- **Weather-Synchronized Farming Windows**: Phenology-aware planting, transplanting, and safe harvesting windows.
- **Explainable Bangla Advisory Cards**: Transparent reasoning that clearly delineates empirical satellite observations from forecast models.

---

## 2. Project Status & Roadmap

Ritucast is developed under a strict **18-phase governed engineering lifecycle**.

| Current Phase | Phase Name | Status |
| :---: | :--- | :--- |
| **01** | **Project Discovery and Problem Definition** | **Completed (PASS)** |
| **02** | **Requirements and Product Strategy** | **Completed (PASS)** |
| **03** | **Dataset Research and Validation** | **Completed (PASS)** |
| **04** | **Agricultural Knowledge & Scientific Validation Planning** | **Completed (PASS)** |
| **05** | **System Architecture & Technology Decisions** | **Completed (PASS)** |
| 06 | Information Architecture & User Journey Design | *Pending Review (Next)* |
| 07–18 | Detailed Design through Long-Term Expansion | *Pending* |

Full details and phase governance rules can be viewed in the [Master Project Roadmap](file:///Users/kazi/Projects/RITUCAST/docs/planning/roadmap.md).

---

## 3. Project Documentation Index

### Phase 1: Strategic & Discovery Baseline
- [Project Overview](file:///Users/kazi/Projects/RITUCAST/docs/project/project-overview.md): Executive summary, purpose, and concept.
- [Problem Definition & Ranked Inventory](file:///Users/kazi/Projects/RITUCAST/docs/project/problem-definition.md): Evidence-based assessment of candidate problems.
- [Target User Analysis](file:///Users/kazi/Projects/RITUCAST/docs/project/target-users.md): Multi-segment evaluation, dual-anchor model (SAAOs + Lead Farmers).
- [Product Vision & Positioning](file:///Users/kazi/Projects/RITUCAST/docs/project/product-vision.md): Vision, mission, 10 core principles, and DSS positioning.
- [Initial Product Scope](file:///Users/kazi/Projects/RITUCAST/docs/project/initial-scope.md): Essential capabilities, non-goals, and explicit exclusions.
- [Geographic & Agricultural Scope](file:///Users/kazi/Projects/RITUCAST/docs/project/geographic-agricultural-scope.md): AEZ assessment and dual-zone pilot testbeds.
- [Success Metrics Framework](file:///Users/kazi/Projects/RITUCAST/docs/project/success-metrics.md): 4-tier measurement pyramid from tech to agronomic impact.
- [Long-Term Product Direction](file:///Users/kazi/Projects/RITUCAST/docs/project/long-term-direction.md): 3 strategic horizons and future expansion areas.

### Phase 2: Product Strategy & User Journeys
- [Product Strategy](file:///Users/kazi/Projects/RITUCAST/docs/product/product-strategy.md): Strategic parameters, competitive differentiation, 5-stage value chain.
- [User Needs & Critical Journeys](file:///Users/kazi/Projects/RITUCAST/docs/product/user-needs-and-journeys.md): 3 detailed personas, 4 JTBDs, and 4 end-to-end user journeys.
- [Initial Release Strategy](file:///Users/kazi/Projects/RITUCAST/docs/product/release-strategy.md): Minimum Complete Product (MCP) scope, staged evolution timeline, and 5 release gates.
- [Success Measurement Plan](file:///Users/kazi/Projects/RITUCAST/docs/product/success-measurement-plan.md): Operational metrics across 5 categories with baseline protocols.

### Phase 2: Product Requirements & Technical Specifications
- [Product Requirements Document (PRD)](file:///Users/kazi/Projects/RITUCAST/docs/requirements/product-requirements.md): Complete PRD with 15 functional requirements with stable IDs.
- [Non-Functional Requirements (NFR)](file:///Users/kazi/Projects/RITUCAST/docs/requirements/nonfunctional-requirements.md): 19 NFRs across usability, accessibility, performance, reliability, and security.
- [Feature Prioritization Matrix](file:///Users/kazi/Projects/RITUCAST/docs/requirements/feature-prioritization.md): 5-tier classification framework and 16-feature master matrix.
- [Requirements Traceability Matrix (RTM)](file:///Users/kazi/Projects/RITUCAST/docs/requirements/requirements-traceability.md): End-to-end traceability mapping problems to requirements and tests.
- [Product-Level Data Requirements](file:///Users/kazi/Projects/RITUCAST/docs/requirements/data-requirements.md): Specifications across 5 categories (`DR-MET`, `DR-PCP`, `DR-SMC`, `DR-SAR`, `DR-AGR`).
- [Recommendation Quality & Scientific Safety](file:///Users/kazi/Projects/RITUCAST/docs/requirements/recommendation-quality-and-safety.md): 4-tier taxonomy, suppression conditions, and anti-overconfidence rules.

### Phase 3: Dataset Research, Validation & Governance
- [Master Candidate Dataset Inventory](file:///Users/kazi/Projects/RITUCAST/docs/data/dataset-inventory.md): Audit of 16 candidate categories; product classifications and recommendations.
- [Dataset Comparison Matrix](file:///Users/kazi/Projects/RITUCAST/docs/data/dataset-comparison-matrix.md): Master matrix comparing 10 primary candidates across 20 parameters with stable IDs.
- [Initial Dataset Stack](file:///Users/kazi/Projects/RITUCAST/docs/data/initial-dataset-stack.md): 8 Core initial datasets, 2 optional, and 6 deferred/rejected with full rationales.
- [Data Access, Licensing & Governance](file:///Users/kazi/Projects/RITUCAST/docs/data/data-access-and-licensing.md): API protocols, auth mechanisms, rate limits, open licenses, and privacy.
- [Data Quality Validation Protocols](file:///Users/kazi/Projects/RITUCAST/docs/data/data-quality-validation.md): 5-stage automated QC protocol, physical value ranges, and QA flag limits.
- [Spatial & Temporal Aggregation Requirements](file:///Users/kazi/Projects/RITUCAST/docs/data/spatial-temporal-requirements.md): Mixed-pixel realities, zonal aggregation math, and anti-false-precision rules.
- [Technical Source Registry](file:///Users/kazi/Projects/RITUCAST/docs/data/source-registry.md): Machine-readable technical catalog of verified endpoints, bounding boxes, and collections.

### Phase 4: Agricultural Knowledge & Scientific Validation
- [Agricultural Knowledge Base](file:///Users/kazi/Projects/RITUCAST/docs/science/agricultural-knowledge-base.md): Synthesis of BRRI, BARI, BARC, FAO, IRRI, and BMD research.
- [Crop & Regional Context Specification](file:///Users/kazi/Projects/RITUCAST/docs/science/crop-and-regional-context.md): Agro-ecological profiles of Barind (AEZ 25/26) and Haor (AEZ 21) testbeds.
- [Dataset Scientific Interpretation](file:///Users/kazi/Projects/RITUCAST/docs/science/dataset-scientific-interpretation.md): Physical mechanics, assumptions, and observational limits of the 8 core datasets.
- [Indicator Interpretation Framework](file:///Users/kazi/Projects/RITUCAST/docs/science/indicator-interpretation-framework.md): Mathematical formulations for FAO-56 $ET_0$, Soil Water Balance, Haor Index $I_{\text{flood}}$.
- [Agricultural Rule Specifications](file:///Users/kazi/Projects/RITUCAST/docs/science/agricultural-rule-specifications.md): Catalog of 6 core rules (`RULE-IRR-01`, `RULE-FLD-01`, etc.) with quantitative triggers.
- [Scientific Validation Plan](file:///Users/kazi/Projects/RITUCAST/docs/science/scientific-validation-plan.md): Ground-truth benchmarking with BMD synoptic stations, BMDA lysimeters, BWDB gauges, and hindcasting.
- [Evaluation Metrics & Acceptance Criteria](file:///Users/kazi/Projects/RITUCAST/docs/science/evaluation-metrics-and-acceptance.md): Formulations ($MAE, RMSE, POD, FAR, CSI, BS, ACR$) and release gating thresholds.
- [Modeling Readiness & Guardrails](file:///Users/kazi/Projects/RITUCAST/docs/science/modeling-readiness-and-guardrails.md): Physical baseline-first philosophy, 6 ML readiness gates, and ban on black-box predictions.
- [Uncertainty & Risk Communication](file:///Users/kazi/Projects/RITUCAST/docs/science/uncertainty-and-risk-communication.md): Advisory confidence score math, lead-time decay, ensemble penalty, Bangla UX copy.
- [Recommendation Safety Framework](file:///Users/kazi/Projects/RITUCAST/docs/science/recommendation-safety-framework.md): Mandatory contextual gating (upazila/crop/stage), automated suppression triggers, "Do No Harm" protocols.
- [Scientific Governance & Provenance](file:///Users/kazi/Projects/RITUCAST/docs/science/scientific-governance.md): Master Scientific Asset Registry tracking 12 assets with lifecycle states and versioning.
- [Research Gaps Register](file:///Users/kazi/Projects/RITUCAST/docs/science/research-gaps.md): Catalog of 5 open scientific uncertainties with assigned roadmap phases and fallback plans.

### Phase 5: System Architecture & Technology Decisions
- [Architecture Requirements](file:///Users/kazi/Projects/RITUCAST/docs/architecture/architecture-requirements.md): Traceable functional/non-functional drivers, client performance budgets ($\le 1.5\text{MB}$ bundle, $\le 3.5\text{s}$ TTI, $\le 45\text{MB}$ heap).
- [System Architecture](file:///Users/kazi/Projects/RITUCAST/docs/architecture/system-architecture.md): Alternative evaluations, selection of Decoupled Modular Monolith, master topology diagram.
- [Component Boundaries](file:///Users/kazi/Projects/RITUCAST/docs/architecture/component-boundaries.md): Responsibilities, I/O, and failure modes across 8 core subsystems.
- [Technology Stack](file:///Users/kazi/Projects/RITUCAST/docs/architecture/technology-stack.md): Justified stack: React 18, TypeScript, Vite, Vanilla CSS, FastAPI, PostGIS, Redis, MapLibre.
- [Data Architecture](file:///Users/kazi/Projects/RITUCAST/docs/architecture/data-architecture.md): Lifecycle stages, relational schemas (ERD), spatial CRS conventions, temporal alignment, provenance.
- [API & Component Contracts](file:///Users/kazi/Projects/RITUCAST/docs/architecture/api-and-component-contracts.md): OpenAPI 3.0 REST contracts for Upazilas, Weather, Water Balance, Flood Hazard, and Advisories.
- [Security & Data Governance](file:///Users/kazi/Projects/RITUCAST/docs/architecture/security-and-data-governance.md): Threat modeling, Zero-PII policy, Secret Manager, Cloud Armor rate limits, open licenses.
- [Reliability, Performance & Cost](file:///Users/kazi/Projects/RITUCAST/docs/architecture/reliability-performance-and-cost.md): 4-tier caching, budget Android tuning, Google Cloud cost model ($\le \$65/\text{month}$).
- [Repository & Module Structure](file:///Users/kazi/Projects/RITUCAST/docs/architecture/repository-and-module-structure.md): Decoupled monorepo layout, dependency invariant rules, coding standards.
- [Testing & Quality Strategy](file:///Users/kazi/Projects/RITUCAST/docs/architecture/testing-and-quality-strategy.md): 5-tier testing pyramid, automated CI/CD blueprint, software vs scientific validity.
- [Architecture Risk Register](file:///Users/kazi/Projects/RITUCAST/docs/architecture/architecture-risk-register.md): 8 engineering risks (`RSK-ARC-01` to `RSK-ARC-08`) with triggers and fallbacks.
- **Architecture Decision Records (ADRs)**:
  - [ADR-01: Decoupled Modular Architecture](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-01-decoupled-modular-architecture.md)
  - [ADR-02: FastAPI Python Backend](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-02-fastapi-backend.md)
  - [ADR-03: React 18, TypeScript & Vanilla CSS](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-03-react-typescript-vanilla-css.md)
  - [ADR-04: PostgreSQL & PostGIS Spatial Datastore](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-04-postgis-spatial-datastore.md)
  - [ADR-05: Redis Multi-Tier Caching & Task Broker](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-05-redis-caching-and-broker.md)
  - [ADR-06: MapLibre GL JS Client Mapping](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-06-maplibre-vector-maps.md)
  - [ADR-07: Asymmetric Regional Pipelines](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-07-asymmetric-regional-pipelines.md)
  - [ADR-08: Automated Suppression Middleware](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-08-automated-suppression-middleware.md)
  - [ADR-09: Celery & Redis Scheduled Ingestion](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-09-celery-scheduled-ingestion.md)

### Planning, Governance & Quality Registers
- [Agent Operating Instructions (AGENTS.md)](file:///Users/kazi/Projects/RITUCAST/AGENTS.md): Project-wide AI operating principles, scope boundaries, and safety guardrails.
- [Phase 1–4 Continuity & Readiness Audit](file:///Users/kazi/Projects/RITUCAST/docs/project/phase-1-to-4-continuity-audit.md): Comprehensive pre-Phase 5 audit of artifacts, tests, data, and risks.
- [Assumptions Register](file:///Users/kazi/Projects/RITUCAST/docs/planning/assumptions-register.md): Tracked assumptions with verification paths (updated with ASM-04/07/11/12).
- [Risk Register](file:///Users/kazi/Projects/RITUCAST/docs/planning/risk-register.md): 22 prioritized risks with mitigations (updated with RSK-19 through RSK-22).
- [Decision Log](file:///Users/kazi/Projects/RITUCAST/docs/planning/decision-log.md): Architectural decisions log (updated with DEC-19 through DEC-23).
- [Master Project Roadmap](file:///Users/kazi/Projects/RITUCAST/docs/planning/roadmap.md): 18-phase lifecycle status.

### Phase Execution Packages
- **Phase 01 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/phase-plan.md) | [Research Notes](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/research-notes.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/validation-report.md) | [Handoff to Phase 2](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/handoff-to-phase-02.md)
- **Phase 02 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-02/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-02/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-02/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-02/validation-report.md) | [Handoff to Phase 3](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-02/handoff-to-phase-03.md)
- **Phase 03 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/readiness-assessment.md) | [Research Notes](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/research-notes.md) | [Verification Log](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/verification-log.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/validation-report.md) | [Handoff to Phase 4](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/handoff-to-phase-04.md)
- **Phase 04 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/readiness-assessment.md) | [Evidence Register](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/evidence-register.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/validation-report.md) | [Handoff to Phase 5](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/handoff-to-phase-05.md)
- **Phase 05 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/validation-report.md) | [Handoff to Phase 6](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/handoff-to-phase-06.md)

---

## 4. Repository Structure

```text
RITUCAST/
├── README.md
├── AGENTS.md
├── .editorconfig
├── .gitignore
└── docs/
    ├── project/
    ├── product/
    ├── requirements/
    ├── data/
    ├── science/
    ├── architecture/
    │   ├── decisions/
    │   │   ├── ADR-01-decoupled-modular-architecture.md
    │   │   ├── ADR-02-fastapi-backend.md
    │   │   ├── ADR-03-react-typescript-vanilla-css.md
    │   │   ├── ADR-04-postgis-spatial-datastore.md
    │   │   ├── ADR-05-redis-caching-and-broker.md
    │   │   ├── ADR-06-maplibre-vector-maps.md
    │   │   ├── ADR-07-asymmetric-regional-pipelines.md
    │   │   ├── ADR-08-automated-suppression-middleware.md
    │   │   └── ADR-09-celery-scheduled-ingestion.md
    │   ├── architecture-requirements.md
    │   ├── system-architecture.md
    │   ├── component-boundaries.md
    │   ├── technology-stack.md
    │   ├── data-architecture.md
    │   ├── api-and-component-contracts.md
    │   ├── security-and-data-governance.md
    │   ├── reliability-performance-and-cost.md
    │   ├── repository-and-module-structure.md
    │   ├── testing-and-quality-strategy.md
    │   └── architecture-risk-register.md
    ├── planning/
    │   ├── roadmap.md
    │   ├── decision-log.md
    │   ├── risk-register.md
    │   └── assumptions-register.md
    └── phases/
        ├── phase-01/
        ├── phase-02/
        ├── phase-03/
        ├── phase-04/
        └── phase-05/
```

---

## 5. Development Principles

1. **Disciplined Phase Execution**: No execution of subsequent phases without formal quality gate review.
2. **Scientific Transparency**: Clear separation of empirical observations, forecast models, and agronomic advisories.
3. **Data Protection**: Large raw datasets, satellite imagery caches, and secrets are excluded from Git via `.gitignore`.
