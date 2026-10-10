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
| **03** | **Dataset Research and Validation** | API auditing (NASA POWER, Sentinel-1/2, SMAP, GPM IMERG), spatial/temporal coverage, rate limits. | **Pending** | Next Phase | Not Started |
| **04** | **Agricultural Knowledge & Scientific Validation Planning** | Phenology rules, crop coefficients ($K_c$), FAO-56 Penman-Monteith calibration, agro-meteorological validation. | **Pending** | Scheduled | Not Started |
| **05** | **System Architecture & Technology Decisions** | High-level component architecture, tech stack selection, DB schemas, cloud hosting strategy. | **Pending** | Scheduled | Not Started |
| **06** | **Information Architecture & User Journey Design** | SAAO and Lead Farmer interaction flows, wireframes, screen hierarchy, notification blueprints. | **Pending** | Scheduled | Not Started |
| **07** | **Visual Design and Design System** | High-contrast mobile UI design tokens, Bangla typography, iconography, component library. | **Pending** | Scheduled | Not Started |
| **08** | **Data Ingestion & Processing Pipeline** | ETL pipelines, raster tiling, geospatial caching, automated cron jobs for weather and satellite updates. | **Pending** | Scheduled | Not Started |
| **09** | **Agricultural Analytics & Recommendation Engine** | Water balance calculation, flash-flood hazard score, advisory generator, explainability rules. | **Pending** | Scheduled | Not Started |
| **10** | **Backend and API Development** | REST/GraphQL APIs, upazila query endpoints, authentication, advisory distribution services. | **Pending** | Scheduled | Not Started |
| **11** | **Frontend Development** | PWA implementation, offline service workers, responsive card views, localization engine. | **Pending** | Scheduled | Not Started |
| **12** | **Maps and Interactive Visualizations** | Vector tile overlays, regional hazard maps, satellite moisture anomaly charts. | **Pending** | Scheduled | Not Started |
| **13** | **Integration and End-to-End Testing** | Automated integration test suite, pipeline-to-client data verification, load testing. | **Pending** | Scheduled | Not Started |
| **14** | **Usability, Accessibility & Performance** | Field testing with SAAOs, 3G performance tuning, bundle size minimization (<1.5MB). | **Pending** | Scheduled | Not Started |
| **15** | **Scientific & Agricultural Validation** | Correlation analysis with BMD rain gauges, BWDB flood logs, and BRRI field crop stages. | **Pending** | Scheduled | Not Started |
| **16** | **Deployment & Production Readiness** | Production deployment (Cloud Run / CDN), SSL, monitoring alerts, SLA definition. | **Pending** | Scheduled | Not Started |
| **17** | **User Feedback & Iterative Improvement** | Pilot deployment in Barind and Haor zones; farmer feedback collection and heuristic tuning. | **Pending** | Scheduled | Not Started |
| **18** | **Expansion & Long-Term Maintenance** | Expansion to coastal saline and central floodplain AEZs; minor crop calendar onboarding. | **Pending** | Scheduled | Not Started |

---

## 3. Phase Milestones & Progress Tracking

- **Phase 01 (Project Discovery)**: Completed 2026-10-10 (`1e4716b`–`b67f78e`). Quality Gate: **PASS**.
- **Phase 02 (Requirements & Strategy)**: Completed 2026-10-10. All PRDs, NFRs, RTMs, and handoff packages validated. Quality Gate: **PASS**.
- **Next Transition**: Awaiting formal project lead review to trigger **Phase 03: Dataset Research and Validation**.
