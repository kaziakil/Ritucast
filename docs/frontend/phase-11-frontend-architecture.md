# Phase 11: Frontend Application Architecture

## 1. Executive Summary

This document specifies the software architecture, design principles, and runtime characteristics of the **Ritucast Frontend Application**, implemented in Phase 11. Ritucast is an evidence-based agricultural decision-support web application providing localized, actionable, and explainable farming intelligence for smallholders, farmer groups, and extension workers (SAAO) across Bangladesh.

The frontend is implemented as a modern, high-performance Single Page Application (SPA) / Progressive Web App (PWA) using **React 19**, **TypeScript 6**, **Vite 8**, and a custom **Vanilla CSS Design System** (`[index.css](file:///Users/kazi/Projects/RITUCAST/frontend/src/index.css)`).

---

## 2. Architecture Principles & Constraints

### 2.1 Four-Tier Information Taxonomy (`DEC-08`)
System outputs are strictly segregated visually and structurally into four distinct agronomic tiers:
1. **Tier 1: Empirical Observations (প্রত্যক্ষ পর্যবেক্ষণ)**: Direct readings from validated sources (NASA POWER solar radiation, BMD radar/rain-gauge precipitation, Sentinel-1 SAR backscatter).
2. **Tier 2: Derived Agronomic Indicators (হিসাবকৃত সূচক)**: Physical calculations (FAO-56 Penman-Monteith $ET_0$, crop water demand $ET_c$, daily root-zone soil water deficit $D_t$, Haor flash-flood hazard index $I_{\text{flood}}$).
3. **Tier 3: Probabilistic Predictions (পূর্বাভাস)**: Multi-model numerical weather forecasts (ECMWF IFS / NOAA GFS) presenting calibrated 72-hour precipitation probability, Quantitative Precipitation Forecast (QPF), and ensemble spread percentage.
4. **Tier 4: Actionable Recommendations (পরামর্শ)**: Operational directives (e.g., postpone irrigation, prepare emergency harvest) with plain-language explanations, economic/fuel savings, and mandatory field inspection copy.

### 2.2 Client Hardware & Payload Budgets (`DEC-09`)
To ensure usability across rural Bangladesh on budget Android devices (2GB–3GB RAM) operating over variable 3G/2G mobile data:
- **Total Bundle Budget**: $\le 1.5\text{MB}$ uncompressed. Actual production build: **292.5 kB JS (85.5 kB gzip)** and **13.5 kB CSS (3.1 kB gzip)**. Total wire payload: **88.6 kB gzip**.
- **Time-to-Interactive (TTI)**: $\le 3.5\text{s}$ simulated on 3G network conditions.
- **Peak Client Heap Memory**: $\le 45\text{MB}$.
- **Zero Direct Upstream Querying**: The browser communicates solely with the Ritucast FastAPI backend (`http://localhost:8000` or configured `VITE_API_BASE_URL`), never directly with upstream satellite or weather services.

### 2.3 Mandatory Contextual Gating (`DEC-17`)
Advisories and water-balance queries cannot be requested without explicit verification of:
1. Supported Administrative Upazila (e.g., Godagari, Tanore, Tahirpur, Sunamganj Sadar).
2. Calibrated Crop (Boro rice - *Oryza sativa L.*).
3. Active Phenological Growth Stage (Tillering, Booting, Flowering, Dough, Maturity).

### 2.4 Automated Suppression Enforcement (`DEC-10`)
When meteorological ensemble spread exceeds 50% or telemetry is $>36\text{ hours}$ old, the backend flags `is_suppressed: true`. The frontend immediately suppresses operational recommendations and renders a prominent amber fallback alert directing farmers to consult their local Sub-Assistant Agriculture Officer (SAAO).

---

## 3. Technology Stack & Decision Rationale

| Layer | Selected Technology | ADR / DEC | Rationale |
| :--- | :--- | :--- | :--- |
| **Framework** | React 19 + TypeScript | `ADR-03` | Component reusability, strict compile-time type safety matching OpenAPI schemas. |
| **Build Tool** | Vite 8 + Rollup | `ADR-03` | Sub-second HMR, tree-shaking, lightweight bundle generation ($<300\text{kB}$). |
| **Styling** | Vanilla CSS (Custom Properties) | `ADR-03`, `DEC-20` | Zero-runtime CSS, total control over outdoor high-contrast palette, zero Tailwind dependencies. |
| **Typography** | Google Fonts (Hind Siliguri, Inter) | `DEC-08` | Native Bangla script rendering with Latin numeral pairing for agronomic measurements. |
| **Icons** | Lucide React | `DEC-20` | Tree-shakable SVG icons with high legibility on outdoor mobile screens. |
| **Testing** | Vitest 5 + React Testing Library | `ADR-03` | Fast in-memory unit and integration testing without headless browser overhead. |

---

## 4. Component Hierarchy & Data Flow

```
[App.tsx] (Root State & Context Provider)
   ├── [Header.tsx] (Branding, Navigation Tabs, System Readiness Pill)
   ├── [ContextSelector.tsx] (Upazila, Crop, Stage Selectors, Refresh Action - DEC-17)
   └── Main Content Container
        ├── [AdvisoryHubView.tsx] (Active Tab: Advisories - DEC-08, DEC-10, DEC-06)
        │    ├── Suppression Alert (DEC-10)
        │    ├── Tier 4 Primary Recommendation Card
        │    │    └── Field Verification Disclaimer
        │    ├── 3-Tier Supporting Foundation Cards (Tier 1, Tier 2, Tier 3)
        │    └── Physical Hazard Assessment Grid
        ├── [WeatherFeedView.tsx] (Tab: Weather)
        │    ├── Tier 1 Empirical Observation (NASA / BMD)
        │    └── Tier 3 72-Hour Multi-Model Forecast (ECMWF / GFS)
        ├── [WaterBalanceView.tsx] (Tab: Water Balance)
        │    ├── AWD Status Banner (Permissible vs Irrigation Required)
        │    ├── Root-Zone Soil Water Deficit Gauge (Dt vs RAW / TAW)
        │    └── FAO-56 Penman-Monteith ET0 & ETc Grid
        ├── [FloodHazardView.tsx] (Tab: Flood Hazard)
        │    ├── Early Harvest Directive Banner (RULE-FLD-01)
        │    ├── Haor Flash Flood Hazard Gauge (I_flood)
        │    └── Non-Applicability Notice for High Barind Tract
        └── [ProvenanceView.tsx] (Tab: Transparency & Sources)
             ├── Freshness & Verification Status Table
             ├── Scientific Methodologies Catalog
             └── Non-Goals & Scope Boundaries (DEC-06)
   └── [Footer.tsx] (Institutional Partners, Anti-Overconfidence Disclaimer, Version)
```

---

## 5. Security & Error Handling

1. **Strict Input Sanitization**: All user inputs (Upazila ID, Crop ID, Growth Stage) are validated against backend-supplied metadata before dispatching queries.
2. **Type Safety & Schema Adherence**: Request parameters and response bodies adhere strictly to `[api.ts](file:///Users/kazi/Projects/RITUCAST/frontend/src/types/api.ts)`.
3. **Graceful Degradation**: If an analytical subsystem or network call fails, friendly error panels are displayed with specific error codes, while maintaining active context and allowing single-click retries.
4. **Anti-Overconfidence Standards**: Prohibits words such as "১০০% নিশ্চিত" or "ফলনের নিশ্চয়তা". All advisory outputs enforce the mandatory field inspection notice: *"সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*
