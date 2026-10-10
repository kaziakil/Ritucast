# Ritucast: 18-Phase Project Master Roadmap

## 1. Governance and Phase Transition Rules

The Ritucast platform is developed across an 18-phase structured engineering lifecycle. To guarantee software reliability, scientific credibility, and user-centered design, the project strictly observes the following governance policies:

1. **Sequential Phase Gating**: A phase may only transition to *In Progress* after the preceding phase achieves a formal **PASS** on all acceptance criteria.
2. **Zero Premature Implementation**: Architecture, data pipeline engineering, frontend design, and backend development are restricted to their assigned phases.
3. **Traceability**: Every phase must publish a `phase-plan.md`, `deliverables-checklist.md`, `validation-report.md`, and a formal `handoff-to-phase-XX.md`.

---

## 2. Master Phase Status Table

| Phase | Phase Name | Primary Focus & Deliverables | Current Status | Target Completion | Quality Gate Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | **Project Discovery and Problem Definition** | Agricultural problem inventory, user segments, vision, initial scope, pilot geography, risks, metrics. | **Completed** | 2026-10-10 | **PASS** |
| **02** | **Requirements and Product Strategy** | Detailed functional & non-functional requirements, user stories, user journey maps, product roadmap. | **Completed** | 2026-10-10 | **PASS** |
| **03** | **Dataset Research and Validation** | API auditing (NASA POWER, Sentinel-1/2, SMAP, GPM IMERG), spatial/temporal coverage, rate limits. | **Completed** | 2026-10-10 | **PASS** |
| **04** | **Agricultural Knowledge & Scientific Validation Planning** | Phenology rules, crop coefficients ($K_c$), FAO-56 Penman-Monteith calibration, agro-meteorological validation. | **Completed** | 2026-10-10 | **PASS** |
| **05** | **System Architecture & Technology Decisions** | High-level component architecture, tech stack selection, DB schemas, cloud hosting strategy. | **Completed** | 2026-10-10 | **PASS** |
| **06** | **Information Architecture & User Journey Design** | SAAO and Lead Farmer interaction flows, wireframes, screen hierarchy, notification blueprints. | **Completed** | 2026-10-10 | **PASS** |
| **07** | **Visual Design and Design System** | High-contrast mobile UI design tokens, Bangla typography, iconography, component library. | **Completed** | 2026-10-10 | **PASS** |
| **08** | **Data Ingestion & Processing Pipeline** | ETL pipelines, raster tiling, geospatial caching, automated cron jobs for weather and satellite updates. | **Completed** | 2026-10-10 | **PASS** |
| **09** | **Agricultural Analytics & Recommendation Engine** | Water balance calculation, flash-flood hazard score, advisory generator, explainability rules. | **Completed** | 2026-10-10 | **PASS** |
| **10** | **Backend and API Development** | REST APIs, Upazila query endpoints, health probes, indicators, advisory distribution services. | **Completed** | 2026-10-10 | **PASS** |
| **11** | **Frontend Development** | React 19 SPA/PWA, Vanilla CSS design system, 4-tier cards, contextual gating, analytical hubs. | **Completed** | 2026-10-10 | **PASS** |
| **12** | **End-to-End Integration & System Validation** | Full-stack data flow verification (Ingestion -> Feature Tables -> Analytics -> REST API -> React PWA), 112 automated tests, live smoke tests, bundle budget audit. | **Completed** | 2026-10-10 | **PASS** |
| **13** | **Maps and Interactive Visualizations** | Vector tile overlays, regional hazard maps, satellite moisture anomaly charts. | **Pending** | Next Phase | Not Started |
| **14** | **Usability, Accessibility & Performance** | Field testing with SAAOs, 3G performance tuning, bundle size minimization (<1.5MB). | **Pending** | Scheduled | Not Started |
| **15** | **Scientific & Agricultural Validation** | Correlation analysis with BMD rain gauges, BWDB flood logs, and BRRI field crop stages. | **Pending** | Scheduled | Not Started |
| **16** | **Deployment & Production Readiness** | Production deployment (Cloud Run / CDN), SSL, monitoring alerts, SLA definition. | **Pending** | Scheduled | Not Started |
| **17** | **User Feedback & Iterative Improvement** | Pilot deployment in Barind and Haor zones; farmer feedback collection and heuristic tuning. | **Pending** | Scheduled | Not Started |
| **18** | **Expansion & Long-Term Maintenance** | Expansion to coastal saline and central floodplain AEZs; minor crop calendar onboarding. | **Pending** | Scheduled | Not Started |

---

## 3. Phase Milestones & Progress Tracking

- **Phase 01 (Project Discovery)**: Completed 2026-10-10 (`1e4716b`–`b67f78e`). Quality Gate: **PASS**.
- **Phase 02 (Requirements & Strategy)**: Completed 2026-10-10 (`c7f8465`–`91f94ec`). Quality Gate: **PASS**.
- **Phase 03 (Dataset Research & Validation)**: Completed 2026-10-10 (`5975248`–`fce9064`). Quality Gate: **PASS**.
- **Phase 04 (Agricultural Knowledge & Scientific Validation Planning)**: Completed 2026-10-10. All 12 science specifications, rule catalog, validation plan, and safety frameworks verified. Quality Gate: **PASS**.
- **Phase 05 (System Architecture & Technology Decisions)**: Completed 2026-10-10. 12 architecture specifications, 9 ADRs, component contracts, testing strategy, and risk register verified. Quality Gate: **PASS**.
- **Phase 06 (Information Architecture & User Journey Design)**: Completed 2026-10-10. 14 UX specifications, sitemap, 6 critical journeys, page content blueprints, trust patterns, and WCAG accessibility standards verified. Quality Gate: **PASS**.
- **Phase 07 (Visual Design and Design System)**: Completed 2026-10-10 (`b1bc4e4`–`3d3cfec`). Visual identity, color system, typography hierarchy, layout grid, component system, data visualization rules, and design tokens verified. Quality Gate: **PASS**.
- **Phase 08 (Data Ingestion & Processing Pipeline)**: Completed 2026-10-10 (`2ab4588`–`3ea2689`). 12 data pipeline specifications, 8 ingestion adapters, Pydantic schemas, semantic bounds, Parquet feature tables, run manifests, and 25 automated tests verified. Quality Gate: **PASS**.
- **Phase 09 (Agricultural Analytics & Recommendation Engine)**: Completed 2026-10-10. 15 analytics specifications, FAO-56 Penman-Monteith ET0, dynamic Kc, soil water balance, Haor flood index, 5 master advisory rules, context gating (DEC-17), suppression middleware (DEC-10), and 35 automated analytics tests (60 total tests) verified. Quality Gate: **PASS**.
- **Phase 10 (Backend API and Service Layer)**: Completed 2026-10-10. 10 backend specifications, modular FastAPI app, in-memory data repository, 4-tier advisory endpoints, OpenAPI 3.0 specification, and 26 automated API tests (86 total repository tests) verified. Quality Gate: **PASS**.
- **Phase 11 (Frontend Application and User Experience)**: Completed 2026-10-10. React 19 SPA, Vanilla CSS design system, 14 frontend specifications, 12 integrated endpoints, 4-tier advisory cards, AWD gauge, flood index meter, 88.6 kB gzipped bundle, and 14 automated Vitest tests (100 total repository tests) verified. Quality Gate: **PASS**.
- **Phase 12 (End-to-End Integration and System Validation)**: Completed 2026-10-10. Complete multi-tier data flow traversal, resolution of repository path coercion (`DEF-12-01`) and UI confidence access (`DEF-12-02`), system E2E tests, live upstream smoke tests, frontend user journey tests, bundle payload audit (307.5 kB uncompressed / 89.3 kB gzip), and 112 automated tests passed (95 Python, 17 Vitest). Quality Gate: **PASS**.
- **Next Transition**: Awaiting formal project lead review to trigger **Phase 13**.



