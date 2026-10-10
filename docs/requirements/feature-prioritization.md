# Ritucast: Feature Prioritization Framework & Master Matrix

## 1. Prioritization Framework & Governance

To prevent feature accumulation and guarantee that engineering resources target validated user problems, Ritucast applies a disciplined 5-tier classification framework:

- **P0 — Foundational**: Non-negotiable architectural prerequisites, safety guardrails, localization, and core irrigation water-balance calculations.
- **P1 — Essential**: Core capabilities required to deliver the primary user journeys in the pilot zones (Haor flood alerts, offline PWA, card sharing).
- **P2 — Valuable**: Secondary agronomic enhancements and visual features scheduled after initial core journey stability (safe spray windows, choropleth maps).
- **P3 — Future**: Strategic horizon capabilities deferred to post-pilot expansion (multi-crop expansion, cooperative machinery tracking).
- **Research Gate**: Features with high potential value but unresolved scientific feasibility or data availability; strictly blocked from implementation until research criteria are satisfied.

---

## 2. Master Feature Prioritization Matrix

| Feature ID | Feature Name & Scope | Linked Requirements | Priority | User & Agronomic Value | Complexity & Rationale | Dependencies | Risks & Limitations | Success Metric |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| **FEAT-01** | **Upazila Administrative Selector** | `FR-LOC-01`, `FR-LOC-03` | **P0** | Enables precise administrative scoping for 495 Upazilas. | **Low**: Standard GeoJSON boundary lookup. | BBS / Survey of BD GeoJSON. | Ambiguous border villages; resolved by centroid mapping. | `MET-UX-01` |
| **FEAT-02** | **Phenological Crop Stage Configuration** | `FR-LOC-02` | **P0** | Matches weather to biological plant sensitivity (flowering, tillering). | **Low-Med**: Stage mapping tables from BRRI. | BRRI Crop Calendar tables. | Farmers uncertain of exact planting dates; resolved by stage categories. | `MET-SCI-03` |
| **FEAT-03** | **7-Day Agro-Weather Forecast Engine** | `FR-ENV-01`, `FR-ENV-05` | **P0** | Provides precipitation amount, probability, temp, RH, and wind. | **Med**: Ingestion, caching, and downscaling pipelines. | NASA POWER / NWP feeds. | Forecast skill decays beyond 72h; mitigated by confidence badges. | `MET-TECH-02` |
| **FEAT-04** | **Irrigation Scheduling Advisory Card** | `FR-ADV-01`, `FR-ADV-05` | **P0** | Primary value: Postpones tubewell pumping when rain fulfills $ET_c$. | **Med-High**: FAO-56 Penman-Monteith rules + SMAP soil balance. | `FEAT-02`, `FEAT-03`, SMAP feeds. | False positive rain forecast could delay needed irrigation; mitigated by bund check instructions. | `MET-AGR-01` |
| **FEAT-05** | **Interactive Explainability Drawer** | `FR-ADV-04`, `NFR-SCI-01` | **P0** | Builds farmer trust by showing observations vs forecasts vs water balance. | **Med**: Dynamic template synthesizer in Bangla. | `FEAT-04`. | Dense information overload; mitigated by progressive disclosure drawer. | `MET-UX-02` |
| **FEAT-06** | **Low-Bandwidth Mobile PWA Layout** | `FR-DSH-01`, `NFR-PERF-01` | **P0** | Enables responsive 720p mobile access on $<1.5\text{MB}$ payload. | **Med**: Mobile CSS design system + bundle optimization. | Modern PWA toolchain. | OS memory pressure on 2GB RAM phones; mitigated by lightweight DOM. | `MET-TECH-03` |
| **FEAT-07** | **Offline Service Worker Caching** | `FR-DSH-03`, `NFR-REL-01` | **P0** | Caches 72h upazila advisories for field visits without cell service. | **Med**: Service Worker Cache API + IndexedDB. | PWA container. | Stale data display; mitigated by hard 36h staleness ceiling (`NFR-REL-03`). | `MET-TECH-01` |
| **FEAT-08** | **Sentinel-1 SAR Haor Inundation Alert** | `FR-ENV-04`, `FR-ADV-02` | **P1** | Saves mature Boro rice from flash floods in Sunamganj pilot. | **High**: SAR backscatter thresholding + GPM upstream rain. | Sentinel-1 GRD pipeline, GPM IMERG. | 6–12 day satellite revisit gap; mitigated by GPM rainfall tracking. | `MET-SCI-02` |
| **FEAT-09** | **Cumulative Rainfall Anomaly Tracker** | `FR-ENV-02` | **P1** | Identifies unseasonal dry spells or extreme precipitation accumulation. | **Med**: Rolling 7-day accumulation vs 10-yr climatology. | GPM IMERG + NASA POWER history. | Sparse historical station records in some upazilas. | `MET-SCI-01` |
| **FEAT-10** | **One-Tap Advisory Card Share** | `FR-DSH-04` | **P1** | Enables SAAOs to blast advice across WhatsApp & IMO groups. | **Low-Med**: HTML-to-Canvas / Web Share API. | Browser Web Share. | Image rendering font issues; mitigated by pre-baked SVG/Canvas templates. | `MET-UX-03` |
| **FEAT-11** | **Safe Spray & Fertilizer Window** | `FR-ADV-03` | **P2** | Prevents pesticide drift and fertilizer leaching. | **Low-Med**: Multi-parameter hourly weather thresholding. | `FEAT-03`. | Overly strict weather rules might reduce spray opportunity windows. | `MET-AGR-01` |
| **FEAT-12** | **Upazila Spatial Risk Choropleth Map** | `FR-DSH-02` | **P2** | Provides regional situational awareness for SAAOs. | **Med-High**: Lightweight vector tile server + client renderer. | PostGIS / MapLibre / GeoJSON. | High GPU/memory usage on budget phones; mitigated by raster tile pre-rendering. | `MET-TECH-03` |
| **FEAT-13** | **Macro-Level Upazila Yield Prediction** | Future Vision | **P3** | Long-term planning for DAE and Food Directorate. | **Very High**: Calibrated crop simulation models (DSSAT/WOFOST). | 5+ years ground-truth BBS yield labels. | High error variance across smallholder parcels. | Phase 15/18 |
| **FEAT-14** | **National Automated SMS / IVR Push** | Future Vision | **P3** | Direct outreach to non-smartphone marginal smallholders. | **High (Ops/Cost)**: Telecom SMS gateways + Bangla TTS IVR. | Commercial telecom contracts. | High recurring per-message transit costs; subscription model needed. | Phase 16/18 |
| **FEAT-15** | **Field-Level Pest CV Diagnosis** | Excluded | **Research Gate** | Smartphone camera image diagnosis of leaf blast or planthoppers. | **High**: Supervised ML computer vision model. | Validated Bangladesh pest photo dataset (10,000+ images). | High risk of false positive chemical spraying recommendations. | Research Gate |
| **FEAT-16** | **Sub-Acre Field Parcel Delineation** | Excluded | **Research Gate** | Plot-by-plot satellite boundary monitoring. | **Very High**: High-res optical (Planet/WorldView) + cadastre data. | Commercial sub-meter imagery ($$$). | Prohibitive commercial imagery licensing costs; fragmented land tenure. | Research Gate |

---

## 3. Summary of Feature Tiers

- **P0 (Foundational Prerequisite)**: 7 Features (`FEAT-01` to `FEAT-07`) — Must be fully specified and built first.
- **P1 (Essential Pilot Capabilities)**: 3 Features (`FEAT-08` to `FEAT-10`) — Required for the complete Dual-Zone pilot user journey.
- **P2 (Valuable Enhancements)**: 2 Features (`FEAT-11`, `FEAT-12`) — Implemented during pilot refinement.
- **P3 (Deferred Horizons)**: 2 Features (`FEAT-13`, `FEAT-14`) — Scheduled for Horizons 2 and 3.
- **Research Gated**: 2 Features (`FEAT-15`, `FEAT-16`) — Strictly excluded from roadmap until scientific prerequisites are verified.
