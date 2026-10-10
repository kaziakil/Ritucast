# Data Visualization & Indicator Display Guidelines

## 1. Scientific Integrity Standards

Visualizations in Ritucast must communicate physical conditions without exaggeration or misleading styling:
1. **Zero Fabricated Precision**: Never imply sub-millimeter precision when underlying sensors operate on coarse grids.
2. **Explicit Measurement Units**: Every axis, gauge, and metric card explicitly documents units (e.g., `মিমি`, `মিমি/দিন`, `°সে`, `মেগাজুল/বর্গমিটার`, `কিমি/ঘণ্টা`).
3. **No Truncated False Baselines**: Water balance gauges and rainfall bars start from true zero baselines.

---

## 2. Implemented Visualization Types

### 2.1 Soil Water Deficit Gauge ($D_t$ vs RAW/TAW)
- **Path**: `[WaterBalanceView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/WaterBalanceView.tsx)`
- **Design**:
  - Horizontal track representing Total Available Water ($\text{TAW} = 56.0\text{mm}$).
  - Permissible AWD range highlighted in light green ($\le \text{RAW} = 19.6\text{mm}$).
  - Current water deficit depicted as a dynamic progress bar.
  - Dashed red marker indicating Readily Available Water ($\text{RAW}$) threshold.

### 2.2 Haor Flash Flood Hazard Index ($I_{\text{flood}}$)
- **Path**: `[FloodHazardView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/FloodHazardView.tsx)`
- **Design**:
  - Segmented risk meter displaying normalized scale from 0.00 to 1.00.
  - Color boundaries:
    - Normal ($\le 0.45$): Green.
    - Advisory ($0.45 - 0.65$): Yellow / Lime.
    - Warning ($0.65 - 0.85$): Amber.
    - Emergency ($> 0.85$): Crimson.
  - Accompanied by four sub-index progress meters (Upstream Rainfall, Water Level Rise Rate, SAR Inundation Fraction, Soil Saturation).

### 2.3 72-Hour Quantitative Precipitation Forecast (QPF)
- **Path**: `[WeatherFeedView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/WeatherFeedView.tsx)`
- **Design**:
  - Daily rainfall volume rendered as proportional blue bars.
  - Rain probability percentage displayed prominently in badge tags.
  - Ensemble spread percentage rendered as a confidence band.

---

## 3. Exclusion of SHAP Visualizations

In accordance with Phase 9 and Phase 10 validation findings:
- Model explanations are strictly rule-based or derived from physical mass balances (FAO-56, USDA-SCS).
- Black-box ML models requiring SHAP explanation trees are **not implemented** in the active production engine.
- Fabricated or pseudo-SHAP visualization components are **strictly excluded**, ensuring zero algorithmic misrepresentation.
