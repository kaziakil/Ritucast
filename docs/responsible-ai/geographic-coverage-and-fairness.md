# Geographic Coverage, Spatial Resolution, and Algorithmic Fairness — Ritucast

## 1. Executive Summary

Agricultural geography in Bangladesh exhibits extreme spatial heterogeneity: agro-ecological zones (AEZs) range from drought-prone undulating clay terraces in the northwest (Barind Tract) to deeply inundated seasonal flood basins in the northeast (Haor Basin).

This document evaluates the geographic coverage boundaries, spatial resolution limitations, and algorithmic fairness safeguards governing **Ritucast**.

---

## 2. Authorized Pilot Testbeds (`DEC-06`, `AGENTS.md`)

Ritucast is intentionally and strictly bounded to two representative pilot testbeds:

| Pilot Zone | Division & District | Upazilas Included | AEZ Code & Classification | Primary Agricultural Hazard | Calibrated Crop |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **High Barind Tract** | Rajshahi Division / Rajshahi District | **Godagari** (`BD-50-20-30`)<br>**Tanore** (`BD-50-20-90`) | AEZ 26: High Barind Tract | Severe groundwater depletion, low aquifer recharge, drought | Boro Rice (*Oryza sativa L.*), Potato |
| **Haor Basin** | Sylhet Division / Sunamganj District | **Sunamganj Sadar** (`BD-60-90-86`)<br>**Tahirpur** (`BD-60-90-89`) | AEZ 21: Sylhet Basin | Pre-monsoon transboundary flash floods, early crop submergence | Boro Rice (*Oryza sativa L.*) |

---

## 3. Spatial Resolution Disparity & Resolution Caveats

Satellite and numerical weather model grid cells operate at resolutions coarser than individual smallholder farm plots:

```
[ GFS / ECMWF Numerical Weather Grid Cell: ~9km - 11km ]
+-----------------------------------------------------------+
|  [ NASA POWER Agro-Climatology Grid: ~50km x 50km ]       |
|                                                           |
|    [ Upazila Administrative Boundary: ~15km x 25km ]      |
|    +-----------------------------------------------+      |
|    |                                               |      |
|    |      * Smallholder Farm Plot: 0.1 - 0.5 ha    |      |
|    |        (10m x 20m)                            |      |
|    |                                               |      |
|    +-----------------------------------------------+      |
+-----------------------------------------------------------+
```

### 3.1 Spatial Resolution Reality
- **Upstream Weather Grids**: $0.1^\circ \times 0.1^\circ$ ($\approx 10\text{km} \times 10\text{km}$) or $0.5^\circ \times 0.5^\circ$ ($\approx 50\text{km} \times 50\text{km}$).
- **Upazila Aggregate Size**: $250\text{--}470\text{ km}^2$.
- **Average Smallholder Plot Size**: $0.2\text{--}0.5\text{ hectares}$ ($2,000\text{--}5,000\text{ m}^2$).
- **Fairness Safeguard**: Ritucast does **not** claim to provide sub-parcel precision. The interface explicitly labels indicators as **Upazila-level regional averages** (*"উপজেলা গড় সূচক"*). This prevents smallholders on localized sandy levees from mistaking a regional clay-loam average for their specific plot.

---

## 4. Algorithmic Fairness & Resource Equity

### 4.1 Equitable Access Without Feature Disadvantage
- **Zero Paywalls**: All decision-support tiers (Tiers 1–4) are completely free and open. No "premium" advice tier exists.
- **Low-Bandwidth Mobile Compatibility**: The entire client interface is optimized to load on 2G/3G connections under $1.5\text{MB}$ payload budgets (`DEC-09`), preventing farmers with budget devices from being excluded.
- **Bangla-First Interface**: Plain-language Bengali typography with clear iconography ensures accessibility for farmers and local extension workers with limited English proficiency.

### 4.2 Prohibited Cross-AEZ Generalization
- A major algorithmic fairness risk is applying Barind drought rules to Haor farmers, or vice versa:
  - In Barind, soil water balance drives irrigation postponement.
  - In Haor, river stage rise ($WL \ge 8.25\text{m}$) and transboundary catchment rain drive emergency harvest directives, regardless of local soil deficit.
- **Enforcement**: [`AgriculturalDataRepository.evaluate_advisories`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L493) explicitly conditions agronomic rule evaluation on `aez_code` (AEZ 26 vs. AEZ 21), preventing algorithmic cross-contamination.

Related documentation:
- [`docs/responsible-ai/agricultural-recommendation-safeguards.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/agricultural-recommendation-safeguards.md)
- [`docs/responsible-ai/model-limitations-and-uncertainty.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/model-limitations-and-uncertainty.md)
- [`docs/responsible-ai/appropriate-use-and-misuse-prevention.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/appropriate-use-and-misuse-prevention.md)
