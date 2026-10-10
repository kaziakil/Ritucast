# Method Selection and Rationale — Ritucast

## 1. Executive Summary & Purpose

A critical principle of agricultural intelligence is selecting analytical methods proportionate to the available empirical evidence. In peasant agriculture, recommending a farmer withhold irrigation or harvest prematurely carries severe financial and food security consequences.

This document establishes the scientific rationale for choosing **deterministic physical equations and domain-informed decision rules** over uncalibrated supervised machine learning for the Ritucast Minimum Complete Product (MCP).

---

## 2. Comparative Method Evaluation

| Analytical Paradigm | Strengths | Severe Deficiencies in Bangladesh Smallholder Context | Decision for Ritucast |
| :--- | :--- | :--- | :--- |
| **Direct Aggregation & Summary** | High transparency; zero overfitting risk; mathematically trivial. | Purely descriptive; cannot evaluate dynamic plant-soil water deficits. | **Approved for Tier 1** (Agroclimatology ledgers). |
| **Deterministic Physical Modeling** (FAO-56, USDA-SCS, Penman-Monteith) | Grounded in thermodynamics and mass balance; verified global standards; strictly bounded outputs; zero training data required. | Requires physical soil parameters ($FC, PWP, Z_r$); point estimates represent regional averages rather than micro-topography. | **Approved for Tier 2** ($ET_0, ET_c, D_t, I_{\text{flood}}$). |
| **Evidence-Supported Rule Catalogs** (BRRI/DAE Thresholds) | Agronomically actionable; fully explainable in plain rural Bengali; auditable by extension agents; predictable failure modes. | Requires expert calibration against local crop varieties and Agro-Ecological Zones (AEZs). | **Approved for Tier 3 & 4** (`RULE-IRR-01`, `RULE-FLD-01`, etc.). |
| **Supervised Machine Learning** (XGBoost, Random Forests, Neural Networks) | Can discover non-linear empirical patterns when massive high-dimensional labeled datasets exist. | **Fatal Flaw (`DEC-06`)**: Ground-truth parcel-level crop yields and continuous soil moisture probes do not exist in Bangladesh. Training models on coarse remote sensing produces spurious correlations and catastrophic hallucinations under climate extremes. | **Strictly Disqualified & Banned** from operational decision support. |

---

## 3. The Fallacy of Premature Machine Learning in Smallholder Advisory

Many agricultural technology projects claim to deploy "AI crop prediction" by fitting gradient boosted trees to satellite NDVI and ERA5 weather grids to predict historical district-averaged yields. In Ritucast, this approach is formally rejected due to three critical scientific flaws:

1. **Severe Aggregation & Spatial Fallacy**:
   - Bangladesh Bureau of Statistics (BBS) records rice yields as annual Upazila-wide aggregates spanning thousands of independent smallholder plots. Fitting an ML model on Upazila averages creates an ecological fallacy: the model predicts macro-administrative reporting biases rather than field-level agronomic responses.
2. **Spurious Causal Attribution**:
   - A satellite NDVI decline can result from cloud shadows, seasonal field clearing, crop rotation, or normal post-maturity senescence. An ML model without physiological grounding easily misclassifies harvest as a devastating disease outbreak (`MOD-DIS-01`).
3. **Black-Box Opacity vs. Extension Worker Trust**:
   - SAAOs and lead farmers reject advice when an application cannot explain *why* an action is recommended. A farmer told to harvest early because "Tree Model Feature 14 = 0.82" will ignore the alert. A farmer told to harvest early because "the Surma river has risen 65 cm in 24 hours and 125 mm of rain fell in the Meghalaya hills" understands the physical reality and acts.

---

## 4. Conclusion & Selected Architecture

Ritucast deliberately selects:
1. **FAO-56 Penman-Monteith Combination Equation** for reference evaporative demand.
2. **USDA Soil Conservation Service Curve Method** for root-zone rainfall infiltration.
3. **Mass-Balance Depletion Model** for daily soil water deficit ($D_t$).
4. **Hydrological Gauge & Orographic Rain Synthesis** for Haor flash flood risk ($I_{\text{flood}}$).
5. **Calibrated Phenological Gating & Threshold Rules** for Bengali advisory card generation.
