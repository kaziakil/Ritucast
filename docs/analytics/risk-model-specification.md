# Agricultural Risk Model Specification — Ritucast

## 1. Executive Summary & Purpose

Agricultural risk modeling requires defining the exact physical outcome under consideration, the decision horizon, the target population, and the asymmetric asymmetric costs of classification errors.

In Ritucast, "risk" is **never** used as an ambiguous composite score. Instead, risk is explicitly partitioned into three domain-specific physical hazards:
1. **Root-Zone Moisture Deficit Risk** (High Barind Tract vegetative drought).
2. **Flash-Flood Inundation Hazard** (Haor Basin pre-monsoon crop submergence).
3. **Cardinal Biometeorological Thermal Risk** (Flowering heatwave or booting cold shock).

---

## 2. Risk Problem Definitions

| Specification Parameter | Risk Domain 1: Barind Moisture Deficit | Risk Domain 2: Haor Pre-Monsoon Flood | Risk Domain 3: Reproductive Thermal Stress |
| :--- | :--- | :--- | :--- |
| **Hazard Event** | Root-zone soil water depletion exceeds Readily Available Water ($D_t \ge RAW$), inducing stomatal closure. | Rapid overtopping or breaching of submersible embankments submerging standing Boro rice. | Morning canopy temperature $>35^\circ\text{C}$ during anthesis or nighttime $T_{\text{min}} < 15^\circ\text{C}$ during meiosis. |
| **Target Geography** | High Barind Tract: Godagari (`BD-50-20-30`), Tanore (`BD-50-20-90`). | Haor Basin: Sunamganj Sadar (`BD-60-90-86`), Tahirpur (`BD-60-90-89`). | High Barind Tract & Haor Basin. |
| **Active Crop & Variety** | Boro rice (*Oryza sativa L.*), primarily BRRI dhan28/29. | Boro rice (*Oryza sativa L.*), primarily BRRI dhan29/88/89. | Boro rice (*Oryza sativa L.*). |
| **Decision Horizon** | 48 to 72 hours forward projection. | 48 to 72 hours transboundary flood wave arrival. | 24 to 72 hours NWP weather forecast. |
| **Primary Physical Drivers** | FAO-56 Penman-Monteith $ET_c$, USDA-SCS effective rain, Barind heavy clay $TAW=56\text{mm}$. | GPM IMERG Meghalaya 48h rainfall ($P_{\text{cat}}$), BWDB Surma gauge water level ($H$) and rate of rise ($\Delta H/\Delta t$). | Open-Meteo multi-model ensemble forecast temperatures ($T_{\text{max}}, T_{\text{min}}$). |
| **Primary Decision Supported** | Withhold scheduled deep tubewell (DTW) pumping cycle before rain, or activate AWD replenishment. | Mobilize combine harvesters and communal labor to harvest fields with $\ge 80\%$ grain maturity. | Flood paddies with $3–7\text{cm}$ standing water layer to buffer canopy temperature extremes. |

---

## 3. Asymmetric Costs of Prediction Errors

In smallholder agriculture, Type I errors (false positives) and Type II errors (false negatives) carry vastly unequal agronomic and socio-economic consequences:

### 3.1 Barind Pre-Rain Irrigation Postponement (`RULE-IRR-01`)
- **False Positive (Model predicts rain; rain fails to arrive)**:
  - Farmer withheld scheduled DTW irrigation for 48 hours.
  - *Agronomic Impact*: High Barind heavy clay has high available water retention ($TAW=56\text{mm}$). During tillering, rice tolerates a 48-hour dry spell without yield loss. The farmer simply pumps on Day 3.
  - *Financial Impact*: Zero yield loss; minimal operational delay.
- **False Negative (Model predicts dry weather; farmer pumps; 30mm storm arrives)**:
  - Farmer applies $50\text{mm}$ DTW irrigation at full pumping cost, followed immediately by heavy rain.
  - *Agronomic Impact*: Paddy waterlogs, bunds overtop, broadcast urea fertilizer leaches into drainage channels.
  - *Financial Impact*: Wasted diesel/electricity pumping fee (~BDT 1,200–1,800/ha) plus wasted nitrogen fertilizer.
- **Policy Calibration**: The system tolerates modest false positives to maximize fuel savings, but enforces a strict rain probability threshold ($P_{\text{prob}} \ge 65\%$) and ensemble spread check ($\le 35\%$) to avoid farmer frustration.

### 3.2 Haor Early Harvest Warning (`RULE-FLD-01`)
- **False Positive (Model issues emergency harvest alert; flood waters peak safely below bunds)**:
  - Farmer harvests Boro rice at $80\%$ grain maturity (some green grains remain on panicle).
  - *Agronomic Impact*: Grain yield is $\sim 8\%$ below absolute biological maximum.
  - *Financial Impact*: Minor reduction in gross tonnage, but crop is 100% saved, dried, and secured.
- **False Negative (Model fails to alert; flash flood inundates haor within 48 hours)**:
  - Rice remains unharvested in low beels. Water rises $1.5\text{m}$ in 24 hours.
  - *Agronomic Impact*: $100\%$ catastrophic crop loss. Standing rice rots underwater, grains sprout on panicles, livestock fodder destroyed.
  - *Financial Impact*: Total seasonal financial ruin; severe regional food crisis.
- **Policy Calibration**: False negatives are catastrophic. The emergency harvest alert is calibrated to fire decisively whenever $I_{\text{flood}} \ge 0.75$, provided crop grain maturity has reached $\ge 80\%$.
