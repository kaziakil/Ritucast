# Uncertainty and Missing Data Handling — Ritucast

## 1. Executive Summary & Purpose

Environmental observations and numerical weather predictions carry inherent scientific and observation uncertainties. In smallholder decision support, pretending to have absolute certainty is dangerous; dismissing uncertainty as zero risk is equally irresponsible.

This document formalizes the **Uncertainty and Missing Data Framework** implemented across Phase 9, governing how data gaps are flagged and how epistemic uncertainty is communicated to users.

---

## 2. Taxonomical Separation of Missing Information States

Ritucast explicitly distinguishes seven distinct missing data states:

| State Code | Descriptive Name | Physical Root Cause | System Handling & Suppression Action |
| :--- | :--- | :--- | :--- |
| `ERR-MISS-SRC` | Missing Source Ingestion | Satellite orbit delayed or API downtime. | Fail early in adapter; log missing manifest; use cached telemetry if $<36\text{h}$ old. |
| `ERR-MISS-OBS` | Sensor Missing Observation | Cloud obscuration in optical NDVI or missing gauge log. | Record as `NaN`; never replace with zero; decrement completeness percentage ($C$). |
| `ERR-SAN-RNG` | Physical Range Violation | Outlier value (e.g. $T_{\text{max}} = 65^\circ\text{C}$). | Flagged in semantic validation; triggers `AdvisorySuppressionEngine`. |
| `ERR-TEMP-COV` | Insufficient Temporal Span | Less than 3 days of weather data in window. | Climatology aggregator reports reduced confidence; suppresses cumulative anomaly calculations. |
| `ERR-SPAT-COV` | Outside Calibrated Zone | Upazila outside approved pilot testbeds. | `ContextGator` raises `ContextGatingError`; zero speculation allowed. |
| `ERR-UNC-SPRD` | Ambiguous Forecast Spread | Ensemble spread $>50\%$ with rain prob $40–60\%$. | Automated suppression (`DEC-10`); displays SAAO consultation fallback copy. |
| `ERR-STAGE-UNC` | Unverified Phenology | Farmer hasn't logged transplanting date. | Recommendation engine suppressed until phenological stage is confirmed. |

---

## 3. Epistemic Uncertainty Communication Standards

### 3.1 Strict Prohibition of Fabricated Probabilities
A common anti-pattern in agro-tech apps is generating pseudo-scientific confidence numbers (e.g., *"Confidence: 94.2%"* or *"80% certain of high yield"*). In Ritucast:
- **No Pseudo-Confidence Percentages**: Numerical probabilities are permitted **only** when they represent mathematically verified physical distributions (e.g., 48-hour Precipitation Probability $P_{\text{prob}}$ from a 50-member NWP ensemble).
- **Heuristic Scores Never Become Probabilities**: A multi-factor flood score ($I_{\text{flood}} = 0.78$) is communicated as an indexed hazard tier ("উচ্চ বন্যা ঝুঁকি" - High Flood Risk), never as "78% probability of flooding."

### 3.2 Linguistic Framing of Forecast Spread
Whenever multi-model ensemble spread is between $25\%$ and $50\%$, advisory cards must display the explicit disclaimer:
> *"আবহাওয়া মডেলের পূর্বাভাসের বিস্তার [X] %। পূর্বাভাসে স্বাভাবিক অনিশ্চয়তা বিদ্যমান থাকায় সরাসরি মাঠ পর্যবেক্ষণ বাঞ্ছনীয়।"*
