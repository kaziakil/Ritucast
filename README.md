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
| **06** | **Information Architecture & User Journey Design** | **Completed (PASS)** |
| **07** | **Visual Design and Design System** | **Completed (PASS)** |
| **08** | **Data Ingestion & Processing Pipeline** | **Completed (PASS)** |
| **09** | **Agricultural Analytics & Recommendation Engine** | **Completed (PASS)** |
| **10** | **Backend API and Service Layer** | **Completed (PASS)** |
| **11** | **Frontend Application and User Experience** | **Completed (PASS)** |
| **12** | **End-to-End Integration and System Validation** | **Completed (PASS)** |
| **13** | **Deployment Architecture and Production Readiness** | **Completed (PASS)** |
| **14** | **CI/CD Automation and Release Management** | **Completed (PASS)** |
| **15** | **Security, Privacy, and Responsible Agricultural Intelligence** | **Completed (PASS)** |
| 16 | Usability, Accessibility & Performance | *Pending Review (Next)* |
| 17–18 | Scientific Validation through Expansion | *Pending* |

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
- **Architecture Decision Records (ADRs)**: Catalog of 9 formal ADRs (`ADR-01` through `ADR-09`) in [docs/architecture/decisions/](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/).

### Phase 6: Information Architecture & User Journey Design
- [UX Design Principles](file:///Users/kazi/Projects/RITUCAST/docs/ux/ux-principles.md): 12 binding principles (farmer-centered, action-oriented, evidence-based, scientifically responsible).
- [User Groups & Needs](file:///Users/kazi/Projects/RITUCAST/docs/ux/user-groups-and-needs.md): Dual-anchor profiles (SAAO Tariqul, Barind Farmer Mokhles, Haor Farmer Joynal) and constraints.
- [Core User Tasks](file:///Users/kazi/Projects/RITUCAST/docs/ux/core-user-tasks.md): 10 core tasks mapped to PRD requirements (`TSK-01` to `TSK-10`) with failure/empty states.
- [Information Architecture](file:///Users/kazi/Projects/RITUCAST/docs/ux/information-architecture.md): Decision-driven navigation model, context-adaptive tabs (Barind Soil vs Haor Flood).
- [Sitemap Specification](file:///Users/kazi/Projects/RITUCAST/docs/ux/sitemap.md): Complete page taxonomy and routing with standalone diagram source [sitemap.mmd](file:///Users/kazi/Projects/RITUCAST/docs/ux/diagrams/sitemap.mmd).
- [Critical User Journeys](file:///Users/kazi/Projects/RITUCAST/docs/ux/user-journeys.md): Step-by-step flows and Mermaid flowcharts for Journeys A through F.
- [Page Content & Layout Requirements](file:///Users/kazi/Projects/RITUCAST/docs/ux/page-requirements.md): Layout blueprints for `PAGE-00` through `PAGE-05` with essential blocks and controls.
- [Geographic Context & Selection](file:///Users/kazi/Projects/RITUCAST/docs/ux/geographic-context-and-selection.md): Upazila selection model, persistence, and coarse satellite grid caveats.
- [Agricultural Insight Information Model](file:///Users/kazi/Projects/RITUCAST/docs/ux/agricultural-insight-information-model.md): 8-Layer conceptual structure separating observations from recommendations.
- [Trust, Uncertainty & Suppression Patterns](file:///Users/kazi/Projects/RITUCAST/docs/ux/trust-and-uncertainty-patterns.md): 8 epistemic states, non-color-only cues, and automated suppression fallbacks.
- [Accessibility, Localization & Connectivity](file:///Users/kazi/Projects/RITUCAST/docs/ux/accessibility-localization-and-connectivity.md): WCAG 2.2 AA targets, Bangla agrarian glossary, and 3G offline caching.
- [Interaction & State Matrix](file:///Users/kazi/Projects/RITUCAST/docs/ux/interaction-and-state-specification.md): Reusable state matrix specifying 14 interaction states (`ST-01` to `ST-14`).
- [UX Success Metrics](file:///Users/kazi/Projects/RITUCAST/docs/ux/ux-success-metrics.md): 10 objective usability metrics (`UX-MET-01` to `UX-MET-10`) and evaluation protocols.

### Phase 7: Visual Design and Design System
- [Visual Direction](file:///Users/kazi/Projects/RITUCAST/docs/design/visual-direction.md): Visual identity, aesthetic tone ("Calm Scientific Authority"), solar light theme, outdoor sunlight legibility.
- [Color System](file:///Users/kazi/Projects/RITUCAST/docs/design/color-system.md): Agronomic color tokens, solar palette, 4-tier epistemic color mapping, WCAG 2.2 AA contrast matrix ($\ge 7:1$).
- [Typography System](file:///Users/kazi/Projects/RITUCAST/docs/design/typography-system.md): Hind Siliguri and Noto Sans Bengali type scale, tabular numbers (`tnum`), line-height $\ge 1.5$.
- [Layout & Responsive System](file:///Users/kazi/Projects/RITUCAST/docs/design/layout-and-responsive-system.md): 8pt fluid grid, 48px touch targets, mobile-first column layouts, breakpoint rules.
- [Design Tokens Blueprint](file:///Users/kazi/Projects/RITUCAST/docs/design/design-tokens.md): Complete Vanilla CSS `:root` Custom Properties architecture for `index.css` ($\le 50\text{KB}$, zero Tailwind).
- [Component Design System](file:///Users/kazi/Projects/RITUCAST/docs/design/component-system.md): Reusable component specifications including the 5-section Advisory Card (`CMP-CARD-01`), navigation, drawers, chips.
- [Data Visualization Guidelines](file:///Users/kazi/Projects/RITUCAST/docs/design/data-visualization-guidelines.md): Accessible dual-layer visualization standards (rain bars, temp lines, soil dials, flood meters + semantic tables).
- [Scientific Transparency Patterns](file:///Users/kazi/Projects/RITUCAST/docs/design/scientific-transparency-patterns.md): 4-tier visual containers (`DEC-08`), automated suppression banner (`DEC-10`), field-check notices.
- [Iconography & Imagery Guidelines](file:///Users/kazi/Projects/RITUCAST/docs/design/iconography-and-imagery.md): Lucide 2px outline glyphs, 24x24px grid, authentic Boro rice imagery rules, non-color-only icons.
- [Interaction & Motion Guidelines](file:///Users/kazi/Projects/RITUCAST/docs/design/interaction-and-motion-guidelines.md): Micro-transitions (150ms/250ms), zero continuous CPU animations, `prefers-reduced-motion` overrides.
- [Feedback & State Patterns](file:///Users/kazi/Projects/RITUCAST/docs/design/feedback-and-state-patterns.md): Visual treatments for 14 interaction states (skeletons, stale data, offline banners, server fallbacks).
- [Accessibility Standards](file:///Users/kazi/Projects/RITUCAST/docs/design/accessibility-standards.md): WCAG 2.2 Level AA compliance rules for visual presentation and assistive devices.
- [Visual References & Wireframes](file:///Users/kazi/Projects/RITUCAST/docs/design/visual-references.md): Annotated layout wireframes for `PAGE-01`, `PAGE-02`, `PAGE-03A`, `PAGE-03B`, and suppression states.

### Phase 8: Data Ingestion and Processing Pipeline
- [Dataset Implementation Scope](file:///Users/kazi/Projects/RITUCAST/docs/data/phase-08-dataset-implementation-scope.md): Classification of 8 approved, 3 deferred, 3 rejected sources with parameter catalogs.
- [Pipeline Architecture](file:///Users/kazi/Projects/RITUCAST/docs/data/pipeline-architecture.md): Flow topology, component boundaries, and decoupling rules.
- [Storage & File Conventions](file:///Users/kazi/Projects/RITUCAST/docs/data/storage-and-file-conventions.md): 5 storage tiers, Snappy Parquet format conventions, and `.gitignore` data protection.
- [Spatial Processing Specification](file:///Users/kazi/Projects/RITUCAST/docs/data/spatial-processing-specification.md): WGS84 standards, pilot zone bounding boxes, and centroid extraction rules.
- [Temporal Processing Specification](file:///Users/kazi/Projects/RITUCAST/docs/data/temporal-processing-specification.md): UTC to BST (+6h) day boundary conversion, rolling rainfall windows (24h, 48h, 7d), and GDD math.
- [Feature Preparation Specification](file:///Users/kazi/Projects/RITUCAST/docs/data/feature-preparation-specification.md): Standardized Parquet analytical table definitions feeding directly into Phase 9.
- [Provenance & Versioning](file:///Users/kazi/Projects/RITUCAST/docs/data/provenance-and-versioning.md): Run manifest JSON schema, SHA-256 cryptographic hashing, and audit ledger.
- [Pipeline Execution Guide](file:///Users/kazi/Projects/RITUCAST/docs/data/pipeline-execution.md): CLI argument reference, dry run flags, exit codes, and invocation examples.
- [Local Pipeline Setup](file:///Users/kazi/Projects/RITUCAST/docs/data/local-data-pipeline-setup.md): Local environment requirements, Python 3.10 setup, test commands, and troubleshooting.
- [Pipeline Testing Strategy](file:///Users/kazi/Projects/RITUCAST/docs/data/pipeline-testing-strategy.md): Testing pyramid, synthetic fixtures, network mocking, and pass criteria.
- [Performance & Resource Guidelines](file:///Users/kazi/Projects/RITUCAST/docs/data/performance-and-resource-guidelines.md): $\le 512\text{MB}$ worker memory budgets, streaming reads, NASA POWER rate limits.
- [Data Licensing & Scientific Safeguards](file:///Users/kazi/Projects/RITUCAST/docs/data/data-licensing-and-scientific-safeguards.md): Open-data licenses, attribution register, and 3 mandatory scientific safeguards.

### Phase 9: Agricultural Analytics and Recommendation Engine
- [Analytics Implementation Scope](file:///Users/kazi/Projects/RITUCAST/docs/analytics/phase-09-analytics-scope.md): Capability classification, physical indicators, master rules catalog, and non-goals.
- [Data Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/analytics/data-readiness-assessment.md): Audit across analytical tiers; justification for blocking ungrounded supervised ML.
- [Analytics Architecture](file:///Users/kazi/Projects/RITUCAST/docs/analytics/analytics-architecture.md): Modular component flow, bounded contexts, contracts, and failure modes.
- [Descriptive Agricultural Analytics](file:///Users/kazi/Projects/RITUCAST/docs/analytics/descriptive-analytics.md): Climatology aggregator, temperature extremes, and data completeness metrics.
- [Environmental Indicators Specification](file:///Users/kazi/Projects/RITUCAST/docs/analytics/environmental-indicators.md): Physical equations for FAO-56 $ET_0$, dynamic $K_c(t)$, soil deficit $D_t$, Haor $I_{\text{flood}}$, and thermal stress.
- [Method Selection and Rationale](file:///Users/kazi/Projects/RITUCAST/docs/analytics/method-selection-and-rationale.md): Rigorous defense of deterministic physical equations over uncalibrated ML.
- [Risk Model Specification](file:///Users/kazi/Projects/RITUCAST/docs/analytics/risk-model-specification.md): Hazard formulations, decision horizons, and asymmetric error cost matrices.
- [Model Development and Evaluation](file:///Users/kazi/Projects/RITUCAST/docs/analytics/model-development-and-evaluation.md): Development protocol and physical benchmark verification.
- [Model Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/analytics/model-validation-report.md): Automated testing results (35 analytics tests, 60 total repo tests passing).
- [Explainability & Attribution Strategy](file:///Users/kazi/Projects/RITUCAST/docs/analytics/explainability-strategy.md): Deterministic parameter audits and plain rural Bengali explanations without SHAP hallucinations.
- [Recommendation Engine Specification](file:///Users/kazi/Projects/RITUCAST/docs/analytics/recommendation-engine-specification.md): Complete specifications for `RULE-IRR-01` through `RULE-TMP-02`.
- [Analytics Output Contracts](file:///Users/kazi/Projects/RITUCAST/docs/analytics/analytics-output-contracts.md): Pydantic v2 schemas and JSON contracts feeding into Phase 10 API.
- [Uncertainty & Missing Data Handling](file:///Users/kazi/Projects/RITUCAST/docs/analytics/uncertainty-and-missing-data.md): 7 missing data states, suppression triggers, and epistemic uncertainty framing.
- [Analytics Testing Strategy](file:///Users/kazi/Projects/RITUCAST/docs/analytics/analytics-testing-strategy.md): Unit, rule, benchmark, and integration test specifications.
- [Reproducibility & Performance](file:///Users/kazi/Projects/RITUCAST/docs/analytics/reproducibility-and-performance.md): Deterministic execution, $<50\text{ms}$ latency, and $<35\text{MB}$ memory footprint.

### Phase 10: Backend API and Service Layer
- [Backend Architecture](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md): FastAPI modular design, repository pattern, and service boundaries.
- [API Specification](file:///Users/kazi/Projects/RITUCAST/docs/backend/api-specification.md): REST protocols, base URLs, 4-tier separation, and safety rules.
- [API Endpoints Catalog](file:///Users/kazi/Projects/RITUCAST/docs/backend/api-endpoints.md): Full contracts for all 11 endpoints with request/response examples.
- [Request Validation & Error Handling](file:///Users/kazi/Projects/RITUCAST/docs/backend/request-validation-and-errors.md): Centralized error translation and immutable envelopes.
- [Security & Configuration Guide](file:///Users/kazi/Projects/RITUCAST/docs/backend/security-and-configuration.md): Pydantic settings, CORS origin restrictions, and threat model.
- [Performance & Resource Management](file:///Users/kazi/Projects/RITUCAST/docs/backend/performance-and-resource-management.md): In-memory caching, latency benchmarks (<20ms), and 3G budget.
- [Local Development Guide](file:///Users/kazi/Projects/RITUCAST/docs/backend/local-development.md): Uvicorn commands, curl examples, and testing instructions.
- [Phase 9 Integration Contract](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-9-integration-contract.md): Verification contract with Phase 9 analytics engine.
- [Data Provenance & Quality Guide](file:///Users/kazi/Projects/RITUCAST/docs/backend/data-provenance-and-quality.md): Upstream dataset freshness and physical bound audits.
- [Known Limitations & Scope Boundaries](file:///Users/kazi/Projects/RITUCAST/docs/backend/known-limitations.md): Explicit non-goals (`DEC-06`) and pilot boundaries.
- [OpenAPI 3.0 Schema Artifact](file:///Users/kazi/Projects/RITUCAST/docs/backend/openapi.json): Auto-generated machine-readable schema.

### Phase 11: Frontend Application and User Experience
- [Frontend Architecture](file:///Users/kazi/Projects/RITUCAST/docs/frontend/phase-11-frontend-architecture.md): React 19 + TypeScript + Vite architecture, 4-tier taxonomy, and 3G budget.
- [Information Architecture](file:///Users/kazi/Projects/RITUCAST/docs/frontend/information-architecture.md): Navigation blueprints, sitemap, and operational card hierarchies.
- [Design System & Tokens](file:///Users/kazi/Projects/RITUCAST/docs/frontend/design-system.md): Vanilla CSS custom properties, high-contrast outdoor tokens, and Bangla typography.
- [Component Structure](file:///Users/kazi/Projects/RITUCAST/docs/frontend/component-structure.md): Component catalog, props interfaces, and view specifications.
- [Backend Integration Contract](file:///Users/kazi/Projects/RITUCAST/docs/frontend/backend-integration.md): REST endpoint mapping, query parameters, and envelope unwrapping.
- [API Client & Error Handling](file:///Users/kazi/Projects/RITUCAST/docs/frontend/api-client-and-error-handling.md): Centralized error parsing, offline detection, and stale data prevention.
- [Geographic & Temporal Display](file:///Users/kazi/Projects/RITUCAST/docs/frontend/geographic-and-temporal-display.md): BBS GeoCode handling, spatial resolution notices, and BST timezones.
- [User Workflows](file:///Users/kazi/Projects/RITUCAST/docs/frontend/user-workflows.md): Step-by-step journeys for Barind farmers, Haor SAAOs, and researchers.
- [Accessibility Compliance](file:///Users/kazi/Projects/RITUCAST/docs/frontend/accessibility.md): WCAG 2.2 AA audit, visible focus rings, ARIA roles, and reduced motion.
- [Responsive Design](file:///Users/kazi/Projects/RITUCAST/docs/frontend/responsive-design.md): Viewport adaptations, mobile touch targets (48px), and tablet ergonomics.
- [Visualization Guidelines](file:///Users/kazi/Projects/RITUCAST/docs/frontend/visualization-guidelines.md): Non-exaggerated gauges, QPF rainfall bars, and exclusion of SHAP.
- [Local Development Guide](file:///Users/kazi/Projects/RITUCAST/docs/frontend/local-development.md): Vite dev server, scripts catalog, and proxy configuration.
- [Testing & Quality Validation](file:///Users/kazi/Projects/RITUCAST/docs/frontend/testing-and-validation.md): 14 Vitest tests, bundle metrics (88.6 kB gzip), and verification logs.
- [Known Limitations & Boundaries](file:///Users/kazi/Projects/RITUCAST/docs/frontend/known-limitations.md): Pilot boundaries, deferrals (Maps to Phase 12), and non-goals (`DEC-06`).

### Phase 12: End-to-End Integration and System Validation
- [System Integration Overview](file:///Users/kazi/Projects/RITUCAST/docs/integration/phase-12-system-integration-overview.md): Integrated 5-tier architecture, verified boundaries, and DEC-06/08/10/17 enforcement.
- [Component Interface Inventory](file:///Users/kazi/Projects/RITUCAST/docs/integration/component-interface-inventory.md): Ingestion, analytics, 13 REST API endpoints, and React view components.
- [End-to-End Data Flow](file:///Users/kazi/Projects/RITUCAST/docs/integration/end-to-end-data-flow.md): Sequence diagrams, physical data transformations, and client lifecycle.
- [Data Contracts & Schemas](file:///Users/kazi/Projects/RITUCAST/docs/integration/data-contracts-and-schemas.md): Parquet feature schemas, REST JSON payloads, and error envelopes.
- [Validation Strategy](file:///Users/kazi/Projects/RITUCAST/docs/testing/phase-12-validation-strategy.md): Testing matrix, acceptance criteria, and 4 scientific quality gates.
- [End-to-End Test Guide](file:///Users/kazi/Projects/RITUCAST/docs/testing/end-to-end-test-guide.md): Test commands, environment setup, and full-stack local execution instructions.
- [Test Fixtures & Mock Data Guide](file:///Users/kazi/Projects/RITUCAST/docs/testing/test-fixtures-and-mock-data.md): Fixture inventory and boundary isolation from live data.
- [Live Data Smoke Tests](file:///Users/kazi/Projects/RITUCAST/docs/testing/live-data-smoke-tests.md): Live query protocols against Open-Meteo and NASA POWER with offline resilience.
- [Known Test Limitations](file:///Users/kazi/Projects/RITUCAST/docs/testing/known-test-limitations.md): Headless browser constraints, satellite tile sizes, and BMD telemetry status.
- [Environment Reproducibility Guide](file:///Users/kazi/Projects/RITUCAST/docs/operations/environment-reproducibility.md): Clean machine installation steps and config management.
- [Error Handling and Recovery](file:///Users/kazi/Projects/RITUCAST/docs/operations/error-handling-and-recovery.md): Failure scenarios, safety suppression, and client resilience.
- [Performance Findings](file:///Users/kazi/Projects/RITUCAST/docs/operations/phase-12-performance-findings.md): Bundle payload audit (307.5 kB / 89.3 kB gzip vs 1.5 MB budget), API latencies.
- [Security Findings](file:///Users/kazi/Projects/RITUCAST/docs/operations/phase-12-security-findings.md): Credential hygiene, Pydantic input validation, and traceback sanitization.

### Phase 13: Deployment Architecture & Production Readiness
- [Deployment Architecture](file:///Users/kazi/Projects/RITUCAST/docs/deployment/phase-13-deployment-architecture.md): Serverless decoupled container architecture on Cloud Run (`asia-south1`).
- [Hosting Options Comparison](file:///Users/kazi/Projects/RITUCAST/docs/deployment/hosting-options-comparison.md): Evaluation of Cloud Run, ECS Fargate, Fly.io/Render, and VPS.
- [Deployment Topology](file:///Users/kazi/Projects/RITUCAST/docs/deployment/deployment-topology.md): Network boundaries, ingress, ports, and internal routing.
- [Deployment Decisions](file:///Users/kazi/Projects/RITUCAST/docs/deployment/deployment-decisions.md): Formal ADRs (`DEC-51`, `DEC-52`, `DEC-53`).
- [Build & Runtime Configuration](file:///Users/kazi/Projects/RITUCAST/docs/deployment/build-and-runtime-configuration.md): Packaging and execution SOPs for backend and frontend.
- [Environment Variables](file:///Users/kazi/Projects/RITUCAST/docs/deployment/environment-variables.md): Reference for configuration variables and zero-secret architecture.
- [Data and Model Artifacts](file:///Users/kazi/Projects/RITUCAST/docs/deployment/data-and-model-artifacts.md): In-image Parquet packaging (<110KB) and integrity probes.
- [Containerization](file:///Users/kazi/Projects/RITUCAST/docs/deployment/containerization.md): Multi-stage Dockerfile specifications and non-root execution.
- [Health Checks & Logging](file:///Users/kazi/Projects/RITUCAST/docs/deployment/health-checks-and-logging.md): `/health`, `/ready`, structured logging, and alerts.
- [Security Checklist](file:///Users/kazi/Projects/RITUCAST/docs/deployment/security-checklist.md): Threat model, CSP/HSTS headers, and non-root UID 10001 audit.
- [Resource & Cost Considerations](file:///Users/kazi/Projects/RITUCAST/docs/deployment/resource-and-cost-considerations.md): Memory profiling and Cloud Run free-tier budget model ($0 to $5/month).
- [Backup & Recovery](file:///Users/kazi/Projects/RITUCAST/docs/deployment/backup-and-recovery.md): Stateless disaster recovery plan (RTO <60s, RPO 0s).
- [Rollback Procedure](file:///Users/kazi/Projects/RITUCAST/docs/deployment/rollback-procedure.md): Instant revision traffic shifts (<2s) and canary rollout SOP.
- [Troubleshooting Runbook](file:///Users/kazi/Projects/RITUCAST/docs/deployment/troubleshooting.md): Operational diagnosis and remediation for common alerts.
- [Deployment Procedure](file:///Users/kazi/Projects/RITUCAST/docs/deployment/deployment-procedure.md): Step-by-step automated (`deploy.sh`) and manual cloud rollout.
- [Deployment Validation](file:///Users/kazi/Projects/RITUCAST/docs/deployment/deployment-validation.md): Local container build and Docker Compose verification report.
- [CI/CD Workflow](file:///Users/kazi/Projects/RITUCAST/docs/deployment/ci-cd-workflow.md): GitHub Actions automation pipeline architecture and gates.
- [Known Limitations](file:///Users/kazi/Projects/RITUCAST/docs/deployment/known-limitations.md): Deferred items and external GCP credentials requirement.

### Phase 14: CI/CD Automation & Release Management
- [CI/CD Architecture](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/phase-14-cicd-architecture.md): Modular three-workflow GitHub Actions automation architecture.
- [Workflow Design & Dependencies](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/workflow-design.md): Dependency DAGs, parallel job execution, and step definitions.
- [Trigger & Branching Policy](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/trigger-and-branch-policy.md): Trunk-based development, path-based filtering, and branch protections.
- [Automated Quality Gates](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/automated-quality-gates.md): 12 blocking and non-blocking quality gate criteria and verification evidence.
- [Deterministic vs. Live Smoke Tests](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/deterministic-and-live-data-tests.md): Isolation of offline regression suite from third-party public satellite APIs.
- [Security Scanning](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/security-scanning.md): Working tree secret scanning, npm audit, and pip-audit vulnerability analysis.
- [Troubleshooting Failed Workflows](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/troubleshooting-failed-workflows.md): Operational diagnosis and remediation runbook.
- [Deployment Workflow](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/deployment-workflow.md): Tag-driven release packaging and approval-gated Cloud Run rollout.
- [Environment Separation](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/environment-separation.md): Isolation between local development, CI runners, staging, and production.
- [Secrets & Permissions](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/secrets-and-permissions.md): Least-privilege token permissions and Google Cloud Workload Identity Federation.
- [Known CI/CD Limitations](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/known-limitations.md): Deferred capabilities and remote GitHub runner prerequisites.
- [Versioning Strategy](file:///Users/kazi/Projects/RITUCAST/docs/releases/versioning-strategy.md): Semantic Versioning 2.0.0 guidelines and tag conventions.
- [Release Process SOP](file:///Users/kazi/Projects/RITUCAST/docs/releases/release-process.md): Step-by-step release lifecycle and verification SOP.
- [Release Artifacts](file:///Users/kazi/Projects/RITUCAST/docs/releases/release-artifacts.md): Release tarball, OpenAPI schema, and container image inventory.
- [Release Notes Template](file:///Users/kazi/Projects/RITUCAST/docs/releases/release-notes.md): Plain-language Bangla and technical communication standards.
- [Rollback & Recovery](file:///Users/kazi/Projects/RITUCAST/docs/releases/rollback-and-recovery.md): Instant Cloud Run revision rollback (<2s) and post-incident review SOP.

### Phase 15: Security, Privacy & Responsible Agricultural Intelligence
- [Baseline Security Assessment](file:///Users/kazi/Projects/RITUCAST/docs/security/phase-15-security-assessment.md): Audit methodology, findings summary, and architectural trust boundaries.
- [Threat Model & STRIDE Analysis](file:///Users/kazi/Projects/RITUCAST/docs/security/threat-model.md): Asset inventory, threat scenarios, and risk rating matrix.
- [Security Boundaries & Trust Architecture](file:///Users/kazi/Projects/RITUCAST/docs/security/security-boundaries.md): 5-zone trust architecture and network boundaries.
- [Security Findings Register](file:///Users/kazi/Projects/RITUCAST/docs/security/security-findings-register.md): Formal log of all findings, severity levels, and remediations.
- [API & Backend Security](file:///Users/kazi/Projects/RITUCAST/docs/security/api-security.md): OWASP headers, payload size limiting, in-memory rate limiting, and path traversal guards.
- [Frontend Security & User Input](file:///Users/kazi/Projects/RITUCAST/docs/security/frontend-security.md): XSS immunity, zero dangerouslySetInnerHTML, and anti-deception mock fallback policy.
- [Secrets & Supply Chain Management](file:///Users/kazi/Projects/RITUCAST/docs/security/secrets-and-dependency-management.md): Secret hygiene, pip-audit and npm audit vulnerability analysis, and container hardening.
- [Secure Configuration](file:///Users/kazi/Projects/RITUCAST/docs/security/secure-configuration.md): Environment separation, secure defaults, and CORS restrictions.
- [Data Inventory & Privacy Classification](file:///Users/kazi/Projects/RITUCAST/docs/privacy/data-inventory.md): Comprehensive inventory, non-PII posture, and zero telemetry verification.
- [Data Handling & Retention Policy](file:///Users/kazi/Projects/RITUCAST/docs/privacy/data-handling-and-retention.md): Ephemeral request processing and logging privacy guarantees.
- [External Services & Data Sharing](file:///Users/kazi/Projects/RITUCAST/docs/privacy/external-services-and-data-sharing.md): Outbound transmission audit and prohibition of direct browser queries.
- [Dataset Licensing & Redistribution Review](file:///Users/kazi/Projects/RITUCAST/docs/data/dataset-licensing-and-redistribution-review.md): Open data license audit, caching rights, and UI attribution.
- [Agricultural Recommendation Safeguards](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/agricultural-recommendation-safeguards.md): 4-tier taxonomy, contextual gating (DEC-17), suppression (DEC-10), and anti-overconfidence copy.
- [Model Limitations & Uncertainty](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/model-limitations-and-uncertainty.md): Physical equation bounds, epistemic uncertainty, and non-causal explainability.
- [Geographic Coverage & Fairness](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/geographic-coverage-and-fairness.md): Spatial resolution disparities, regional average labeling, and equitable access.
- [Appropriate Use & Misuse Prevention](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/appropriate-use-and-misuse-prevention.md): Non-goals (DEC-06), loan underwriting prohibitions, and agronomic primacy.
- [Security Test Plan](file:///Users/kazi/Projects/RITUCAST/docs/security/security-test-plan.md): Automated verification coverage across pytest and vitest.
- [Security Remediation Record](file:///Users/kazi/Projects/RITUCAST/docs/security/security-remediation-record.md): Component-by-component engineering fixes and code modifications.
- [Remaining Risks](file:///Users/kazi/Projects/RITUCAST/docs/security/remaining-risks.md): Residual risk register, mitigating factors, and post-Phase 15 follow-up.

### Planning, Governance & Quality Registers
- [Agent Operating Instructions (AGENTS.md)](file:///Users/kazi/Projects/RITUCAST/AGENTS.md): Project-wide AI operating principles, scope boundaries, and safety guardrails.
- [Phase 1–4 Continuity & Readiness Audit](file:///Users/kazi/Projects/RITUCAST/docs/project/phase-1-to-4-continuity-audit.md): Comprehensive pre-Phase 5 audit of artifacts, tests, data, and risks.
- [Assumptions Register](file:///Users/kazi/Projects/RITUCAST/docs/planning/assumptions-register.md): Tracked assumptions with verification paths (updated with ASM-22).
- [Risk Register](file:///Users/kazi/Projects/RITUCAST/docs/planning/risk-register.md): 52 prioritized risks with mitigations (updated with RSK-50 through RSK-52).
- [Decision Log](file:///Users/kazi/Projects/RITUCAST/docs/planning/decision-log.md): Architectural decisions log (updated with DEC-58 through DEC-61).
- [Master Project Roadmap](file:///Users/kazi/Projects/RITUCAST/docs/planning/roadmap.md): 18-phase lifecycle status.
- [Changelog (CHANGELOG.md)](file:///Users/kazi/Projects/RITUCAST/CHANGELOG.md): Keep a Changelog documentation for release v1.0.0.

### Phase Execution Packages
- **Phase 01 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/phase-plan.md) | [Research Notes](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/research-notes.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/validation-report.md) | [Handoff to Phase 2](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/handoff-to-phase-02.md)
- **Phase 02 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-02/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-02/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-02/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-02/validation-report.md) | [Handoff to Phase 3](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-02/handoff-to-phase-03.md)
- **Phase 03 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/readiness-assessment.md) | [Research Notes](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/research-notes.md) | [Verification Log](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/verification-log.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/validation-report.md) | [Handoff to Phase 4](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-03/handoff-to-phase-04.md)
- **Phase 04 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/readiness-assessment.md) | [Evidence Register](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/evidence-register.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/validation-report.md) | [Handoff to Phase 5](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/handoff-to-phase-05.md)
- **Phase 05 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/validation-report.md) | [Handoff to Phase 6](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/handoff-to-phase-06.md)
- **Phase 06 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-06/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-06/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-06/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-06/validation-report.md) | [Handoff to Phase 7](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-06/handoff-to-phase-07.md)
- **Phase 07 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-07/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-07/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-07/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-07/validation-report.md) | [Handoff to Phase 8](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-07/handoff-to-phase-08.md)
- **Phase 08 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-08/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-08/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-08/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-08/validation-report.md) | [Handoff to Phase 9](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-08/handoff-to-phase-09.md)
- **Phase 09 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-09/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-09/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-09/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-09/validation-report.md) | [Handoff to Phase 10](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-09/handoff-to-phase-10.md)
- **Phase 10 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-10/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-10/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-10/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-10/validation-report.md) | [Completion Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-10/phase-10-completion-report.md) | [Handoff to Phase 11](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-10/handoff-to-phase-11.md)
- **Phase 11 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-11/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-11/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-11/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-11/validation-report.md) | [Completion Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-11/phase-11-completion-report.md) | [Handoff to Phase 12](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-11/handoff-to-phase-12.md)
- **Phase 12 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-12/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-12/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-12/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-12/validation-report.md) | [Completion Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-12/phase-12-completion-report.md) | [Handoff to Phase 13](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-12/handoff-to-phase-13.md)
- **Phase 13 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-13/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-13/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-13/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-13/validation-report.md) | [Completion Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-13/phase-13-completion-report.md) | [Handoff to Phase 14](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-13/handoff-to-phase-14.md)
- **Phase 14 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-14/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-14/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-14/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-14/validation-report.md) | [Completion Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-14/phase-14-completion-report.md) | [Handoff to Phase 15](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-14/handoff-to-phase-15.md)
- **Phase 15 Package**: [Phase Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-15/phase-plan.md) | [Readiness Assessment](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-15/readiness-assessment.md) | [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-15/deliverables-checklist.md) | [Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-15/validation-report.md) | [Completion Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-15/phase-15-completion-report.md) | [Handoff to Phase 16](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-15/handoff-to-phase-16.md)

---

## 4. Repository Structure

```text
RITUCAST/
├── README.md
├── AGENTS.md
├── .editorconfig
├── .gitignore
├── api/
│   ├── config.py
│   ├── dependencies.py
│   ├── main.py
│   ├── data_access/
│   │   └── repository.py
│   ├── middleware/
│   │   └── error_handlers.py
│   ├── routers/
│   │   ├── health.py
│   │   ├── geo.py
│   │   ├── metadata.py
│   │   ├── weather.py
│   │   ├── water_balance.py
│   │   ├── flood_hazard.py
│   │   ├── advisories.py
│   │   ├── risk.py
│   │   └── provenance.py
│   └── schemas/
│       ├── common.py
│       ├── geo.py
│       ├── metadata.py
│       ├── indicators.py
│       ├── advisories.py
│       ├── risk.py
│       └── provenance.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── test/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── index.css
│   ├── index.html
│   └── vite.config.ts
├── configs/
│   └── datasets/
├── data/
│   ├── sample/
│   └── processed/
├── analytics/
├── pipelines/
├── tests/
│   ├── unit/
│   ├── spatial/
│   ├── temporal/
│   ├── failure/
│   ├── integration/
│   ├── analytics/
│   └── api/
└── docs/
    ├── project/
    ├── product/
    ├── requirements/
    ├── data/
    ├── science/
    ├── architecture/
    ├── ux/
    ├── design/
    ├── analytics/
    ├── backend/
    ├── frontend/
    ├── planning/
    └── phases/
        ├── phase-01/
        ├── ...
        ├── phase-10/
        └── phase-11/
```

---

## 5. Development Principles

1. **Disciplined Phase Execution**: No execution of subsequent phases without formal quality gate review.
2. **Scientific Transparency**: Clear separation of empirical observations, forecast models, and agronomic advisories.
3. **Data Protection**: Large raw datasets, satellite imagery caches, and secrets are excluded from Git via `.gitignore`.

