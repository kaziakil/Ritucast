# Descriptive Agricultural Analytics Specification — Ritucast

## 1. Executive Summary & Purpose

Descriptive agricultural analytics transform raw daily meteorological time series into transparent, statistical summaries representing the physical growing environment.

In strict adherence to the Four-Tier Information Taxonomy (`DEC-08`), descriptive statistics represent **Tier 1 (Empirical Observations)** and baseline aggregations. They never make speculative predictive claims or assert causal agricultural damage without verified agronomic models.

---

## 2. Implemented Descriptive Aggregations

Descriptive metrics are implemented in [climatology.py](file:///Users/kazi/Projects/RITUCAST/analytics/descriptive/climatology.py) via `ClimatologyAggregator.summarize_period()`:

| Metric Identifier | Metric Name | Mathematical Definition | Input Variable & Unit | Spatial & Temporal Resolution | Agronomic Interpretation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `MET-TMEAN-01` | Mean Daily Temperature | $\bar{T} = \frac{1}{N} \sum_{i=1}^N T_{2\text{m}, i}$ | $T_{2\text{m}}$ ($^\circ\text{C}$) | Upazila centroid; user-defined window (7d, 30d, season). | General thermal accumulation driving phenological development rate. |
| `MET-TMAX-01` | Maximum Temperature Observed | $T_{\text{max}} = \max_{i} (T_{\text{max}, i})$ | $T_{\text{max}}$ ($^\circ\text{C}$) | Upazila centroid; user-defined window. | Extreme heat exposure; evaluated against $35^\circ\text{C}$ anthesis threshold. |
| `MET-TMIN-01` | Minimum Temperature Observed | $T_{\text{min}} = \min_{i} (T_{\text{min}, i})$ | $T_{\text{min}}$ ($^\circ\text{C}$) | Upazila centroid; user-defined window. | Extreme cold exposure; evaluated against $15^\circ\text{C}$ booting threshold. |
| `MET-PCP-01` | Cumulative Precipitation | $P_{\text{cum}} = \sum_{i=1}^N P_i$ | Precipitation ($\text{mm}$) | Upazila centroid; rolling retrospective window. | Total rainfall volume available for infiltration and runoff. |
| `MET-SRAD-01` | Mean Daily Solar Radiation | $\bar{R}_s = \frac{1}{N} \sum_{i=1}^N R_{s, i}$ | Solar Radiation ($\text{MJ/m}^2/\text{day}$) | Upazila centroid; user-defined window. | Photosynthetically active radiation driving biomass and $ET_0$. |
| `MET-RH-01` | Mean Relative Humidity | $\bar{RH} = \frac{1}{N} \sum_{i=1}^N RH_i$ | Relative Humidity ($\%$) | Upazila centroid; user-defined window. | Canopy boundary layer vapor pressure deficit and disease favorability proxy. |
| `MET-COMP-01` | Temporal Completeness | $C = \frac{N_{\text{observed}}}{N_{\text{span}}} \times 100\%$ | Calendar days ($\%$) | Upazila centroid; user-defined window. | Data quality indicator; flags missing observation days. |

---

## 3. Epistemic Safeguards & Anti-Overconfidence Rules

1. **No False Drought Claims (`DEC-06`)**:
   - The absence of rainfall ($P_{\text{cum}} = 0\text{mm}$ over 20 days) must **never** be labeled as an "agricultural drought" or "crop failure" in the High Barind Tract.
   - High Barind Boro rice is $100\%$ irrigated via deep tubewells (DTWs). Zero winter rain is the normal climatological state. Water stress can only be diagnosed via the root-zone soil water deficit ($D_t$), integrating irrigation cycles.
2. **Missing Observation Treatment**:
   - Missing meteorological records are never converted to zero values. Zero rainfall is an empirical observation; missing data is represented as `NaN` and penalizes the temporal completeness score ($C$).
3. **No Uncalibrated Anomaly Assertions**:
   - An observation cannot be classified as an "anomaly" without referencing a verified 30-year climatological normal baseline (e.g., BMD 1991–2020 normal). Phase 9 reports absolute physical values and rolling differences rather than unanchored percentage anomalies.
