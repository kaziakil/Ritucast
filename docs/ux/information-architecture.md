# Ritucast Information Architecture Specification

## 1. Executive Summary & Design Rationale

This specification defines the structural navigation model, content hierarchy, and organizational schemas for the Ritucast platform.

### Key Architectural Decisions
1. **Decision-Driven, Not Pipeline-Driven**: The information architecture is organized around the immediate operational decisions farmers and extension officers must make (e.g., *"Should I pump water today?"*, *"Is flash-flood approaching?"*), rather than mirroring the internal data ingestion pipelines (e.g., separate screens for NASA POWER, Sentinel-1, SMAP).
2. **Context-Adaptive Navigation**: The platform dynamically adapts its secondary modules based on the active agro-ecological zone:
   - When a **High Barind Tract** Upazila is active, the third navigation tab renders **মাটি ও সেচ (Soil & Irrigation)**.
   - When a **Haor Basin** Upazila is active, the third navigation tab renders **বন্যা ও প্লাবন (Flood & Inundation)**.
3. **Card-First, Map-Deferred Hierarchy (`ADR-06`, `DEC-09`)**: High-priority operational summaries and actionable advice are presented on lightweight cards in the primary tab. Complex geospatial vector maps (MapLibre GL JS) are isolated into a dedicated fourth tab ("মানচিত্র") to protect mobile TTI and 2GB RAM limits.

---

## 2. Navigation Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│ TOP APP BAR: [ Ritucast Logo ] [ Upazila Selector: গোদাগাড়ী ▾ ] [ ধান ▾ ] │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│                          VIEWPORT CONTENT                              │
│         (Tab 1: Advisory | Tab 2: Weather | Tab 3: Soil/Flood | Tab 4) │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│ BOTTOM NAVIGATION BAR (Mobile):                                        │
│  [ 🌾 আজকের পরামর্শ ]  [ 🌦 আবহাওয়া ]  [ 💧 মাটি/বন্যা ]  [ 🗺 মানচিত্র ]  [ ℹ তথ্য ]  │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Navigation Model Hierarchy

| Level | Navigation Element | Purpose & Behavior |
| :--- | :--- | :--- |
| **Global Header** | **Persistent Context Bar** | Always visible. Displays active Upazila, Crop & Stage selector, and Network/Data Freshness status. Tapping opens Context Modal. |
| **Primary Navigation** | **Bottom Navigation Bar** (Mobile) / **Top Header Bar** (Desktop) | 5 Core destinations: (1) আজকের পরামর্শ, (2) আবহাওয়া, (3) মাটি ও সেচ / বন্যা ও প্লাবন, (4) মানচিত্র, (5) সহায়িকা ও তথ্যসূত্র. |
| **Secondary Navigation** | **Sub-Tabs / Time Switcher** | Present within modules (e.g., in Weather: *আজকের আবহাওয়া* vs *৪৮ ঘণ্টা পূর্বাভাস* vs *৭ দিনের ধারা*). |
| **Contextual Overlays** | **Slide-Up Bottom Drawers** | Non-disruptive inspection of data provenance (*তথ্যসূত্র ও সময়*), scientific explainability (*কেন এই পরামর্শ?*), and share sheets. |

---

## 3. Structural Module Specifications

### 3.1 Module 1: আজকের পরামর্শ (Today's Advisory / Overview)
- **Purpose**: The primary daily landing destination. Delivers immediate operational clarity in under 5 seconds.
- **Target Users**: Lead Farmers, SAAOs, UAOs.
- **Content Hierarchy**:
  1. *Emergency Alert Banner* (if active flash flood, high heat, or advisory suppression is triggered).
  2. *Tier 4 Actionable Recommendation Card* (e.g., "আজ সেচ দেওয়ার প্রয়োজন নেই" with Bangla explanation and mandatory field verification copy).
  3. *Today's Environmental Snapshot* (Current temperature, 24h rainfall, soil moisture status).
  4. *Quick Action Floating Bar* (Share to WhatsApp, Check Soil).
- **Failure / Gating State**: If Crop/Stage is unconfirmed, displays the Context Gating card with a 1-tap stage selector.

---

### 3.2 Module 2: আবহাওয়া ও পূর্বাভাস (Weather & Climate Forecast)
- **Purpose**: Comprehensive agro-meteorological monitoring and rain likelihood planning.
- **Target Users**: SAAOs, Lead Farmers.
- **Content Hierarchy**:
  1. *Sub-Tab 1: বর্তমান অবস্থা (Empirical Observations - Tier 1)*: BMD station / NASA POWER temperature, humidity, solar radiation, wind speed.
  2. *Sub-Tab 2: ৪৮ ঘণ্টার পূর্বাভাস (Rainfall & NWP - Tier 3)*: 3-hour precipitation probability bar chart, expected rainfall volume (mm), multi-model ensemble spread indicator.
  3. *Sub-Tab 3: ৭ দিনের প্রবণতা (Weekly Trend)*: Extended outlook with confidence degradation markers.

---

### 3.3 Module 3A: মাটি ও সেচ (Soil & Irrigation — Barind Mode)
- **Active When**: Upazila is in High Barind Tract (Godagari, Tanore).
- **Purpose**: Groundwater conservation and diesel expenditure management via Alternate Wetting and Drying (AWD) principles.
- **Target Users**: Barind Farmers, DTW Pump Managers, SAAOs.
- **Content Hierarchy**:
  1. *Daily Soil Water Balance Card (Tier 2)*: Root-zone water deficit ($D_t$) gauge comparing current depletion against Readily Available Water ($RAW$).
  2. *Evapotranspiration Summary*: Reference $ET_0$ (FAO-56 Penman-Monteith) and crop evapotranspiration ($ET_c = K_c \times ET_0$).
  3. *AWD Field Tube Verification Guide*: Diagram illustrating how to check the perforated plastic pipe in the field.
  4. *Irrigation Cost Savings Calculator*: Cumulative taka saved from postponed pump hours.

---

### 3.3 Module 3B: বন্যা ও প্লাবন (Flood & Inundation — Haor Mode)
- **Active When**: Upazila is in Haor Basin (Sunamganj Sadar, Tahirpur).
- **Purpose**: Pre-monsoon flash-flood advance warning and emergency harvest decision-making.
- **Target Users**: Haor Boro Farmers, Embankment Committees, SAAOs.
- **Content Hierarchy**:
  1. *Haor Composite Hazard Level (Tier 2)*: 3-Tier gauge (স্বাভাবিক / সতর্কবার্তা / জরুরি সতর্কতা) based on $I_{\text{flood}}$ (`DEC-16`).
  2. *Upstream Meghalaya Catchment Rainfall ($P_{\text{cat}}$)*: 48-hour GPM IMERG satellite rainfall sum over the Meghalaya hills with flood threshold markers.
  3. *Surma River Gauge Status*: River water level distance from Danger Level ($DL - H_t$) and 24h rate of rise ($\Delta H/\Delta t$).
  4. *Crop Harvest Maturity Action Guide*: Phenology-based guidance (e.g., harvest if $\ge 80\%$ ripe; prepare thresher).

---

### 3.4 Module 4: মানচিত্র ও বিশ্লেষণ (Geospatial Diagnostic Map)
- **Purpose**: Regional spatial analysis and visual validation across Upazila boundaries.
- **Target Users**: SAAOs, UAOs, Technical Farmers.
- **Behavior**: **Lazy-loaded**. MapLibre GL JS engine and vector tile layers are only initialized when the user clicks this tab.
- **Content Hierarchy**:
  1. *Layer Switcher*:
     - Upazila Administrative Boundaries (Pilot testbeds highlighted).
     - Rainfall Anomaly / 48h Rain Forecast Heatmap.
     - Sentinel-1 SAR Surface Water & Inundation Extent.
     - SMAP / Soil Water Deficit Spatial Grid.
  2. *Legend & Unit Scale*: Explains color ramps and spatial grid resolution (e.g., "প্রতিটি গ্রিড ১০x১০ কিমি").
  3. *Spatial Disclaimer Banner*: Reminds users that satellite layers provide regional context, not sub-acre boundaries.

---

### 3.5 Module 5: সহায়িকা ও তথ্যসূত্র (Help, Data Sources & Methodology)
- **Purpose**: Scientific transparency, institutional trust, and user education.
- **Target Users**: All.
- **Content Hierarchy**:
  1. *About Ritucast*: Mission, institutional partners (DAE, BRRI, BMD, BWDB).
  2. *Scientific Methodology*: Plain-language explanation of FAO-56 Penman-Monteith, AWD irrigation, and satellite radar.
  3. *Data Sources Registry*: Live status and update cadences for NASA POWER, Sentinel-1, GPM, and BMD.
  4. *Agronomic Glossary*: Bangla agrarian terms explained.
  5. *DAE Emergency Contact Directory*: Local SAAO and Upazila Agriculture Office phone numbers.

---

## 4. Contextual Actions & Floating Utility Patterns

1. **One-Tap Share Sheet**: Persistent share icon on all advisory and alert cards triggering native Web Share or WhatsApp image card export (`FR-DSH-04`).
2. **Context Gating Switcher**: Tap on the header location/crop badge opens a slide-up modal to switch Upazila or update crop growth stage in $\le 2$ taps.
3. **Data Quality & Freshness Indicator**: Tap on the status pill in the header displays exact observation timestamps and data provider latency.
