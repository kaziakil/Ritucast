# Ritucast: Product Requirements Document (PRD)

## 1. Executive Product Baseline

### 1.1 Product Summary
**Ritucast** is an agro-climatic decision-support platform that transforms gridded Earth observations (NASA POWER, Sentinel-1 SAR, SMAP, GPM IMERG) and weather forecasts into localized, stage-aware, and explainable farming advisories for Bangladesh.

### 1.2 Target Users
- **Primary Co-Anchors**: Department of Agricultural Extension (DAE) Sub-Assistant Agriculture Officers (SAAOs) and Progressive Lead Farmers / Tubewell Operators.
- **Secondary Beneficiaries**: Marginal Smallholder farming households (via SAAO mediation and shareable visual advisory cards).

### 1.3 Core Strategic Exclusions (Locked Non-Goals)
- **EXC-01**: No sub-acre individual-field parcel boundary delineation or property-level yield guarantees.
- **EXC-02**: No automated pesticide or fungicide chemical spray diagnosis from satellite imagery.
- **EXC-03**: No direct cellular/IoT hardware actuation or remote pump valve controls.
- **EXC-04**: No commercial agrochemical or seed brand endorsements.

---

## 2. Functional Requirements Specification

---

### Category A: Location & Agricultural Context

#### `FR-LOC-01`: Administrative Location Selection Hierarchy
- **Description**: Provide a multi-tier selector allowing users to specify location by Division $\rightarrow$ District $\rightarrow$ Upazila across Bangladesh, defaulting to pilot upazilas (Godagari, Tanore, Sunamganj Sadar, Tahirpur).
- **User Problem**: Farmers and SAAOs need advisories strictly localized to their administrative jurisdiction.
- **Priority**: **P0 (Foundational)**
- **Dependencies**: National Administrative Boundary GeoJSON (BBS / Survey of Bangladesh).
- **Expected Behavior**: Dropdown or searchable modal displays 8 Divisions, 64 Districts, and 495 Upazilas. Selection persists in local storage across browser sessions.
- **Acceptance Criteria**:
  - GIVEN a user on the home screen, WHEN they tap the location header, THEN they can search and select any of the 495 Upazilas within $\le 3$ clicks/taps.
  - Selected upazila persists on page refresh without requiring user re-entry.
- **Success Metric**: `MET-UX-01` (Journey Completion $\ge 85\%$).
- **Limitations**: Coarse boundary polygons; does not resolve union/ward micro-polygons in Phase 2.

#### `FR-LOC-02`: Crop and Phenological Growth Stage Configuration
- **Description**: Enable users to select their active crop and its approximate phenological growth stage.
- **User Problem**: A generic weather forecast is meaningless without knowing whether a crop is in sensitive flowering or harvest maturity.
- **Priority**: **P0 (Foundational)**
- **Dependencies**: BRRI / BARI Crop Phenology Calendar Tables.
- **Expected Behavior**: User selects crop (Boro Rice, Aman Rice, Aus Rice, Potato, Mustard). System dynamically populates standard phenological stages:
  1. *Seedbed / Sowing*
  2. *Transplanting / Early Vegetative*
  3. *Tillering / Stem Elongation*
  4. *Panicle Initiation / Flowering*
  5. *Ripening / Harvest Maturity*
- **Acceptance Criteria**:
  - GIVEN a selected crop, WHEN the user changes the phenological stage, THEN the decision engine recalculates crop water requirement ($ET_c$) using the stage-specific crop coefficient ($K_c$) within $<300\text{ms}$.
- **Success Metric**: `MET-SCI-03` ($ET_c$ Consistency).

#### `FR-LOC-03`: Geolocation Auto-Detection with Safe Fallback
- **Description**: Allow one-tap browser geolocation to identify the nearest Upazila centroid, with graceful manual fallback if GPS is denied or unavailable.
- **User Problem**: Faster onboarding for mobile users who do not want to navigate administrative menus.
- **Priority**: **P1 (Essential)**
- **Dependencies**: Browser HTML5 Geolocation API, Upazila centroid spatial lookup.
- **Expected Behavior**: Prompts user for location permission. If granted, maps coordinates to the containing Upazila polygon. If denied, defaults cleanly to manual dropdown without blocking the app.
- **Acceptance Criteria**:
  - GIVEN GPS permission denied, WHEN app loads, THEN no modal error freezes the UI; manual selector is activated with zero latency.

---

### Category B: Environmental Information

#### `FR-ENV-01`: 7-Day Daily Agro-Meteorological Forecast Summary
- **Description**: Display daily maximum/minimum temperature, precipitation probability (%), expected rainfall amount (mm), average relative humidity (%), and wind speed (km/h) for the selected Upazila.
- **User Problem**: Farmers need reliable 3-to-7 day weather forecasts tailored to field operations.
- **Priority**: **P0 (Foundational)**
- **Dependencies**: NASA POWER Agrometeorology API / Numerical Weather Prediction feeds.
- **Expected Behavior**: Displays a horizontal scrolling or card-based 7-day forecast. Highlights temperature extremes (<10°C cold waves, >35°C heatwaves).
- **Acceptance Criteria**:
  - Temperature displayed in °C with $\pm 1^\circ$ precision; rainfall displayed in mm and categorized (*হালকা*, *মাঝারি*, *ভারী*).
  - Explicit forecast timestamp and data freshness indicator displayed on the screen.
- **Success Metric**: `MET-TECH-02` (Freshness $<4\text{h}$).

#### `FR-ENV-02`: 7-Day Cumulative Precipitation Anomaly Tracking
- **Description**: Compute and display rolling 7-day cumulative rainfall compared against the 10-year seasonal historical baseline for the selected Upazila.
- **User Problem**: Farmers cannot tell if current soil moisture conditions are abnormally wet or dry compared to typical seasonal norms.
- **Priority**: **P1 (Essential)**
- **Dependencies**: GPM IMERG Early/Late precipitation feeds + historical NASA POWER climatology.
- **Expected Behavior**: Shows a simple gauge or bar indicating whether the current week is *স্বাভাবিকের চেয়ে শুষ্ক* (Drier than normal), *স্বাভাবিক* (Normal), or *অস্বাভাবিক বৃষ্টিপাত* (Excess wet).
- **Acceptance Criteria**:
  - Compares current 7-day rolling sum against Upazila 10-year historical mean; classifies deviation into terciles.

#### `FR-ENV-03`: Regional Root-Zone Soil-Moisture Deficit Indicator
- **Description**: Provide a normalized soil-moisture deficit index for the Upazila combining satellite observations with water-balance calculations.
- **User Problem**: Surface soil cracking does not accurately reflect root-zone moisture available to rice crops.
- **Priority**: **P1 (Essential)**
- **Dependencies**: SMAP L3/L4 Soil Moisture products + Penman-Monteith $ET_0$ water balance.
- **Expected Behavior**: Displays root-zone moisture status categorized into: *তীব্র ঘাটতি* (Critical Deficit), *পর্যাপ্ত* (Adequate), or *অতিরিক্ত ভেজা / জলাবদ্ধ* (Saturated/Waterlogged).
- **Acceptance Criteria**:
  - Accompanied by mandatory spatial disclaimer: *"উপজেলা ভিত্তিক আঞ্চলিক উপগ্রহ পর্যবেক্ষণ"* (Upazila-level regional satellite observation).
- **Success Metric**: `MET-SCI-01` (Agreement with BMDA lysimeter benchmarks).

#### `FR-ENV-04`: Radar Surface Inundation & Flood Risk Tracking
- **Description**: Ingest Sentinel-1 C-band SAR radar standing water fraction and combine with upstream catchment rainfall to estimate wetland inundation risk.
- **User Problem**: Pre-monsoon flash floods in the Haor basin submerge Boro rice without overland advance warning.
- **Priority**: **P1 (Essential for Haor Pilot)**
- **Dependencies**: Sentinel-1 SAR GRD water masks + GPM IMERG upstream Meghalaya catchment rainfall tracking.
- **Expected Behavior**: Detects sudden surface water expansion ($\Delta \text{Backscatter} < -3\text{dB}$) and high upstream rainfall ($>100\text{mm}$ in 48h); triggers high-priority warning card.
- **Acceptance Criteria**:
  - GIVEN upstream rainfall $>100\text{mm}$ in 48h, WHEN user views Haor pilot upazila, THEN the system displays the Flash Flood Harvest Urgency card with an alert badge.

#### `FR-ENV-05`: Data Freshness, Observation Timestamps & Source Attribution
- **Description**: Every data card must clearly display when the underlying satellite and weather observations were last updated, citing the provider agency.
- **User Problem**: Stale data masquerading as real-time advice causes agronomic damage and destroys user trust.
- **Priority**: **P0 (Foundational / Safety)**
- **Dependencies**: Pipeline ingestion metadata tables.
- **Expected Behavior**: Clear footer text on every card: *"তথ্য হালনাগাদ: ১০ অক্টোবর, সকাল ০৮:০০ (উৎস: নাসা ও বিএমডি)"*. If data is $>18\text{ hours}$ old, a yellow warning banner appears.
- **Acceptance Criteria**:
  - If data is older than 24 hours, system suppresses definitive advisories and displays a data-refresh disclaimer.

---

### Category C: Agricultural Insights & Advisory Engine

#### `FR-ADV-01`: Weather-Synchronized Irrigation Scheduling Advisory
- **Description**: Synthesize 72-hour precipitation forecasts, soil moisture deficit, and crop $ET_c$ to output a concrete irrigation decision (Postpone vs Irrigate).
- **User Problem**: Running diesel/electric tubewells right before heavy rain wastes money (1,500–2,500 BDT/acre) and leaches fertilizer.
- **Priority**: **P0 (Core Value Proposition)**
- **Dependencies**: FAO-56 Penman-Monteith rules engine, `FR-ENV-01`, `FR-ENV-03`, `FR-LOC-02`.
- **Expected Behavior**:
  - If forecasted rainfall ($P_{\text{forecast}} \ge 15\text{mm}$ with $\text{Probability} \ge 65\%$) within 48h and soil moisture is not in severe deficit $\rightarrow$ Generate **"সেচ স্থগিত রাখুন"** (Postpone Irrigation for 3 Days).
  - If soil moisture is in critical deficit and $P_{\text{forecast}} < 5\text{mm}$ $\rightarrow$ Generate **"জরুরি সেচ প্রয়োগ করুন"** (Apply Irrigation within 48 Hours).
- **Acceptance Criteria**:
  - Recommendation card displays clear Bangla action text, expected fuel/money savings, and local bund check instructions.
- **Success Metric**: `MET-AGR-01` (Avoided pumping hours in Barind pilot).

#### `FR-ADV-02`: Flash-Flood Inundation & Emergency Harvest Advisory
- **Description**: Evaluate upstream Meghalaya catchment rainfall and local radar water levels to issue harvest urgency advisories for Haor Boro rice.
- **User Problem**: Catastrophic loss of mature Boro crop from sudden flash floods in Haor depressions.
- **Priority**: **P1 (Core Value for Haor Pilot)**
- **Dependencies**: `FR-ENV-04`, `FR-LOC-02`.
- **Expected Behavior**:
  - If upstream rainfall exceeds 100mm/48h and rice is in ripening stage ($\ge 80\%$ mature) $\rightarrow$ Issue: **"জরুরি ধান কর্তন সতর্কতা: পাহাড়ি ঢলের আশঙ্কা রয়েছে। ৮০% পরিপক্ক ধান দ্রুত কেটে ফেলুন।"**
- **Acceptance Criteria**:
  - Triggers red alert card with prominent harvesting icon and emergency harvester mobilization advice.

#### `FR-ADV-03`: Safe Agrochemical Spraying & Fertilizer Top-Dressing Window
- **Description**: Evaluate rainfall rate, probability, and wind speed over the next 24–48 hours to identify safe windows for foliar sprays and urea top-dressing.
- **User Problem**: Applying urea or protective sprays immediately before rain washes expensive inputs into irrigation drains.
- **Priority**: **P2 (Valuable)**
- **Dependencies**: Hourly/daily rainfall forecasts, wind speed thresholds.
- **Expected Behavior**:
  - Safe window defined as: Rain probability $<25\%$, rain rate $<1\text{mm/h}$, wind speed $<15\text{km/h}$ for a continuous 12-hour window.
- **Acceptance Criteria**:
  - Displays green "স্প্রে ও সার প্রয়োগের জন্য অনুকূল সময়" (Favorable window) or amber "সার প্রয়োগ স্থগিত রাখুন" (Postpone application due to rain wash-off risk).

#### `FR-ADV-04`: Interactive Explainability Drawer ("কেন এই পরামর্শ?")
- **Description**: Provide an interactive drawer on every advisory card that breaks down the scientific reasoning in plain, accessible Bangla.
- **User Problem**: Farmers and SAAOs reject black-box advice they cannot explain or verify.
- **Priority**: **P0 (Foundational / Safety)**
- **Dependencies**: `FR-ADV-01`, `FR-ADV-02`.
- **Expected Behavior**:
  - Tapping "কেন এই পরামর্শ?" opens an accessible overlay displaying:
    1. *পর্যবেক্ষিত তথ্য (Observed)*: Current soil moisture and past 7-day rain.
    2. *পূর্বাভাস (Forecast)*: Expected rain and temperature over next 48–72h.
    3. *পানির ভারসাম্য (Water Balance)*: Crop daily water need vs incoming rainfall.
    4. *আস্থা বা নির্ভরযোগ্যতা (Confidence Score)*: High / Moderate / Low.
- **Acceptance Criteria**:
  - Drawer opens in $<200\text{ms}$; zero scientific acronyms (e.g., NDVI, ET0) without clear Bangla descriptive labels.
- **Success Metric**: `MET-UX-02` (Advisory Comprehension $\ge 90\%$).

#### `FR-ADV-05`: Transparent Confidence and Uncertainty Rating Display
- **Description**: Every advisory must display an explicit confidence rating (*উচ্চ*, *মাঝারি*, *সীমিত*) reflecting forecast time-decay.
- **User Problem**: Overconfident digital advice leads to severe user disillusionment when a forecast misses.
- **Priority**: **P0 (Foundational / Safety)**
- **Dependencies**: Weather model ensemble spread / forecast horizon decay table.
- **Expected Behavior**:
  - 24–48h horizon: Marked "উচ্চ আস্থা" (High Confidence, if ensemble spread is low).
  - 48–72h horizon: Marked "মাঝারি আস্থা" (Moderate Confidence).
  - $>72\text{h}$ horizon: Marked "প্রাথমিক আভাস" (Preliminary Outlook — requires daily re-checking).
- **Acceptance Criteria**:
  - Confidence indicators use clear text plus iconography; never hidden behind sub-menus.

---

### Category D: Data Presentation & Mobile UX

#### `FR-DSH-01`: Action-First Mobile Dashboard Layout
- **Description**: A streamlined, single-column responsive dashboard designed for budget Android screens (720p resolution, 360px viewport width).
- **User Problem**: Cluttered multi-pane dashboards overwhelm rural smartphone users.
- **Priority**: **P0 (Foundational)**
- **Dependencies**: Mobile-responsive CSS design system.
- **Expected Behavior**: Top section displays Location + Crop Selector; middle section displays the Primary Action Card; bottom section displays 7-Day Forecast & Soil Water Trends.
- **Acceptance Criteria**:
  - Viewport renders cleanly at 360px width without horizontal scrollbars or truncated Bangla characters.

#### `FR-DSH-02`: Upazila Risk Overview Map (Lightweight Vector/Raster Tiles)
- **Description**: An interactive or pre-rendered spatial overview map allowing SAAOs to visualize drought and waterlogging risks across adjacent Upazilas.
- **User Problem**: SAAOs need regional context to evaluate whether a hazard is local or district-wide.
- **Priority**: **P2 (Valuable)**
- **Dependencies**: Pre-rendered map vector/raster tiles, Leaflet/MapLibre client.
- **Expected Behavior**: Map displays choropleth fill by Upazila (Green = Normal, Amber = Moisture Deficit, Blue = Inundation Alert). Tapping an Upazila switches the active dashboard.
- **Acceptance Criteria**:
  - Map tiles load in $<1.5\text{s}$ over 3G; map rendering memory footprint $<40\text{MB}$ RAM.

#### `FR-DSH-03`: Offline PWA Operation and Local Advisory Retention
- **Description**: Implement Progressive Web App (PWA) service workers to cache the application shell and the latest 72-hour upazila advisory data locally in the browser.
- **User Problem**: SAAOs and farmers frequently lose cellular connection while in agricultural fields.
- **Priority**: **P1 (Essential)**
- **Dependencies**: Service Worker Cache API, IndexedDB.
- **Expected Behavior**: When offline, the app opens instantly, displays cached data with an "অফলাইন মোড" (Offline Mode) badge, and displays the exact timestamp of cached observations.
- **Acceptance Criteria**:
  - GIVEN no internet connection, WHEN user opens Ritucast, THEN the dashboard loads cached data within $<1.5\text{s}$ without an empty screen or browser dinosaur error.
- **Success Metric**: `MET-TECH-03` (PWA Cold Load $<3.5\text{s}$ on 3G).

#### `FR-DSH-04`: One-Tap Social & WhatsApp Advisory Card Share
- **Description**: Provide a single-tap button to export an advisory card as a formatted image or clean Bangla text summary for instant sharing via WhatsApp or IMO.
- **User Problem**: SAAOs and lead farmers communicate with marginal farmers through messaging apps.
- **Priority**: **P1 (Essential)**
- **Dependencies**: HTML-to-Canvas / Web Share API.
- **Expected Behavior**: Tapping "শেয়ার করুন" (Share) launches the native OS share sheet or copies an optimized image/card with the Ritucast logo, upazila name, and Bangla advisory.
- **Acceptance Criteria**:
  - Generates a lightweight PNG card ($<250\text{KB}$) within $<500\text{ms}$.

---

## 3. Summary of Functional Requirements by Priority

| Priority Tier | Description | Requirement Count | Requirement IDs |
| :--- | :--- | :---: | :--- |
| **P0 (Foundational)** | Core architectural prerequisites, safety guardrails, and primary irrigation engine. | **7** | `FR-LOC-01`, `FR-LOC-02`, `FR-ENV-01`, `FR-ENV-05`, `FR-ADV-01`, `FR-ADV-04`, `FR-ADV-05`, `FR-DSH-01` |
| **P1 (Essential)** | Core initial release capabilities for pilot testbeds (Haor flood, PWA, share). | **6** | `FR-LOC-03`, `FR-ENV-02`, `FR-ENV-03`, `FR-ENV-04`, `FR-ADV-02`, `FR-DSH-03`, `FR-DSH-04` |
| **P2 (Valuable)** | Enhancements following core journey stability (safe spray window, map tiles). | **2** | `FR-ADV-03`, `FR-DSH-02` |
| **Total Functional Requirements** | | **15** | |
