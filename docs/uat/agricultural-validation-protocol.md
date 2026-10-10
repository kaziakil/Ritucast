# Agricultural & Physical Validation Protocol — Ritucast

## 1. Overview & Scientific Context

This protocol defines the formal **Agricultural & Ground-Truth Validation Methodology** for **Ritucast**. It outlines how model estimates, numerical weather predictions, and derived physical indices will be quantitatively compared against observational ground truth and established agronomic baselines during **Phase 17: Scientific & Agricultural Validation**.

Ritucast integrates empirical observations (Tier 1), physical equations (Tier 2), and probabilistic forecasts (Tier 3) to produce actionable farming advice (Tier 4) per `DEC-08`. Rigorous ground-truthing ensures that these recommendations remain safe, agronomically sound, and explainable.

---

## 2. Validation Framework & Ground-Truth Sensors

### 2.1 High Barind Tract (Rajshahi: Godagari, Tanore)

| Indicator / Metric | Model / Equation Source | Ground-Truth Baseline | Instrumentation & Protocol | Target Accuracy |
| :--- | :--- | :--- | :--- | :--- |
| **Reference Evapotranspiration ($ET_0$)** | FAO-56 Penman-Monteith (`EQN-ET0-01`) using NASA POWER | BMD Rajshahi Weather Station (`Station ID: 41923`) | Class-A Evaporation Pan + Campbell Scientific AWS ($R_s, T, RH, u_2$) | $\text{RMSE} \le 0.65\text{ mm/day}$; $R^2 \ge 0.85$ |
| **Crop Evapotranspiration ($ET_c$)** | $ET_c = K_c \times ET_0$ with BRRI/FAO-56 calibrated $K_c$ | BRRI Rajshahi Lysimeter Data | Lysimetric water balance measurements for Boro rice | Relative error $\le 12\%$ |
| **Soil Water Deficit ($D_t$)** | Dual/Single $K_c$ daily soil water balance (`EQN-SWD-01`) | Perforated Pani Pipe (AWD Field Tube) | Weekly manual water table depth readings below soil surface in 15 test plots | AWD trigger concordance $\ge 90\%$ |
| **Precipitation (24h/48h)** | ECMWF IFS / GFS ensemble blended QPF | BMD Rajshahi Daily Rain Gauge | Manual standard rain gauge (SRG) + tipping bucket AWS | Threat Score $\ge 0.60$ for rain $>5\text{ mm}$ |

### 2.2 Haor Basin (Sylhet: Sunamganj Sadar, Tahirpur)

| Indicator / Metric | Model / Equation Source | Ground-Truth Baseline | Instrumentation & Protocol | Target Accuracy |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Catchment Rain ($P_{48h}$)** | GPM IMERG Early Run + ECMWF IFS QPF over Meghalaya Hills | IMD Cherrapunji & Shillong Gauges (Cross-border feeds) | Daily recorded millimeter totals across transboundary catchment | Detection of heavy surge events ($>100\text{mm}$) POD $\ge 85\%$ |
| **River Water Level ($H_t$)** | BWDB Telemetered River Stage | BWDB Sunamganj Gauging Station (`SW-267`, Surma River) | Twice-daily manual staff gauge readings + automated radar gauge | Stage error $\le 0.15\text{ m}$ |
| **Inundation Extent ($I_t$)** | Sentinel-1 SAR C-band backscatter ($<-16\text{ dB}$) | FFWC Daily Inundation Bulletins + SAAO Field Logs | Ground GPS photography of flooded beels and haor perimeters | Spatial agreement $\ge 85\%$ |
| **Flash Flood Index ($I_{\text{flood}}$)** | Composite formula (`IDX-FLD-01`) | Observed Flash Flood Occurrence | Post-event emergency verification by Sunamganj DAE office | POD $\ge 85\%$, FAR $\le 20\%$ |

---

## 3. Quantitative Evaluation Metrics

Model outputs will be evaluated using standard physical and statistical validation metrics:

### 3.1 Continuous Variable Metrics ($ET_0, D_t, P$)
1. **Root Mean Square Error (RMSE)**:
   $$\text{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^N (M_i - O_i)^2}$$
2. **Mean Bias Error (MBE)**:
   $$\text{MBE} = \frac{1}{N}\sum_{i=1}^N (M_i - O_i)$$
3. **Nash-Sutcliffe Efficiency (NSE)**:
   $$\text{NSE} = 1 - \frac{\sum (O_i - M_i)^2}{\sum (O_i - \bar{O})^2}$$

### 3.2 Categorical Hazard & Advisory Metrics (Contingency Matrix)

| Model Prediction \ Observed Event | Event Occurred (Observed) | Event Did Not Occur | Total |
| :--- | :--- | :--- | :--- |
| **Advisory / Warning Issued** | Hits ($H$) | False Alarms ($F$) | $H + F$ |
| **No Advisory / Normal Issued** | Misses ($M$) | Correct Rejections ($C$) | $M + C$ |
| **Total** | $H + M$ | $F + C$ | $N$ |

- **Probability of Detection (POD)**: $\text{POD} = \frac{H}{H + M} \ge 0.85$
- **False Alarm Ratio (FAR)**: $\text{FAR} = \frac{F}{H + F} \le 0.20$
- **Critical Success Index (CSI / Threat Score)**: $\text{CSI} = \frac{H}{H + M + F} \ge 0.65$

---

## 4. Phenological Ground-Truthing Protocol

Under `DEC-17`, advisory generation requires active growth stage verification. SAAOs will log weekly phenological stages for Boro rice test parcels according to the standard BBCH/IRRI scale:

1. **Vegetative Phase**:
   - Transplanting / Seedling establishment (Day 0–15)
   - Tillering (কুশি পর্যায়, Day 16–40)
2. **Reproductive Phase**:
   - Panicle Initiation / Booting (থোর পর্যায়, Day 41–65)
   - Flowering / Heading (ফুল পর্যায়, Day 66–80)
3. **Ripening Phase**:
   - Milk / Dough stage (দুধ/নরম পর্যায়, Day 81–105)
   - Maturity / Ripening (পাকা পর্যায়, Day 106–125)

Any divergence between calendar-projected phenology and actual field observation will trigger a manual stage override in the Ritucast Context Selector to ensure AWD stress or early harvest advice matches true crop physiology.

---

## 5. Phase 17 Execution Readiness

This validation protocol establishes the rigorous scientific bridge from Phase 16 (UAT & Usability Validation) to Phase 17 (Scientific & Agricultural Validation). All mathematical formulas, error budgets, and contingency tables defined here will govern the formal benchmark reports executed in Phase 17.
