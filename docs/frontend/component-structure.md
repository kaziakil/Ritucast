# Frontend Component Structure & Specifications

## 1. Component Architecture Overview

All UI presentation components are modular, pure React functional components utilizing typed props declared in `[api.ts](file:///Users/kazi/Projects/RITUCAST/frontend/src/types/api.ts)`. Presentation is strictly decoupled from network fetch operations, which reside in `[apiClient.ts](file:///Users/kazi/Projects/RITUCAST/frontend/src/services/apiClient.ts)`.

---

## 2. Component Inventory

### 2.1 `App.tsx` (Root Orchestrator)
- **Path**: `[App.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/App.tsx)`
- **Responsibilities**:
  - Initializes metadata (Upazila list, crop profiles, system readiness) via `Promise.allSettled`.
  - Manages active tab state (`advisories`, `weather`, `water-balance`, `flood`, `provenance`).
  - Coordinates global selection state (`selectedUpazilaId`, `selectedCropId`, `selectedStage`).
  - Orchestrates analytical data queries whenever context changes or manual refresh is triggered.
  - Handles global network errors and provides visual fallbacks.

### 2.2 `Header.tsx` (Top Navigation & Health Monitor)
- **Path**: `[Header.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/Header.tsx)`
- **Responsibilities**:
  - Renders official branding: `ঋতুকাস্ট Ritucast` with the brand Sprout icon.
  - Displays dynamic System Readiness Pill:
    - `যাচাই হচ্ছে...` (Verifying) during initial metadata probe.
    - `সচল (লাইভ)` (Active Green) when backend dependencies report `ready: true`.
    - `সীমাবদ্ধ` (Limited Amber) when dependencies or satellite caches are missing.
  - Provides accessible tab navigation buttons with `aria-current="page"`.

### 2.3 `ContextSelector.tsx` (Contextual Gating Bar)
- **Path**: `[ContextSelector.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/ContextSelector.tsx)`
- **Responsibilities**:
  - Renders accessible `<select>` controls for Upazila, Crop, and Phenological Growth Stage.
  - Dynamically updates available growth stages when a crop changes.
  - Displays contextual badges: AEZ code and name, primary regional risk (Groundwater Deficit vs Flash Flood).
  - Displays Contextual Gating compliance indicator (`DEC-17`).

### 2.4 `AdvisoryHubView.tsx` (Operational Decision View)
- **Path**: `[AdvisoryHubView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/AdvisoryHubView.tsx)`
- **Responsibilities**:
  - Renders automated suppression banner (`DEC-10`) when meteorological spread exceeds thresholds.
  - Displays Primary Action Recommendation Card (Tier 4) with action checklist and economic savings breakdown.
  - Displays mandatory field verification notice (`AGENTS.md` / `DEC-10`).
  - Renders 3-Tier supporting foundation grid:
    - Tier 1: NASA / BMD sensor summary.
    - Tier 2: FAO-56 $ET_0$ and soil moisture deficit $D_t$.
    - Tier 3: Numerical weather prediction (NWP) 72-hour rain probability and QPF.
  - Renders physical hazard evaluations (Drought, Heat Stress, Cold Stress, Flood) adhering to `DEC-06`.

### 2.5 `WeatherFeedView.tsx` (Atmospheric Conditions)
- **Path**: `[WeatherFeedView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/WeatherFeedView.tsx)`
- **Responsibilities**:
  - Renders yesterday's ground truth weather observation (Max/Min Temp, Rainfall, Solar Radiation, Humidity).
  - Renders 72-hour forecast cards with daily precipitation probability, QPF rainfall bars, and temperature ranges.
  - Highlights ensemble spread percentage with risk color coding.

### 2.6 `WaterBalanceView.tsx` (Soil Moisture & AWD)
- **Path**: `[WaterBalanceView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/WaterBalanceView.tsx)`
- **Responsibilities**:
  - Renders Alternate Wetting and Drying (AWD) status banner (Drying Permissible vs Irrigation Required).
  - Displays root-zone water deficit gauge ($D_t$) against Readily Available Water (RAW = 19.6mm) and Total Available Water (TAW = 56.0mm).
  - Displays FAO-56 Penman-Monteith reference evapotranspiration ($ET_0$) and crop demand ($ET_c$).

### 2.7 `FloodHazardView.tsx` (Transboundary Haor Flood)
- **Path**: `[FloodHazardView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/FloodHazardView.tsx)`
- **Responsibilities**:
  - Renders early harvest alert banner (`RULE-FLD-01`) when flood hazard index breaches threshold and crop is ripe.
  - Renders Haor Flash Flood Hazard Index gauge ($I_{\text{flood}}$) with color-coded severity tiers.
  - Renders non-applicability warning for High Barind Tract upazilas.

### 2.8 `ProvenanceView.tsx` (Transparency & Governance)
- **Path**: `[ProvenanceView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/ProvenanceView.tsx)`
- **Responsibilities**:
  - Displays table of ingested datasets with latency hours, coverage, and license.
  - Catalogs physical equations implemented (`EQN-ET0-01`, `EQN-SWD-01`, `IDX-FLD-01`).
  - Re-articulates strict platform boundaries (`DEC-06` Non-Goals).

### 2.9 `Footer.tsx` (Institutional Accountability)
- **Path**: `[Footer.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/Footer.tsx)`
- **Responsibilities**:
  - Acknowledges research and extension partners (DAE, BRRI, BMD, BWDB).
  - Enforces platform-wide anti-overconfidence disclaimer.
  - Displays build version and timestamp.
