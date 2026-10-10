# Environmental Indicators Specification — Ritucast

## 1. Executive Summary & Purpose

Environmental indicators represent **Tier 2 (Derived Agronomic Indicators)** under the Ritucast taxonomy (`DEC-08`). They transform multi-source physical observations into mathematically sound, dimensionless or agronomic units reflecting plant-soil-water and hydrological interactions.

All indicators implemented in Phase 9 adhere to the mathematical foundations specified in [indicator-interpretation-framework.md](file:///Users/kazi/Projects/RITUCAST/docs/science/indicator-interpretation-framework.md).

---

## 2. Master Indicator Specifications

### 2.1 Reference Evapotranspiration ($ET_0$, `EQN-ET0-01`)
- **Scientific Interpretation**: Daily atmospheric evaporative demand over an extensive, well-watered reference grass canopy ($h = 0.12\text{m}$, surface resistance $70\text{ s/m}$, albedo $\alpha = 0.23$).
- **Equation**:
  $$ET_0 = \frac{0.408 \Delta (R_n - G) + \gamma \frac{900}{T_{\text{mean}} + 273} u_2 (e_s - e_a)}{\Delta + \gamma (1 + 0.34 u_2)}$$
- **Units**: $\text{mm/day}$.
- **Inputs**: $T_{\text{max}}, T_{\text{min}}$ ($^\circ\text{C}$), $RH_{\text{mean}}$ ($\%$), $u_2$ ($\text{m/s}$), $R_s$ ($\text{MJ/m}^2/\text{day}$), elevation $z$ ($\text{m}$).
- **Spatial / Temporal Resolution**: Upazila centroid point query; daily time step.
- **Physical Bounds**: Validated within $0.5$ to $15.0\text{ mm/day}$.
- **Known Limitations**: NASA POWER solar radiation carries 24–48 hour latency. For real-time Day $T$, Open-Meteo current temperatures serve as an interim baseline.

### 2.2 Dynamic Crop Water Demand ($ET_c$)
- **Scientific Interpretation**: Daily water consumed by Boro rice under standard non-limiting soil moisture conditions at a specific phenological stage.
- **Equation**:
  $$ET_c = K_c(t) \times ET_0$$
- **Units**: $\text{mm/day}$.
- **$K_c$ Resolution**: Linearly interpolated across 5 developmental knots:
  - Day 1 (Transplanting): $K_c = 1.10$
  - Day 40 (Mid-Tillering): $K_c = 1.15$
  - Day 75 (Panicle Initiation): $K_c = 1.30$
  - Day 100 (Anthesis/Flowering): $K_c = 1.30$
  - Day 145 (Physiological Maturity): $K_c = 0.65$
- **Known Limitations**: Assumes standard 145-day semi-dwarf Boro varieties (BRRI dhan28/29). Short-duration varieties (115–125 days) require manual stage assignment via context gate.

### 2.3 Root-Zone Daily Soil Water Deficit ($D_t$, `EQN-SWD-01`)
- **Scientific Interpretation**: Net moisture depletion in the effective Boro rice root zone ($Z_r = 0.40\text{m}$) relative to field capacity.
- **Equation**:
  $$D_t = D_{t-1} + ET_{c, t} - P_{\text{eff}, t} - I_t + DP_t \quad (0 \le D_t \le TAW)$$
- **Units**: $\text{mm}$.
- **Soil Parameters (High Barind Heavy Clay Paleosols)**:
  - Total Available Water: $TAW = 1000 \times (\theta_{\text{FC}} - \theta_{\text{PWP}}) \times Z_r = 56.0\text{ mm}$ ($\theta_{\text{FC}}=0.32, \theta_{\text{PWP}}=0.18$).
  - Readily Available Water: $RAW = p \times TAW = 19.6\text{ mm}$ during tillering ($p=0.35$); $RAW = 5.6\text{ mm}$ during flowering ($p=0.10$).
- **Effective Precipitation ($P_{\text{eff}}$)**: Calibrated USDA Soil Conservation Service formulation. Rains $\le 3\text{mm}$ evaporate without infiltration; storms $>50\text{mm}$ run off bunded paddy spillways.
- **Critical Threshold**: $D_t \ge RAW$ triggers vegetative moisture deficit alert (`RULE-IRR-02`).

### 2.4 Haor Flash-Flood Hydrological Hazard Index ($I_{\text{flood}}$, `IDX-FLD-01`)
- **Scientific Interpretation**: Dimensionless composite hazard metric integrating upstream transboundary catchment cloudbursts with downstream river stage proximity to danger levels.
- **Equation**:
  $$I_{\text{flood}} = 0.35 \cdot f_P(P_{\text{cat}}) + 0.30 \cdot f_S(H, DL) + 0.20 \cdot f_R\left(\frac{\Delta H}{\Delta t}\right) + 0.15 \cdot f_I(f_{\text{inund}})$$
- **Units**: Dimensionless $[0.0, 1.0]$.
- **Sub-Functions**:
  - $f_P(P_{\text{cat}}) = \min(1.0, \max(0.0, P_{\text{cat}} - 30.0) / 120.0)$ (where $P_{\text{cat}}$ is 48h rainfall over southern Meghalaya hills).
  - $f_S(H, DL) = \min(1.0, \max(0.0, (H - (DL - 1.0)) / 1.20))$ (Surma gauge stage relative to $DL=8.25\text{m}$ PWD).
  - $f_R(\Delta H/\Delta t) = \min(1.0, \max(0.0, (\Delta H/\Delta t - 0.20) / 0.80))$ (24h rate of river stage rise in $\text{m/day}$).
  - $f_I(f_{\text{inund}}) = \min(1.0, f_{\text{inund}} / 0.40)$ (satellite observed inundation fraction).
- **Hazard Tiers**:
  - $< 0.35$: **Normal** (Standard monitoring).
  - $0.35 – 0.55$: **Advisory** (Inspect embankments, verify harvesters).
  - $0.55 – 0.75$: **Warning** (Flood water entering low beels within 48h).
  - $\ge 0.75$: **Emergency** (Triggers `RULE-FLD-01` emergency early harvest if grain maturity $\ge 80\%$).

### 2.5 Cardinal Thermal Stress Indices ($I_{\text{heat}}, I_{\text{cold}}$)
- **$I_{\text{heat}}$ (Anthesis Heat Sterility)**:
  - $I_{\text{heat}} = \min(1.0, \max(0.0, (T_{\text{max}} - 35.0) / 5.0))$.
  - Trigger: $I_{\text{heat}} > 0.0$ for $\ge 2$ consecutive days during anthesis/flowering (`RULE-TMP-02`).
  - Agronomic mitigation: $3–5\text{cm}$ standing water layer provides evaporative canopy cooling ($1.0–2.0^\circ\text{C}$).
- **$I_{\text{cold}}$ (Booting Cold Microspore Sterility)**:
  - $I_{\text{cold}} = \min(1.0, \max(0.0, (15.0 - T_{\text{min}}) / 5.0))$.
  - Trigger: $I_{\text{cold}} > 0.0$ for $\ge 3$ consecutive days during booting/panicle initiation (`RULE-TMP-01`).
  - Agronomic mitigation: $5–7\text{cm}$ nighttime standing water provides thermal blanket buffering ($1.5–2.5^\circ\text{C}$).
