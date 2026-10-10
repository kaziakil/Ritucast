# Ritucast: Scientific Research Gaps & Uncertainty Register

## 1. Executive Summary & Purpose

A scientifically honest platform must explicitly document what is known, what is provisional, and what remains an open research question. Concealing scientific uncertainties or treating provisional assumptions as proven facts creates severe vulnerabilities during field deployment.

This document establishes the **Research Gaps Register**, tracking:
- Critical open scientific questions.
- Required empirical evidence and validation datasets.
- Assigned future roadmap phases responsible for resolving each gap.
- Risk level and fallback operational strategies if the gap remains unresolved.

---

## 2. Master Research Gaps Inventory

| Gap ID | Research Question | Scientific Context | Required Evidence & Data Sources | Impact if Unresolved | Assigned Phase | Fallback Operational Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`GAP-01`** | **Transboundary Catchment Runoff Lag Calibration**: What is the exact empirical time lag (hours) between peak rainfall in the Meghalaya Hills and flood stage cresting at Sunamganj? | Pre-monsoon convective cloudbursts over Cherrapunji flow into Sunamganj via the Surma, Kushiyara, and Jadukata rivers. Current literature estimates lag between 12 and 36 hours depending on antecedent soil wetness. | Paired historical time-series of half-hourly GPM IMERG V07 grids over Meghalaya and hourly BWDB gauge logs at Sunamganj (`#268`) and Lorergarh (`#128`) across 2017–2024. | Early harvest alerts could trigger either too early (wasting harvest labor) or too late (submerged crop). | **Phase 9 (Analytics) & Phase 15** | Use conservative 24h lag window; trigger preliminary advisory at $P_{\text{cat}} \ge 70\text{mm}$. |
| **`GAP-02`** | **SMAP 9km Radiometer Disaggregation for Bunded Paddies**: How can 9km passive microwave soil moisture be disaggregated from standing water in flooded paddies to isolate upland soil drying? | In mixed landscape pixels, standing water in paddies saturates the L-band radiometer ($0.45–0.50\text{ m}^3/\text{m}^3$), masking acute drought in adjacent un-irrigated upland fields (`RSK-13`, `ASM-04`). | High-resolution Sentinel-1 SAR surface watermasks ($10\text{m}$) used to mask out flooded areas from the 9km radiometer footprint, validated against BMDA ground sensors in Godagari. | Inability to detect upland drought stress in mixed cropping zones. | **Phase 9 (Recommendation Engine)** | Rely strictly on mass-balance soil water deficit model ($D_t$) for field-level advice; use SMAP strictly for regional context. |
| **`GAP-03`** | **NASA POWER Grid Cell Downscaling to Barind Micro-Topography**: How does the $0.5^\circ$ (~55km) MERRA-2 reanalysis grid represent micro-topographic temperature extremes across Barind valleys? | High Barind topography undulates between $15\text{m}$ and $40\text{m}$ elevation. Cold air pools in valley bottoms at night, while ridge tops experience higher daytime wind and evaporative demand. | High-density deployment of low-cost temperature loggers or historical BMDA AWS transects across Godagari and Tanore. | Minor underestimation of nighttime cold shock or daytime heat stress ($1.0–1.5^\circ\text{C}$ bias). | **Phase 8 (ETL) & Phase 9** | Apply standard environmental lapse rate adjustments based on SRTM 30m digital elevation models. |
| **`GAP-04`** | **Inter-Annual Phenological Shift Detection under Cloud Cover**: How can inter-annual variance in Boro sowing dates ($\pm 10–14\text{ days}$) be detected when optical satellites are blinded by clouds? | Severe winter cold or delayed seedbed preparation can shift transplanting dates by up to 2 weeks. Static calendar lookup risks misidentifying the active growth stage. | SAAO mobile crowdsourcing: Frontline extension officers confirm block transplanting dates directly in the Ritucast PWA during weekly visits (`FR-LOC-03`). | System might misidentify flowering stage, triggering thermal warnings at the wrong time. | **Phase 6 (IA) & Phase 11 (Frontend)** | Implement user-confirmed phenological stage override in the PWA UI. |
| **`GAP-05`** | **In-Situ Lysimeter & Class-A Pan Evaporation Data Acquisition**: Can digitized historical daily lysimeter and pan evaporation records be formally acquired from BRRI and BMDA? | FAO-56 Penman-Monteith $ET_0$ calculations should ideally be validated against measured pan evaporation and drainage lysimeters in Bangladesh. | Formal institutional data-sharing MoU or bilateral research exchange with BRRI Water Management Division and BMDA. | Slight uncertainty in empirical $K_c$ coefficients for newer Boro varieties (BRRI dhan89/92). | **Phase 15 (Validation)** | Rely on published peer-reviewed BRRI lysimeter literature (e.g., Sattar et al., 2009; Rashid et al., 2016). |

---

## 3. Governance and Gap Retirement Protocol

1. A research gap may only be formally marked **Closed / Resolved** when empirical validation results are documented in the corresponding phase validation report (e.g., Phase 9 or Phase 15).
2. If a research gap cannot be resolved due to data unavailability, the affected feature must be classified as **Research-Gated**, restricted to advisory context, or formally deferred by the Project Lead.
