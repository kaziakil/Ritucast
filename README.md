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
| :---: | :--- | :---: |
| **01** | **Project Discovery and Problem Definition** | **Completed (PASS)** |
| 02 | Requirements and Product Strategy | *Pending Review* |
| 03–18 | Dataset Validation through Long-Term Expansion | *Pending* |

Full details and phase governance rules can be viewed in the [Master Project Roadmap](file:///Users/kazi/Projects/RITUCAST/docs/planning/roadmap.md).

---

## 3. Project Documentation Index

The complete Phase 1 Project Discovery and Problem Definition deliverables are organized as follows:

### Strategic & Product Baseline
- [Project Overview](file:///Users/kazi/Projects/RITUCAST/docs/project/project-overview.md): Executive summary, purpose, and concept.
- [Problem Definition & Ranked Inventory](file:///Users/kazi/Projects/RITUCAST/docs/project/problem-definition.md): Evidence-based assessment of candidate problems.
- [Target User Analysis](file:///Users/kazi/Projects/RITUCAST/docs/project/target-users.md): Multi-segment evaluation, dual-anchor model (SAAOs + Lead Farmers).
- [Product Vision & Positioning](file:///Users/kazi/Projects/RITUCAST/docs/project/product-vision.md): Vision, mission, 10 core principles, and DSS positioning.
- [Initial Product Scope](file:///Users/kazi/Projects/RITUCAST/docs/project/initial-scope.md): Essential capabilities, non-goals, and explicit exclusions.
- [Geographic & Agricultural Scope](file:///Users/kazi/Projects/RITUCAST/docs/project/geographic-agricultural-scope.md): AEZ assessment and dual-zone pilot testbeds.
- [Success Metrics Framework](file:///Users/kazi/Projects/RITUCAST/docs/project/success-metrics.md): 4-tier measurement pyramid from tech to agronomic impact.
- [Long-Term Product Direction](file:///Users/kazi/Projects/RITUCAST/docs/project/long-term-direction.md): 3 strategic horizons and future expansion areas.

### Planning & Governance
- [Assumptions Register](file:///Users/kazi/Projects/RITUCAST/docs/planning/assumptions-register.md): 8 tracked assumptions with upgrade criteria.
- [Risk Register](file:///Users/kazi/Projects/RITUCAST/docs/planning/risk-register.md): 10 prioritized risks across product, data, science, tech, and adoption.
- [Decision Log](file:///Users/kazi/Projects/RITUCAST/docs/planning/decision-log.md): Architectural decisions and trade-offs.
- [Master Project Roadmap](file:///Users/kazi/Projects/RITUCAST/docs/planning/roadmap.md): 18-phase lifecycle status.

### Phase 1 Execution & Quality Assurance
- [Phase 1 Plan](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/phase-plan.md): Objectives and boundaries.
- [Research Notes & Citations](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/research-notes.md): Evidence base from BBS, DAE, BMD, BWDB, BRRI, FAO, NASA.
- [Deliverables Checklist](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/deliverables-checklist.md): 15 deliverables & 17 criteria audit.
- [Phase 1 Validation Report](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/validation-report.md): Formal quality gate audit (**PASS**).
- [Handoff to Phase 2](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-01/handoff-to-phase-02.md): Handoff package for Requirements and Product Strategy.

---

## 4. Repository Structure

```text
RITUCAST/
├── README.md
├── .gitignore
├── docs/
│   ├── project/
│   │   ├── project-overview.md
│   │   ├── problem-definition.md
│   │   ├── target-users.md
│   │   ├── product-vision.md
│   │   ├── initial-scope.md
│   │   ├── geographic-agricultural-scope.md
│   │   ├── success-metrics.md
│   │   └── long-term-direction.md
│   ├── planning/
│   │   ├── assumptions-register.md
│   │   ├── risk-register.md
│   │   ├── decision-log.md
│   │   └── roadmap.md
│   └── phases/
│       └── phase-01/
│           ├── phase-plan.md
│           ├── research-notes.md
│           ├── deliverables-checklist.md
│           ├── validation-report.md
│           └── handoff-to-phase-02.md
```

---

## 5. Development Principles

1. **Disciplined Phase Execution**: No execution of subsequent phases without formal quality gate review.
2. **Scientific Transparency**: Clear separation of empirical observations, forecast models, and agronomic advisories.
3. **Data Protection**: Large raw datasets, satellite imagery caches, and secrets are excluded from Git via `.gitignore`.
