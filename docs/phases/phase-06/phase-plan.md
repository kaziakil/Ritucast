# Phase 6 Plan: Information Architecture and User Journey Design

## 1. Executive Summary & Phase Mission

- **Phase ID**: Phase 06 — Information Architecture and User Journey Design
- **Phase Lead**: Senior Product Designer & UX Architect (Google Antigravity)
- **Lifecycle Context**: Follows [Phase 05: System Architecture & Technology Decisions](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-05/validation-report.md); precedes Phase 07: Visual Design & Design System.
- **Mission Statement**: Transform the verified agricultural problem scope, user requirements, scientific rules, and system architecture into an intuitive, accessible, and scientifically honest information architecture. Define what users need to find, understand, and accomplish across Bangladesh's dual-zone pilot testbeds (High Barind Tract and Haor Basin).

---

## 2. Work Breakdown Structure (WBS)

```
Phase 06: Information Architecture & User Journey Design
├── 1. Foundational UX Strategy & Governance
│   ├── Readiness Assessment & Prerequisite Audit (docs/phases/phase-06/readiness-assessment.md)
│   ├── UX Design Principles & Compliance Rules (docs/ux/ux-principles.md)
│   ├── User Groups, Personas & Constraints (docs/ux/user-groups-and-needs.md)
│   └── Core Product Tasks & Priorities (docs/ux/core-user-tasks.md)
├── 2. Structural Information Architecture
│   ├── Information Architecture Specification (docs/ux/information-architecture.md)
│   ├── Complete Application Sitemap (docs/ux/sitemap.md)
│   └── Standalone Sitemap Diagram (docs/ux/diagrams/sitemap.mmd)
├── 3. Interaction Flows & Page Blueprints
│   ├── Critical User Journeys (A through F) (docs/ux/user-journeys.md)
│   ├── Page-Level Content & Layout Specifications (docs/ux/page-requirements.md)
│   └── Geographic Context & Selection Model (docs/ux/geographic-context-and-selection.md)
├── 4. Scientific Communication & Trust Guardrails
│   ├── Agricultural Insight Information Hierarchy (docs/ux/agricultural-insight-information-model.md)
│   ├── Trust, Uncertainty & Suppression UX Patterns (docs/ux/trust-and-uncertainty-patterns.md)
│   ├── Accessibility, Bangla Localization & Connectivity (docs/ux/accessibility-localization-and-connectivity.md)
│   ├── UX State & Interaction Matrix (docs/ux/interaction-and-state-specification.md)
│   └── UX Success Metrics & Evaluation Protocol (docs/ux/ux-success-metrics.md)
└── 5. Quality Review & Phase Transition
    ├── Deliverables Checklist (docs/phases/phase-06/deliverables-checklist.md)
    ├── Phase 6 Validation Report (docs/phases/phase-06/validation-report.md)
    ├── Handoff Package to Phase 7 (docs/phases/phase-06/handoff-to-phase-07.md)
    └── Governance Registers & Master README Updates
```

---

## 3. Strict Scope Boundaries & Governance Rules

In strict adherence to [AGENTS.md](file:///Users/kazi/Projects/RITUCAST/AGENTS.md):
1. **Zero Premature Implementation**: No visual design tokens (colors, fonts, CSS) from Phase 7; no React code or components from Phase 11; no backend API development from Phase 10.
2. **Four-Tier Information Taxonomy (`DEC-08`)**: All wireframe content structures must visually partition Empirical Observations, Derived Indicators, Probabilistic Forecasts, and Actionable Recommendations.
3. **Mandatory Contextual Gating (`DEC-17`)**: User flows must guarantee that Upazila, Crop, and Phenological Stage selections are confirmed prior to rendering Tier 4 recommendation cards.
4. **Automated Suppression Fallbacks (`DEC-10`, `ADR-08`)**: Explicit fallback states and messaging must be specified for stale data (>36h) or high ensemble spread (>50%).
5. **Mobile-First Budget (`DEC-09`, `ADR-03`)**: Card-first critical path; MapLibre vector maps deferred to secondary diagnostic views to ensure bundle $\le 1.5\text{MB}$ and peak heap $\le 45\text{MB}$.

---

## 4. Phase 6 Deliverables Tracking

| Deliverable ID | Document Path | Core Scope |
| :--- | :--- | :--- |
| `DEL-06-01` | `docs/ux/ux-principles.md` | 12 Binding UX principles and compliance evaluation criteria. |
| `DEL-06-02` | `docs/ux/user-groups-and-needs.md` | Primary, secondary, future, and excluded user groups with constraints. |
| `DEL-06-03` | `docs/ux/core-user-tasks.md` | Must-have vs optional product tasks linked to requirements. |
| `DEL-06-04` | `docs/ux/information-architecture.md` | Primary/secondary navigation, tabs, filters, and structural hierarchy. |
| `DEL-06-05` | `docs/ux/sitemap.md` | Application sitemap distinguishing release vs future views. |
| `DEL-06-06` | `docs/ux/diagrams/sitemap.mmd` | Standalone Mermaid diagram for visual sitemap rendering. |
| `DEL-06-07` | `docs/ux/user-journeys.md` | Step-by-step user journeys (A–F) with Mermaid flowcharts. |
| `DEL-06-08` | `docs/ux/page-requirements.md` | Page-level content blocks, controls, and responsive layouts. |
| `DEL-06-09` | `docs/ux/geographic-context-and-selection.md` | Geographic hierarchy, default context, persistence, and boundary rules. |
| `DEL-06-10` | `docs/ux/agricultural-insight-information-model.md` | Information model for 4-tier cards, Bangla copy, and field verification. |
| `DEL-06-11` | `docs/ux/trust-and-uncertainty-patterns.md` | Presentation patterns for freshness, suppression, and uncertainty. |
| `DEL-06-12` | `docs/ux/accessibility-localization-and-connectivity.md` | WCAG 2.2 AA targets, Bangla localization, and 3G offline caching. |
| `DEL-06-13` | `docs/ux/interaction-and-state-specification.md` | Reusable state matrix (loading, empty, stale, error, suppressed). |
| `DEL-06-14` | `docs/ux/ux-success-metrics.md` | Measurable UX usability metrics and evaluation protocols. |
| `DEL-06-15` | `docs/phases/phase-06/handoff-to-phase-07.md` | Actionable handoff package to Visual Design & Design System. |
