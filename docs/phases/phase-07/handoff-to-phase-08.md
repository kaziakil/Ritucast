# Phase 7 to Phase 8 Handoff Specification

## 1. Executive Summary & Purpose

- **From**: Phase 07 — Visual Design and Design System
- **To**: Phase 08 — Data Ingestion and Processing Pipeline
- **Date**: 2026-10-10
- **Status**: **READY FOR PHASE 08 INITIATION**

This document establishes the binding design constraints, data presentation requirements, and provenance schemas created during Phase 7 that directly govern the engineering of data pipelines in Phase 8 and subsequent implementation phases.

---

## 2. Cross-Phase Implementation Matrix

| Phase | Phase Name | How Phase 7 Design System Informs This Phase | Core Spec to Consult |
| :--- | :--- | :--- | :--- |
| **Phase 08** | **Data Ingestion & Processing Pipeline** | Ingestion tasks must preserve exact audit fields (`retrieval_timestamp`, `source_id`, `quality_flags`) displayed on UI cards; output Upazila zonal statistics matching UI precision. | [scientific-transparency-patterns.md](file:///Users/kazi/Projects/RITUCAST/docs/design/scientific-transparency-patterns.md) |
| **Phase 09** | **Agricultural Analytics & Recommendation Engine** | Analytics models must output quantitative indicators formatted for UI visualization: $D_t$ vs $RAW$ for Barind gauge; $I_{\text{flood}}$ for Haor threat meter; suppression flags for high ensemble spread. | [data-visualization-guidelines.md](file:///Users/kazi/Projects/RITUCAST/docs/design/data-visualization-guidelines.md) |
| **Phase 10** | **Backend and API Development** | REST API response payloads must match the data attributes required by the standard 5-section card and emit HTTP error codes mapped to the 14 UI interaction states. | [component-system.md](file:///Users/kazi/Projects/RITUCAST/docs/design/component-system.md), [feedback-and-state-patterns.md](file:///Users/kazi/Projects/RITUCAST/docs/design/feedback-and-state-patterns.md) |
| **Phase 11** | **Frontend Development** | Directly builds `apps/web/src/index.css` using the Vanilla CSS custom properties blueprint; builds React components matching `CMP-CARD-01` through `CMP-MOD-01`. | [design-tokens.md](file:///Users/kazi/Projects/RITUCAST/docs/design/design-tokens.md), [component-system.md](file:///Users/kazi/Projects/RITUCAST/docs/design/component-system.md) |
| **Phase 12** | **Maps & Interactive Visualizations** | MapLibre vector styling must adhere to the discrete color stops, Upazila polygon highlights, and coarse resolution disclaimer standards. | [data-visualization-guidelines.md](file:///Users/kazi/Projects/RITUCAST/docs/design/data-visualization-guidelines.md) |

---

## 3. Specific Mandates for the Incoming Phase 8 Data Engineering Team

1. **Mandatory Provenance Payload Preservation**:
   - Every Celery ingestion task (NASA POWER, Sentinel-1, GPM, BMD) must capture:
     - `source_id`: Canonical provider name (e.g., `NASA_POWER`, `BMD_SYNOPTIC`, `ESA_SENTINEL_1`).
     - `observation_timestamp`: ISO-8601 UTC timestamp of sensing.
     - `retrieval_timestamp`: ISO-8601 UTC timestamp of pipeline fetch.
     - `quality_flags`: Sensor validity bitmask (e.g., cloud cover flag, missing band flag).
     - `spatial_coverage_pct`: Float percentage ($0.0–100.0\%$) of valid pixels inside Upazila boundary.
2. **Display Precision Alignment**:
   - Pipeline aggregation algorithms must output rounded numerical statistics aligned with UI formatting:
     - Temperature: 1 decimal place (e.g., $28.5^\circ\text{C}$).
     - Rainfall: 1 decimal place (e.g., $18.2\text{ mm}$).
     - Evapotranspiration ($ET_0$): 1 decimal place (e.g., $4.2\text{ mm/day}$).
     - Hazard Index ($I_{\text{flood}}$): 2 decimal places (e.g., $0.68$).
3. **Asymmetric Ingestion Cadence (`ADR-07`)**:
   - Barind irrigation pipelines run on a daily 24-hour cycle at 06:00 BST.
   - Haor flash-flood pipelines run on a 6-hourly cycle (00:00, 06:00, 12:00, 18:00 BST) to ensure flood threat meters reflect transboundary Meghalaya rainfall surges in near-real-time.

---

## 4. Verification Sign-Off

- **Phase 7 Lead**: Approved (Visual Design and Design System Complete)
- **Phase 8 Readiness**: **GREEN (Unblocked — Ready for ETL Pipeline Development)**
