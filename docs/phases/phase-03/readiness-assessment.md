# Phase 3: Readiness Assessment & Requirements Baseline Extraction

## 1. Executive Summary

- **Evaluation Date**: 2026-10-10
- **Auditor**: Senior Earth Observation Scientist & Agricultural Data Engineer (Google Antigravity)
- **Phase 2 Baseline Evaluation Outcome**: **READY (PASS)**
- **Baseline Integrity**: Git commit `91f94ec` contains verified PRD, NFRs, Feature Prioritization Matrix, Product-Level Data Requirements (`DR-MET`, `DR-PCP`, `DR-SMC`, `DR-SAR`, `DR-AGR`), and the Phase 3 Handoff Specification.

Phase 2 defined exactly **what data the platform requires** and **which user decisions each variable supports**. Phase 3 executes the systematic audit to determine **which specific scientific datasets, products, versions, and API mechanisms fulfill those requirements for Bangladesh**.

---

## 2. Requirements Baseline Extraction

The following operational requirements from Phase 2 mandate empirical data backing:

| Requirement ID | Capability Supported | Required Environmental Information | Geographic Extent | Spatial Resolution Target | Temporal Horizon & Latency | Linked Data Specification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`FR-ENV-01`** | 7-Day Agro-Weather Forecast | $T_{\text{max}}$, $T_{\text{min}}$, Rain probability & mm, RH, Wind speed, Solar radiation. | National (495 Upazilas) | $\le 0.5^\circ$ ($\approx 50\text{km}$), Upazila-interpolated | 7-day forecast; updated every $\le 12\text{h}$ | `DR-MET-01` |
| **`FR-ENV-02`** | 7-Day Rainfall Anomaly | Rolling 7-day precipitation accumulation vs 10-year seasonal climatology. | National (495 Upazilas) | $\le 0.1^\circ$ ($\approx 10\text{km}$) | Rolling 7-day sum; historical 2014–present | `DR-PCP-01` |
| **`FR-ENV-03`** | Root-Zone Soil Moisture Deficit | Soil moisture anomaly / drying curve in top 0–100 cm root zone. | Barind Pilot (Rajshahi) + National | $\le 9\text{km}$ to $36\text{km}$ regional footprint | 2–3 day revisit; updated $\le 48\text{h}$ | `DR-SMC-01` |
| **`FR-ENV-04`** | Radar Surface Inundation Alert | Cloud-penetrating standing water extent & upstream transboundary rainfall. | Haor Pilot (Sylhet) + Meghalaya | $\le 10\text{m} - 20\text{m}$ (SAR); $\le 0.1^\circ$ (Rain) | 6–12 day SAR pass; rain updated $\le 6\text{h}$ | `DR-SAR-01`, `DR-PCP-01` |
| **`FR-ADV-01`** | Weather-Synced Irrigation Advisory | Penman-Monteith Reference $ET_0$, Crop $ET_c$, 72h forecast precipitation. | Barind Pilot (Rajshahi) | Upazila scale | 72-hour operational window | `DR-MET-01`, `DR-AGR-01` |
| **`FR-ADV-02`** | Haor Emergency Harvest Warning | Upstream catchment rainfall ($>100\text{mm}/48\text{h}$) + radar waterlogging. | Haor Pilot (Sunamganj) | Upazila & Catchment scale | 48-hour emergency lead time | `DR-SAR-01`, `DR-PCP-01` |
| **`FR-LOC-01`** | Upazila Administrative Hierarchy | Official administrative boundary polygons (495 Upazilas, 64 Districts). | National Bangladesh | Boundary level | Static verified geometries | `DR-AGR-01` |
| **`FR-LOC-02`** | Phenology & Crop Stage Binding | Stage-specific crop growth coefficients ($K_c$) for Boro, Aman, Aus, Potato. | Regional / AEZ specific | Crop variety level | Seasonal phenology calendar | `DR-AGR-01` |

---

## 3. Scope Boundaries & Investigation Rules

1. **Verification Before Endorsement**: No dataset will be included in the recommended initial stack based on marketing claims or generic global usage. Coverage over Bangladesh ($20.5^\circ\text{N} - 26.7^\circ\text{N}$, $88.0^\circ\text{E} - 92.7^\circ\text{E}$) and actual API responsiveness must be proven.
2. **Zero Large Ingestion in Phase 3**: Phase 3 performs small, bounded sample requests (e.g., 3-day point/bounding-box queries) to verify schema, units, coordinate bounds, and latency. Bulk downloading and database population belong strictly to Phase 8.
3. **Respect Scientific Resolution Realities**: The investigation must rigorously distinguish nominal pixel grid size from independent informational resolution. Coarse gridded products (SMAP, IMERG, POWER) must be evaluated as regional/upazila context, not sub-acre field boundary readings.
