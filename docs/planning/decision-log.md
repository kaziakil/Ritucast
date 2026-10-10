# Ritucast: Project Decision Log

## 1. Decision Log Governance

This document records architectural, strategic, and product decisions made throughout the Ritucast project lifecycle. Every entry documents:
- **Decision ID & Title**
- **Date & Phase**
- **Context & Problem Statement**
- **Options Considered & Trade-offs**
- **Decision Taken & Rationale**
- **Impact & Downstream Dependencies**
- **Approval Status**

---

## 2. Phase 1 Architecture & Product Decisions

---

### DEC-01: Adoption of 18-Phase Governed Development Lifecycle
- **Date**: 2026-10-10 (Phase 1)
- **Status**: **Approved**
- **Context**: Large-scale agricultural technology platforms frequently suffer from premature optimization, ungrounded feature creep, or incomplete scientific validation if driven solely by rapid prototyping.
- **Alternatives Considered**:
  - *Option A*: Unstructured agile development (rapid sprint prototyping without formal phase boundaries).
  - *Option B*: Traditional heavy waterfall with no intermediate iterations.
  - *Option C (Selected)*: Disciplined 18-phase development roadmap with rigorous entry/exit criteria, formal phase artifacts, and change management.
- **Rationale**: An 18-phase model enforces scientific validation, user alignment, and architecture stability before heavy code deployment.
- **Downstream Impact**: Phases 2–18 remain strictly pending until prerequisite phase quality gates are validated and accepted.

---

### DEC-02: User Segment Selection: The Dual-Anchor Model (SAAOs + Lead Farmers)
- **Date**: 2026-10-10 (Phase 1)
- **Status**: **Approved**
- **Context**: Over 80% of Bangladesh farmers are smallholders with varying literacy, smartphone access, and digital confidence. Direct-to-marginal-farmer apps often suffer from high churn.
- **Alternatives Considered**:
  - *Option A*: Direct-to-Consumer (D2C) targeting all 16 million smallholder farmers via a mobile app.
  - *Option B*: Institutional-only B2G tool serving only Dhaka-level DAE directors and researchers.
  - *Option C (Selected)*: **Dual-Anchor Model**—co-targeting frontline extension officers (SAAOs) and progressive lead farmers / tubewell managers as primary users.
- **Rationale**: SAAOs already visit farmers weekly and possess agronomic training to interpret data. Lead farmers have smartphones, manage irrigation capital, and influence neighboring smallholders.
- **Downstream Impact**: Drives Phase 2 persona creation, Phase 6 information architecture, and Phase 7 UI design (dual quick-action vs diagnostic modes).

---

### DEC-03: Geographic Scope: Dual-Zone Calibrated Pilot with National Background
- **Date**: 2026-10-10 (Phase 1)
- **Status**: **Approved**
- **Context**: Bangladesh possesses 30 distinct Agro-Ecological Zones (AEZs). Calibrating micro-models across all zones in the initial release risks broad, inaccurate advisories.
- **Alternatives Considered**:
  - *Option A*: Full 64-district national rollout on Day 1.
  - *Option B*: Single-district micro pilot (e.g., only Rajshahi Sadar).
  - *Option C (Selected)*: **Dual-Zone Representative Pilot** (Barind Tract for drought/irrigation; Haor Basin for flash flood/inundation) paired with a coarse **National Background Agro-Weather Tier**.
- **Rationale**: Tests both critical agro-climatic extremes (acute water deficit vs. catastrophic sudden flooding) on high-value Boro rice, while keeping algorithmic tuning manageable.
- **Downstream Impact**: Defines testbed regions for Phase 3 data gathering, Phase 4 agronomic models, and Phase 14 usability testing.

---

### DEC-04: Remote Sensing Modality Hierarchy: Cloud-Penetrating Priority
- **Date**: 2026-10-10 (Phase 1)
- **Status**: **Approved**
- **Context**: Bangladesh experiences persistent cloud cover (80–90%) throughout the monsoon (June–October), rendering optical sensors (MODIS, Sentinel-2) blind for multi-week stretches.
- **Alternatives Considered**:
  - *Option A*: Optical-first architecture (NDVI/EVI primary).
  - *Option B (Selected)*: Radar and microwave priority (Sentinel-1 C-band SAR + GPM IMERG microwave precipitation) for waterlogging and flood risk, utilizing optical indices strictly as secondary or dry-season indicators.
- **Rationale**: Guarantees system resilience during the most hazardous wet months when smallholders face peak flood and waterlogging risks.
- **Downstream Impact**: Shapes Phase 3 dataset validation and Phase 8 data ingestion pipelines.

---

### DEC-05: Product Positioning: Agro-Climatic Decision Support System (DSS)
- **Date**: 2026-10-10 (Phase 1)
- **Status**: **Approved**
- **Context**: Need to define clear product boundaries between a simple weather app and an unfeasible farm-automation platform.
- **Alternatives Considered**:
  - *Option A*: Generic Agricultural Information Portal (news, static crop lists).
  - *Option B*: Raw Satellite Visualization Dashboard (academic GIS tool).
  - *Option C (Selected)*: **Agro-Climatic Decision-Support System with Real-Time Risk Awareness**.
- **Rationale**: Fills the specific unaddressed gap in Bangladesh agriculture: translating environmental observations into actionable operational guidance (when to irrigate, when to harvest, when to prepare for inundation).
- **Downstream Impact**: Guides Phase 2 requirements specification and Phase 9 recommendation engine design.

---

### DEC-06: Explicit Exclusions from Initial Product Scope
- **Date**: 2026-10-10 (Phase 1)
- **Status**: **Approved**
- **Context**: High-risk capabilities can easily derail timelines and compromise credibility if unvalidated.
- **Decided Exclusions for Initial Release**:
  1. *No individual-field farm-level yield guarantees.*
  2. *No computer-vision disease diagnosis from coarse satellite data.*
  3. *No automated irrigation actuator or machinery IoT controls.*
  4. *No commercial brand advertising or input endorsements.*
- **Rationale**: Protects scientific credibility, prevents legal/agronomic liabilities, and maintains laser focus on core decision-support value.
- **Downstream Impact**: Keeps Phase 2 feature prioritization focused and achievable.

---

## 3. Phase 2 Requirements & Product Strategy Decisions

---

### DEC-07: Minimum Complete Product (MCP) Definition
- **Date**: 2026-10-10 (Phase 2)
- **Status**: **Approved**
- **Context**: Need to define what constitutes the smallest meaningful initial release that delivers real farmer value without feature creep.
- **Alternatives Considered**:
  - *Option A*: Basic weather and NDVI dashboard (fast, but lacks decision utility).
  - *Option B*: Full national platform across 30 AEZs with yield models and SMS push (unrealistic initial scope).
  - *Option C (Selected)*: **Minimum Complete Product (MCP)**: End-to-end irrigation scheduling and Haor flash-flood emergency harvest advisory in Bangla, tested across Barind and Haor pilot zones on Boro rice, delivered as an offline-capable PWA (<1.5MB).
- **Rationale**: Demonstrates concrete economic savings (avoided pumping fuel) and catastrophe prevention (early harvest) with high agronomic credibility.
- **Downstream Impact**: Locks the P0 and P1 feature set for Phase 3 and beyond.

---

### DEC-08: Adoption of 4-Tier Information Taxonomy for Scientific Safety
- **Date**: 2026-10-10 (Phase 2)
- **Status**: **Approved**
- **Context**: Blurring the lines between empirical measurements and model forecasts leads to false certainty and destroys trust.
- **Decision Taken**: Formally classify and visually delineate all platform outputs into: (1) Empirical Observations, (2) Derived Agronomic Indicators, (3) Probabilistic Predictions, and (4) Actionable Recommendations (`NFR-SCI-01`).
- **Rationale**: Protects farmers from mistaking 48-hour probabilistic forecasts for guaranteed certainties.
- **Downstream Impact**: Drives Phase 6 Information Architecture, Phase 7 UI badge design, and Phase 9 Advisory Engine.

---

### DEC-09: Enforcement of Strict Hardware and Payload Budgets
- **Date**: 2026-10-10 (Phase 2)
- **Status**: **Approved**
- **Context**: Rural Bangladesh users operate low-cost Android phones (2GB–3GB RAM, 720p screens) on variable 3G cellular networks.
- **Decision Taken**: Enforce a strict initial client bundle size $\le 1.5\text{MB}$, Time-to-Interactive $\le 3.5\text{s}$ on throttled 3G, and peak client heap memory $\le 45\text{MB}$.
- **Rationale**: Prevents application crashes and high data-cost barriers for smallholder and extension users.
- **Downstream Impact**: Constrains Phase 5 technology choices and Phase 11 frontend dependencies (disallows heavy monolithic GIS libraries).

---

### DEC-10: Automated Recommendation Suppression Policy
- **Date**: 2026-10-10 (Phase 2)
- **Status**: **Approved**
- **Context**: Presenting stale or highly uncertain predictions as active agricultural advice risks severe crop damage.
- **Decision Taken**: Enforce automated suppression of definitive action cards if weather data is $>36\text{ hours}$ old (`NFR-REL-03`) or if weather model ensemble spread exceeds 50%, falling back to a safe advisory to inspect fields and consult local SAAOs.
- **Rationale**: Prioritizes farmer safety and organizational credibility over false availability.
- **Downstream Impact**: Informs Phase 8 data freshness tracking and Phase 9 recommendation fallback rules.

---

## 4. Phase 3 Dataset Research & Validation Decisions

---

### DEC-11: Selection of 8-Dataset Initial Release Core Stack
- **Date**: 2026-10-10 (Phase 3)
- **Status**: **Approved**
- **Context**: Need to lock the minimal defensible data stack supporting the Minimum Complete Product (MCP) without unnecessary technical complexity or data bloat.
- **Decision Taken**: Formally select 8 core datasets: (1) NASA POWER Daily Agrometeorology (`DATA-MET-01`), (2) Open-Meteo Operational NWP Forecasts (`DATA-FCST-01`), (3) GPM IMERG V07 Precipitation (`DATA-PCP-01`), (4) Sentinel-1 C-Band SAR GRD (`DATA-SAR-01`), (5) SMAP Enhanced L3 9km Soil Moisture (`DATA-SMC-01`), (6) BRRI/BARI Phenology & $K_c$ Tables (`DATA-AGR-01`), (7) Bangladesh Admin Boundaries GeoJSON (`DATA-BND-01`), and (8) BWDB River Stage Logs (`DATA-HYD-01`).
- **Rationale**: Every selected dataset directly fulfills a locked Phase 2 functional requirement and has been verified via live API queries for Bangladesh.
- **Downstream Impact**: Directs Phase 4 scientific validation planning and Phase 8 ETL ingestion architecture.

---

### DEC-12: Adoption of Sentinel-1 C-Band SAR as Primary Monsoon Inundation Modality
- **Date**: 2026-10-10 (Phase 3)
- **Status**: **Approved**
- **Context**: Monsoon cloud cover (80–90%) blinds optical sensors (Sentinel-2, MODIS) during the crucial pre-monsoon and monsoon flood seasons in Bangladesh.
- **Decision Taken**: Mandate Sentinel-1 C-band Synthetic Aperture Radar (SAR) as the primary satellite sensor for mapping standing floodwater and waterlogging in the Haor basin.
- **Rationale**: C-band radar at 5.405 GHz is 100% cloud-penetrating; live CDSE OData testing confirmed immediate product publication within 2 hours and 5 minutes of sensing over Bangladesh.
- **Downstream Impact**: Shapes Phase 4 flood rule calibration and Phase 8 radar GRD backscatter thresholding workflows.

---

### DEC-13: Selection of Open-Meteo for Operational NWP Weather Forecast Feeds
- **Date**: 2026-10-10 (Phase 3)
- **Status**: **Approved**
- **Context**: Need a reliable, non-commercial, lightweight REST API for 7-day precipitation, temperature, and wind forecasts without paid API keys or restrictive quotas.
- **Decision Taken**: Select Open-Meteo API (aggregating ECMWF IFS 9km and NOAA GFS 13km models) as the primary operational forecast provider for the MCP.
- **Rationale**: Completely open, CC-BY 4.0 license, 10,000 calls/day free quota, delivers lightweight JSON payloads directly to backend caches with zero client API keys.
- **Downstream Impact**: Powers Phase 10 backend weather endpoints and Phase 11 client forecast views.

---

### DEC-14: Formal Deferral of Sentinel-2 MSI Optical Imagery & Commercial Datasets
- **Date**: 2026-10-10 (Phase 3)
- **Status**: **Approved**
- **Context**: Evaluating high-resolution optical imagery, digital soil property maps, and commercial financial/insurance datasets.
- **Decided Actions**:
  1. *Defer Sentinel-2 MSI* to Phase 12 due to severe monsoon cloud contamination and excessive raw data volume (~1GB/scene).
  2. *Defer SRDI/SoilGrids* to Phase 4 for baseline soil water-holding capacity calibration.
  3. *Reject private crop insurance claims and farmer loan records* to enforce privacy-by-design (`NFR-SEC-01`) and avoid irrelevant proprietary dependencies.
  4. *Reject CROP-CASMA* because it is strictly restricted to the Contiguous United States (CONUS).
- **Rationale**: Keeps the project strictly focused on achievable smallholder decision support and prevents privacy/bandwidth violations.
- **Downstream Impact**: Eliminates unnecessary data licensing and infrastructure overhead from Phase 5 and Phase 8.

---

## 5. Phase 4 Agricultural Knowledge & Scientific Validation Decisions

---

### DEC-15: Baseline Priority Mandate: Physical & Mechanistic Models First
- **Date**: 2026-10-10 (Phase 4)
- **Status**: **Approved**
- **Context**: Premature application of machine learning or deep learning to agricultural advisory generation introduces severe hallucination risks, overfitting on sparse labels, and opaque "black-box" decision making.
- **Decision Taken**: Formally mandate Level 1 physical and mechanistic models (FAO-56 Penman-Monteith $ET_0$, mass-balance soil water deficit $D_t$, and deterministic thermal/flood rules) as the primary operational baseline for the Minimum Complete Product (MCP). Machine learning models may only be considered in Phase 9/15 if they satisfy 6 strict readiness gates and demonstrate statistically significant ($p < 0.01$) outperformance on independent hold-out test sets.
- **Rationale**: Physical models are physically grounded, explainable to agronomists and farmers, and have zero risk of statistical overfitting.
- **Downstream Impact**: Guides Phase 5 system architecture, Phase 8 data pipelines, and Phase 9 recommendation engine design.

---

### DEC-16: Formulation of the Multi-Factor Haor Flash-Flood Index ($I_{\text{flood}}$)
- **Date**: 2026-10-10 (Phase 4)
- **Status**: **Approved**
- **Context**: Sentinel-1 SAR has a 6–12 day revisit period, which cannot catch rapid 48-hour flash floods alone; in-situ river gauges give only short localized warning; local rainfall fails to capture transboundary cloudbursts occurring in Meghalaya.
- **Decision Taken**: Combine four independent proxies into a normalized composite Flash Flood Hazard Index: (1) Meghalaya Catchment 48h GPM IMERG rainfall ($w_1 = 0.35$), (2) BWDB Surma River stage proximity to Danger Level ($w_2 = 0.30$), (3) Surma River 24h rate of rise ($w_3 = 0.20$), and (4) Sentinel-1 SAR surface water area ($w_4 = 0.15$).
- **Rationale**: Provides 48–72 hours of predictive lead time for early harvest alerts (`RULE-FLD-01`), overcoming the satellite revisit gap while preventing false alarms.
- **Downstream Impact**: Shapes Phase 5 data model, Phase 8 catchment aggregation, and Phase 9 flood alert logic.

---

### DEC-17: Mandatory Contextual Gating Policy for Advisory Generation
- **Date**: 2026-10-10 (Phase 4)
- **Status**: **Approved**
- **Context**: Agricultural operations are highly non-linear. An action that saves water during vegetative tillering (drying soil under AWD) causes catastrophic spikelet sterility if applied during anthesis (flowering).
- **Decision Taken**: Strictly prohibit the recommendation engine from executing or emitting any actionable advisory without verified confirmation of three mandatory parameters: (1) Administrative Upazila, (2) Active Crop, and (3) Active Phenological Growth Stage.
- **Rationale**: Enforces the "Do No Harm" agronomic safety mandate and prevents misleading guidance.
- **Downstream Impact**: Informs Phase 5 API request validation, Phase 6 user journey design, and Phase 9 advisory engine.

---

### DEC-18: Quantitative Advisory Confidence Scoring and Ensemble Degradation Math
- **Date**: 2026-10-10 (Phase 4)
- **Status**: **Approved**
- **Context**: Need a rigorous mathematical formula to quantify advisory confidence, decay confidence over lead times, and trigger automated suppression during high forecast uncertainty.
- **Decision Taken**: Adopt the quantitative formulation: $C_{\text{adv}} = C_{\text{base}} \times \exp(-\lambda \cdot t_{\text{lead}}/24) \times f_{\text{ensemble}}(S_{\text{spread}}) \times f_{\text{freshness}}(\Delta t_{\text{data}})$, with $\lambda = 0.12$. Categorize into High ($\ge 0.80$), Moderate ($0.60–0.79$), Low ($0.40–0.59$), and Suppressed ($<0.40$).
- **Rationale**: Mathematically enforces honest communication of uncertainty, aligns with the 4-tier taxonomy, and guarantees automated suppression when data is stale ($>36\text{h}$) or model disagreement exceeds $50\%$.
- **Downstream Impact**: Directs Phase 5 data structures, Phase 9 advisory calculation, and Phase 11 UI badge rendering.

---

## 6. Phase 5 System Architecture & Technology Decisions

---

### DEC-19: Selection of Decoupled Modular Architecture
- **Date**: 2026-10-10 (Phase 5)
- **Status**: **Approved**
- **Context**: The platform requires strong separation between UI presentation, analytical computations, and asynchronous geospatial ingestion without incurring the operational overhead of microservices or Kubernetes.
- **Alternatives Considered**:
  - *Option A*: Traditional Monolith (Django / Laravel with server-side templates).
  - *Option B*: Full Microservices (separate containers for Auth, Weather, Ingestion, Maps, Advisories).
  - *Option C*: Full Serverless (AWS Lambda / Google Cloud Functions for all processing).
  - *Option D (Selected)*: **Decoupled Modular Architecture** (FastAPI backend + Celery workers + PostGIS/Redis + Static React/Vite PWA client).
- **Rationale**: Keeps total cloud hosting costs $\le \$65/\text{month}$, eliminates distributed transaction complexity, preserves modular boundaries for future extraction, and enables static edge-caching of the PWA bundle.
- **Downstream Impact**: Informs repository layout, Docker Compose configs, and Phase 8–11 development workflows. Ref: [ADR-01](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-01-decoupled-modular-architecture.md).

---

### DEC-20: Frontend Stack: React 18, TypeScript, Vite, and Vanilla CSS Tokens
- **Date**: 2026-10-10 (Phase 5)
- **Status**: **Approved**
- **Context**: Target rural users operate budget Android devices (2GB–3GB RAM) over 3G cellular networks, requiring bundle size $\le 1.5\text{MB}$, TTI $\le 3.5\text{s}$, and heap $\le 45\text{MB}$.
- **Alternatives Considered**:
  - *Option A*: React with Tailwind CSS and Next.js SSR.
  - *Option B*: Vue.js / Nuxt.js.
  - *Option C (Selected)*: **React 18 + TypeScript + Vite + Vanilla CSS Custom Properties (Tokens)**.
- **Rationale**: Eliminates Tailwind runtime overhead and heavy utility classes; Vanilla CSS tokens provide full control over typography, high-contrast theming, and micro-animations while keeping production JS/CSS payloads under 350KB gzipped (well within the 1.5MB budget).
- **Downstream Impact**: Directs Phase 7 design system tokens and Phase 11 frontend development. Ref: [ADR-03](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-03-react-typescript-vanilla-css.md).

---

### DEC-21: Backend & Spatial Datastore: FastAPI, Python 3.11, PostgreSQL 16 + PostGIS 3.4
- **Date**: 2026-10-10 (Phase 5)
- **Status**: **Approved**
- **Context**: Scientific equations (FAO-56, water balance) and geospatial manipulation (GeoJSON, rasters) require native Python ecosystem integration and high-performance vector spatial indexing.
- **Alternatives Considered**:
  - *Option A*: Node.js (Express/NestJS) with MongoDB.
  - *Option B*: Go with PostgreSQL.
  - *Option C (Selected)*: **FastAPI + Python 3.11 + Pydantic v2 + PostgreSQL 16 / PostGIS 3.4 + Redis 7**.
- **Rationale**: Direct interoperability with NumPy, SciPy, and Rasterio; Pydantic v2 delivers high-speed validation for advisory schemas; PostGIS provides native spatial queries (e.g., `ST_Contains`, `ST_Intersects`) for Upazila administrative polygons.
- **Downstream Impact**: Directs Phase 8 pipelines, Phase 9 analytics engine, and Phase 10 API implementation. Ref: [ADR-02](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-02-fastapi-backend.md), [ADR-04](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-04-postgis-spatial-datastore.md).

---

### DEC-22: Asymmetric Regional Pipelines for Pilot Testbeds
- **Date**: 2026-10-10 (Phase 5)
- **Status**: **Approved**
- **Context**: Barind irrigation management operates on a slow, cumulative 24-hour evaporative cycle, whereas Haor flash floods develop within 6–12 hours of transboundary Meghalaya rainfall spikes.
- **Alternatives Considered**:
  - *Option A*: Uniform daily 24h cron schedule across all regions.
  - *Option B*: Uniform 1-hour polling across all regions.
  - *Option C (Selected)*: **Asymmetric Regional Pipelines** (Daily 24h pipeline for Barind Tract; 6-hourly pipeline with rapid-poll fallback for Haor Basin).
- **Rationale**: Prevents costly compute and API waste in Barind while guaranteeing timely early-harvest warnings in Haor before upstream runoff inundates Boro fields.
- **Downstream Impact**: Defines Celery beat schedules in Phase 8 and alert generation triggers in Phase 9. Ref: [ADR-07](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-07-asymmetric-regional-pipelines.md).

---

### DEC-23: Centralized Automated Suppression Middleware
- **Date**: 2026-10-10 (Phase 5)
- **Status**: **Approved**
- **Context**: Strict adherence to the `DEC-10` automated suppression policy requires an infallible mechanism to prevent stale (>36h) or highly uncertain advisory delivery.
- **Alternatives Considered**:
  - *Option A*: Client-side advisory filtering in React.
  - *Option B*: Ad-hoc `if` statements inside individual analytics functions.
  - *Option C (Selected)*: **Centralized FastAPI Middleware (`AdvisorySuppressionMiddleware`)**.
- **Rationale**: Intercepts all outgoing recommendation payloads before serialization; guarantees that even if a buggy algorithmic heuristic emits an advisory, it is suppressed server-side and replaced with the safe field-verification notice.
- **Downstream Impact**: Informs Phase 10 API gateway security and Phase 13 integration test suite. Ref: [ADR-08](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-08-automated-suppression-middleware.md).

---

## 7. Phase 6 Information Architecture & UX Decisions

---

### DEC-24: Decision-Driven, Non-Pipeline Navigation Architecture
- **Date**: 2026-10-10 (Phase 6)
- **Status**: **Approved**
- **Context**: Organizing the user interface around internal remote sensing datasets (e.g., separate tabs for NASA, Sentinel-1, SMAP) confuses farmers and extension workers who think in operational farming questions.
- **Alternatives Considered**:
  - *Option A*: Dataset-centric navigation (Tabs: Satellite Radar, Weather API, Soil Moisture, Predictions).
  - *Option B*: Map-first GIS layout (Interactive map as primary landing view).
  - *Option C (Selected)*: **Decision-Driven 5-Item Navigation** (`আজকের পরামর্শ`, `আবহাওয়া ও পূর্বাভাস`, `মাটি ও সেচ / বন্যা ও প্লাবন`, `মানচিত্র ও বিশ্লেষণ`, `সাহায্য ও তথ্যসূত্র`).
- **Rationale**: Places immediate operational advice on the home screen; maps and technical indicators are progressively disclosed when needed.
- **Downstream Impact**: Guides Phase 7 navigation design tokens, Phase 11 client routing, and Phase 14 usability testing. Ref: [information-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/ux/information-architecture.md).

---

### DEC-25: Context-Adaptive Regional Navigation Switching
- **Date**: 2026-10-10 (Phase 6)
- **Status**: **Approved**
- **Context**: The High Barind Tract faces chronic groundwater drought, requiring AWD irrigation scheduling; the Haor Basin faces catastrophic sudden flash floods, requiring emergency harvest warnings. Forcing both into static tabs creates irrelevant visual clutter.
- **Alternatives Considered**:
  - *Option A*: Static tabs displaying both Soil and Flood modules simultaneously across all regions.
  - *Option B*: Separate standalone web apps for Barind and Haor.
  - *Option C (Selected)*: **Context-Adaptive Navigation Module (Module 3)**. Dynamically renders `মাটি ও সেচ` when a Barind Upazila is active, and `বন্যা ও প্লাবন` when a Haor Upazila is active.
- **Rationale**: Maintains a unified codebase and seamless user experience while delivering hyper-relevant local decision support.
- **Downstream Impact**: Directs Phase 7 component states and Phase 11 React routing logic. Ref: [information-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/ux/information-architecture.md).

---

### DEC-26: Chip Modal Location Selection over Interactive Map Picker
- **Date**: 2026-10-10 (Phase 6)
- **Status**: **Approved**
- **Context**: Rural target users operate budget Android devices (2GB RAM) over 3G cellular connections. Forcing an interactive map canvas render solely to select an Upazila creates 5–8 second latency and high crash rates (`RSK-19`, `DEC-09`).
- **Alternatives Considered**:
  - *Option A*: Map-click-only location picker.
  - *Option B*: Standard browser HTML dropdown `<select>`.
  - *Option C (Selected)*: **High-Performance Chip & Search Bottom Sheet Modal** (Instant load <100ms; quick chips for pilot Upazilas; fuzzy Bangla text search).
- **Rationale**: Enables location selection in $\le 2$ taps and $\le 3$ seconds on budget smartphones without loading heavy WebGL map assets.
- **Downstream Impact**: Shapes Phase 7 modal wireframes and Phase 11 state persistence. Ref: [geographic-context-and-selection.md](file:///Users/kazi/Projects/RITUCAST/docs/ux/geographic-context-and-selection.md).

---

### DEC-27: 8-Layer Agricultural Insight Hierarchy and Non-Color-Only Accessibility Mandate
- **Date**: 2026-10-10 (Phase 6)
- **Status**: **Approved**
- **Context**: Agricultural operations carry significant economic and food security risks. Ambiguous color indicators or blurring observations with predictions leads to false confidence or dangerous inaction.
- **Alternatives Considered**:
  - *Option A*: Single unified risk score badge (e.g., "Risk: 7/10").
  - *Option B*: Color-coded status dots without text labels.
  - *Option C (Selected)*: **8-Layer Information Hierarchy with Non-Color-Only WCAG 2.2 AA Enforcement**. Every card pairs color with a distinct glyph icon (`[✓]`, `[⚠️]`, `[🚨]`) and descriptive text label.
- **Rationale**: Guarantees legibility in intense outdoor sunlight and accessibility for color-blind farmers while strictly upholding the `DEC-08` information taxonomy.
- **Downstream Impact**: Governs Phase 7 design system token pairing and Phase 11 accessible component templates. Ref: [agricultural-insight-information-model.md](file:///Users/kazi/Projects/RITUCAST/docs/ux/agricultural-insight-information-model.md), [accessibility-localization-and-connectivity.md](file:///Users/kazi/Projects/RITUCAST/docs/ux/accessibility-localization-and-connectivity.md).

---

## 8. Phase 7 Visual Design & Design System Decisions

---

### DEC-28: Solar Light Theme and High-Contrast Agronomic Palette
- **Date**: 2026-10-10 (Phase 7)
- **Status**: **Approved**
- **Context**: Rural extension officers and lead farmers operate mobile devices in direct outdoor sunlight across open rice fields. Low-contrast pastel tones, dark-mode default interfaces, and translucent glassmorphism wash out completely under 80,000–100,000 lux outdoor solar illumination.
- **Alternatives Considered**:
  - *Option A*: Dark-mode default palette (high glare and reflection in outdoor fields).
  - *Option B*: Standard SaaS pastel palette (washed out in high ambient daylight).
  - *Option C (Selected)*: **Solar Light Theme with $\ge 7:1$ High-Contrast Agronomic Color System**. Off-white canvas (`#F8FAF8`), crisp white surfaces (`#FFFFFF`), deep ink charcoal text (`#111827`, $16.1:1$ contrast ratio), deep forest green primary accents (`#1B4332`), and high-saturation semantic status colors.
- **Rationale**: Guarantees legibility under harsh glare while projecting grounded scientific authority and calm confidence, exceeding WCAG 2.2 Level AAA contrast for primary body copy.
- **Downstream Impact**: Informs Phase 7 CSS custom properties, Phase 11 client stylesheet, and Phase 14 field readability validation. Ref: [visual-direction.md](file:///Users/kazi/Projects/RITUCAST/docs/design/visual-direction.md), [color-system.md](file:///Users/kazi/Projects/RITUCAST/docs/design/color-system.md).

---

### DEC-29: Vanilla CSS Custom Properties Token Architecture (Zero Tailwind)
- **Date**: 2026-10-10 (Phase 7)
- **Status**: **Approved**
- **Context**: Client hardware budgets dictate strict payload limits ($\le 1.5\text{MB}$ total bundle, $\le 3.5\text{s}$ TTI on 3G, `DEC-09`, `ADR-03`). Utility frameworks like Tailwind CSS introduce runtime or pre-processing overhead and violate repository architectural decisions (`ADR-03`).
- **Alternatives Considered**:
  - *Option A*: Tailwind CSS v3/v4 utility classes (violates ADR-03; utility bloat).
  - *Option B*: CSS-in-JS (e.g., Styled Components; excessive runtime JS and bundle bloat).
  - *Option C (Selected)*: **Vanilla CSS Custom Properties Architecture in `index.css`**. Central `:root` definitions for design tokens (colors, typography, spacing, elevations, transitions) consuming $\le 50\text{KB}$ uncompressed.
- **Rationale**: Zero external styling dependencies, instantaneous CSS parsing, zero runtime overhead, native browser theme caching, and strict adherence to established project architecture.
- **Downstream Impact**: Directly implemented in Phase 11 frontend styling; prevents dependency creep. Ref: [design-tokens.md](file:///Users/kazi/Projects/RITUCAST/docs/design/design-tokens.md), [ADR-03](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-03-react-typescript-vanilla-css.md).

---

### DEC-30: Standard 5-Section Advisory Card Layout (`CMP-CARD-01`)
- **Date**: 2026-10-10 (Phase 7)
- **Status**: **Approved**
- **Context**: Frontline farmers need immediate operational guidance without cognitive friction, while scientific safety standards demand explicit data provenance and mandatory field-verification reminders (`DEC-10`, `DEC-17`).
- **Alternatives Considered**:
  - *Option A*: Unstructured free-form notification cards.
  - *Option B*: Purely technical meteorological summaries without clear operational recommendations.
  - *Option C (Selected)*: **Strict 5-Section Card Anatomy (`CMP-CARD-01`)**:
    1. Header & Tier Badge (Upazila, Crop, Growth Stage, Tier 4 Indicator).
    2. Operational Status Pill (Actionable Directive with icon and label).
    3. Agronomic Copy & Physical Reasoning (Plain Bangla context).
    4. Economic Impact & One-Click WhatsApp Share (Diesel/cost savings, peer distribution).
    5. Scientific Provenance & Mandatory Field-Check Notice (`"সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"`).
- **Rationale**: Eliminates guesswork, standardizes user cognitive parsing across all modules, and structurally embeds scientific safeguards into every rendered advisory.
- **Downstream Impact**: Informs Phase 7 component specs, Phase 11 React card templates, and Phase 14 comprehension testing. Ref: [component-system.md](file:///Users/kazi/Projects/RITUCAST/docs/design/component-system.md), [scientific-transparency-patterns.md](file:///Users/kazi/Projects/RITUCAST/docs/design/scientific-transparency-patterns.md).

---

### DEC-31: Accessible Dual-Layer Visualization Standards
- **Date**: 2026-10-10 (Phase 7)
- **Status**: **Approved**
- **Context**: Rural extension workers using screen readers or low-end rendering engines cannot interpret standalone SVG/Canvas graphs; graphic-only charts violate WCAG 2.2 Success Criterion 1.1.1 (Non-text Content).
- **Alternatives Considered**:
  - *Option A*: Graphical SVG/Canvas charts only with generic `alt` text.
  - *Option B*: Text tables only without visual trends.
  - *Option C (Selected)*: **Dual-Layer Visualization Standard**. Every visual chart (48h rainfall probability bars, temperature trend lines, soil water balance dials, flood risk gauges) is paired with a semantically complete, visually hidden (`sr-only`) HTML `<table>` or structured `<dl>` list containing exact numerical values, dates, and units.
- **Rationale**: Delivers high-clarity visual cues for sighted users in the field while guaranteeing 100% programmatic accessibility and automated screen-reader parsing.
- **Downstream Impact**: Directs Phase 7 visualization guidelines, Phase 11 accessible chart components, and Phase 12 interactive graphics. Ref: [data-visualization-guidelines.md](file:///Users/kazi/Projects/RITUCAST/docs/design/data-visualization-guidelines.md), [accessibility-standards.md](file:///Users/kazi/Projects/RITUCAST/docs/design/accessibility-standards.md).

---

## 9. Phase 8 Data Ingestion & Processing Pipeline Decisions

---

### DEC-32: Direct Parquet Feature Serialization over Intermediate Relational Dumping
- **Date**: 2026-10-10 (Phase 8)
- **Status**: **Approved**
- **Context**: Passing large numerical weather time series through multi-table relational SQL writes during batch ETL introduces high I/O latency, connection pooling bottlenecks, and schema migration fragility before scientific features are even validated.
- **Alternatives Considered**:
  - *Option A*: Direct write into PostGIS relational tables (`weather_daily`, `hydrology_readings`) during raw ETL.
  - *Option B*: Flat CSV file dumping.
  - *Option C (Selected)*: **Direct Columnar Parquet Serialization (`pyarrow` engine, `snappy` compression)**. Processed feature tables are serialized directly into immutable Parquet files in `data/processed/`, which are subsequently ingested or queried by downstream analytics and database seeders.
- **Rationale**: Reduces disk footprint by $80\%$, achieves $10\times$ faster scan speeds for Phase 9 vectorized mathematical modeling, preserves strong data types, and guarantees portable offline testing.
- **Downstream Impact**: Governs Phase 8 storage conventions and Phase 9 input loading. Ref: [storage-and-file-conventions.md](file:///Users/kazi/Projects/RITUCAST/docs/data/storage-and-file-conventions.md), [feature-preparation-specification.md](file:///Users/kazi/Projects/RITUCAST/docs/data/feature-preparation-specification.md).

---

### DEC-33: Centroid Extraction for Coarse Grids without False Micro-Interpolation
- **Date**: 2026-10-10 (Phase 8)
- **Status**: **Approved**
- **Context**: NASA POWER ($0.5^\circ$, ~50km), Open-Meteo ($0.25^\circ$, ~28km), and SMAP (9km) have spatial resolutions larger than individual Upazilas or agricultural parcels. Falsely upscaling these grids via bilinear interpolation gives farmers an illusion of plot-specific micro-precision (`RSK-03`).
- **Alternatives Considered**:
  - *Option A*: High-resolution bilinear/kriging interpolation to 100m grid.
  - *Option B*: Nearest-neighbor boundary rasterization.
  - *Option C (Selected)*: **Point Sampling at Administrative Centroids with Explicit Spatial Resolution Metadata**. Records sample the grid value at the verified Upazila centroid and attach a mandatory `spatial_resolution_km` tag.
- **Rationale**: Upholds scientific integrity (`NFR-SCI-01`), avoids fabricated sub-acre precision, and remains transparent about observational limits.
- **Downstream Impact**: Governs Phase 8 spatial processing and Phase 9/10 API metadata responses. Ref: [spatial-processing-specification.md](file:///Users/kazi/Projects/RITUCAST/docs/data/spatial-processing-specification.md).

---

### DEC-34: Deterministic Rolling Climatology Windows
- **Date**: 2026-10-10 (Phase 8)
- **Status**: **Approved**
- **Context**: Haor flash-flood early warnings and Barind soil water balance rely on multi-day cumulative precipitation ($P_{\text{cum}}$). Ad-hoc calculations in web handlers risk inconsistent window definitions and data leakage.
- **Alternatives Considered**:
  - *Option A*: Dynamic SQL `SUM() OVER (PARTITION BY upazila ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)` on each API request.
  - *Option B*: Pre-computing rolling windows inside Phase 9 analytics engine.
  - *Option C (Selected)*: **Pipeline-Level Pre-Computation of Rolling Windows (24h, 48h, 7d)**. Computed during temporal processing and stored directly in the Parquet feature tables (`catchment_rainfall_daily.parquet`).
- **Rationale**: Eliminates runtime calculation overhead, prevents future data leakage during hindcasting, and standardizes hazard triggers across all modules.
- **Downstream Impact**: Directly feeds Phase 9 `IDX-FLD-01` and `RULE-IRR-01`. Ref: [temporal-processing-specification.md](file:///Users/kazi/Projects/RITUCAST/docs/data/temporal-processing-specification.md).

---

### DEC-35: Immutable Cryptographic Run Manifests with SHA-256 Hashes
- **Date**: 2026-10-10 (Phase 8)
- **Status**: **Approved**
- **Context**: Agricultural intelligence platforms require verifiable scientific provenance. If an advisory is audited following an unexpected crop damage event, engineers must know the exact input data, Git commit, and validation outcomes that generated the advice.
- **Alternatives Considered**:
  - *Option A*: Transient console logging only.
  - *Option B*: Database log table with no file-level cryptographic hashes.
  - *Option C (Selected)*: **Permanent JSON Run Manifests (`data/processed/manifests/<run_id>.json`) with SHA-256 Checksums**. Captures execution UUID, Git commit, parameter inputs, dataset records counts, and bit-level file hashes.
- **Rationale**: Provides tamper-evident data provenance, guarantees bit-level reproducibility, and establishes institutional accountability.
- **Downstream Impact**: Governs Phase 8 provenance ledger and Phase 10 API attribution headers. Ref: [provenance-and-versioning.md](file:///Users/kazi/Projects/RITUCAST/docs/data/provenance-and-versioning.md).

---

## 10. Phase 9 Agricultural Analytics & Recommendation Decisions

---

### DEC-36: Physical Deterministic Modeling over Supervised Machine Learning in MCP
- **Date**: 2026-10-10 (Phase 9)
- **Status**: **Approved**
- **Context**: Deciding whether to train black-box supervised machine learning models (e.g. gradient boosted trees predicting yields or soil moisture) versus deterministic physical models (FAO-56 Penman-Monteith, USDA-SCS water balance).
- **Alternatives Considered**:
  - *Option A*: Train supervised XGBoost model on coarse historical BBS Upazila yields and satellite NDVI.
  - *Option B (Selected)*: **Strict Disqualification of Supervised ML in Favor of Calibrated Physical Thermodynamics**. Ground all advisories in validated physical conservation laws (FAO-56 $ET_0$, root-zone depletion $D_t$, BWDB hydraulic danger proximity).
- **Rationale**: BBS yield data lacks micro-plot variance and parcel ground truth (`DEC-06`). Fitting black-box ML models to coarse remote sensing generates spurious correlations and hallucinations under climate extremes, destroying farmer trust.
- **Downstream Impact**: Formally locks Phase 9 analytical architecture; directs Phase 10 API design to serve physical parameters and auditable rules. Ref: [method-selection-and-rationale.md](file:///Users/kazi/Projects/RITUCAST/docs/analytics/method-selection-and-rationale.md).

---

### DEC-37: Piecewise Linear $K_c$ Knot Interpolation for Continuous Crop Water Demand
- **Date**: 2026-10-10 (Phase 9)
- **Status**: **Approved**
- **Context**: Boro rice transpiration changes continuously as the canopy develops. Discrete step-wise jumps between stages cause unnatural spikes in daily crop water demand ($ET_c$).
- **Alternatives Considered**:
  - *Option A*: Discrete step-function assigning constant $K_c$ per stage.
  - *Option B (Selected)*: **Piecewise Linear Interpolation across 5 Phenological Knots**. Day 1 (1.10), Day 40 (1.15), Day 75 (1.30), Day 100 (1.30), Day 145 (0.65).
- **Rationale**: Smooths daily water consumption curves, prevents artificial irrigation trigger jitter, and accurately captures canopy closure dynamics.
- **Downstream Impact**: Governs `CropWaterDemandCalculator` in `analytics/indicators/crop_water_demand.py`. Ref: [environmental-indicators.md](file:///Users/kazi/Projects/RITUCAST/docs/analytics/environmental-indicators.md).

---

### DEC-38: USDA Soil Conservation Service Method for Root-Zone Infiltration Invariance
- **Date**: 2026-10-10 (Phase 9)
- **Status**: **Approved**
- **Context**: Raw precipitation cannot be added directly to root-zone moisture; light rains evaporate immediately from crop canopies, while extreme cloudbursts run off bunded paddy spillways.
- **Alternatives Considered**:
  - *Option A*: Assume 100% of rain infiltrates into soil ($P_{\text{eff}} = P$).
  - *Option B (Selected)*: **Calibrated USDA-SCS Effective Precipitation Curve**. Rain $\le 3.0\text{mm}$ provides $0\text{mm}$ infiltration; moderate rains follow $(P \times (125 - 0.2P))/125$; extreme storms cap infiltration at spillway crest.
- **Rationale**: Prevents underestimation of soil moisture deficit following drizzle, and prevents overestimation following torrential storms.
- **Downstream Impact**: Standardizes water balance calculation in `SoilWaterDeficitCalculator`. Ref: [soil_water_deficit.py](file:///Users/kazi/Projects/RITUCAST/analytics/indicators/soil_water_deficit.py).

---

### DEC-39: Normalized Multi-Factor Transboundary Haor Flood Index Weighting
- **Date**: 2026-10-10 (Phase 9)
- **Status**: **Approved**
- **Context**: Haor flash floods are non-linear transboundary events driven by Meghalaya rainfall, Surma river baseflow, and rapid surge rates. Relying on a single proxy creates catastrophic false negatives or false alarms.
- **Alternatives Considered**:
  - *Option A*: Rely solely on local river gauge danger level ($H \ge DL$).
  - *Option B*: Rely solely on upstream Meghalaya rainfall forecasts.
  - *Option C (Selected)*: **Coupled 4-Factor Weighted Composite Index ($I_{\text{flood}} \in [0, 1]$)**. Weights: Catchment Rain ($w_1=0.35$), River Danger Proximity ($w_2=0.30$), River Rate of Rise ($w_3=0.20$), and Inundation Fraction ($w_4=0.15$).
- **Rationale**: Catchment rain provides 48h advance warning; river rate of rise confirms incoming flood wave surge; proximity to danger level gauges levee freeboard.
- **Downstream Impact**: Governs `HaorFloodIndexCalculator` and triggers `RULE-FLD-01`. Ref: [haor_flood_index.py](file:///Users/kazi/Projects/RITUCAST/analytics/indicators/haor_flood_index.py).

---

## 11. Phase 10 Backend API & Service Layer Decisions

---

### DEC-40: Adoption of FastAPI and Pydantic v2 for Asynchronous Service Layer
- **Date**: 2026-10-10 (Phase 10)
- **Status**: **Approved**
- **Context**: Choosing the API delivery framework to expose Phase 9 analytics to mobile PWAs and extension workers.
- **Alternatives Considered**:
  - *Option A*: Flask or Django REST Framework.
  - *Option B*: Express.js/Node.js requiring inter-process communication with Python analytics.
  - *Option C (Selected)*: **FastAPI + Pydantic v2**.
- **Rationale**: Direct in-process execution of Phase 9 Python calculators without IPC overhead; native asynchronous request handling; automatic OpenAPI 3.0 specification generation; strict schema validation.
- **Downstream Impact**: Defined structure of `api/` package and routers. Ref: [phase-10-backend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md).

---

### DEC-41: In-Memory Caching for Processed Parquet Tables and Metadata
- **Date**: 2026-10-10 (Phase 10)
- **Status**: **Approved**
- **Context**: Deciding how the API loads Parquet feature tables without inducing repeated disk I/O on every HTTP request.
- **Alternatives Considered**:
  - *Option A*: Query Parquet files from disk on every incoming request.
  - *Option B*: Introduce Redis or PostgreSQL infrastructure prematurely.
  - *Option C (Selected)*: **In-Memory Caching in `AgriculturalDataRepository`**.
- **Rationale**: Processed tables for pilot Upazilas occupy under 3MB total heap memory; in-memory caching keeps query latency below 20ms and avoids external infrastructure dependencies for MVP.
- **Downstream Impact**: Governs `AgriculturalDataRepository` caching in `api/data_access/repository.py`. Ref: [performance-and-resource-management.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/performance-and-resource-management.md).

---

### DEC-42: Centralized Error Translation into Immutable Error Envelopes
- **Date**: 2026-10-10 (Phase 10)
- **Status**: **Approved**
- **Context**: Ensuring consistent, secure client error reporting without leaking raw stack traces, file paths, or framework internals.
- **Alternatives Considered**:
  - *Option A*: Default FastAPI/Starlette error format.
  - *Option B (Selected)*: **Centralized Error Translation Middleware (`api/middleware/error_handlers.py`)**.
- **Rationale**: Guarantees all errors (400, 404, 422, 500) return uniform JSON with `status: "error"`, machine-readable `code`, human-readable `message`, and ISO `timestamp_utc`.
- **Downstream Impact**: Enforced across all routers and verified in test suite. Ref: [request-validation-and-errors.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/request-validation-and-errors.md).

---

### DEC-43: Upazila Administrative Code Canonicalization and Shorthand Alias Support
- **Date**: 2026-10-10 (Phase 10)
- **Status**: **Approved**
- **Context**: Field extensions and previous phases used both shorthand codes (e.g. `BD-50-28`, `BD-60-90`) and official 8-digit BBS codes (e.g. `BD-50-20-30`, `BD-60-90-89`).
- **Alternatives Considered**:
  - *Option A*: Reject all shorthand codes with HTTP 404.
  - *Option B (Selected)*: **Transparent Upazila Identifier Canonicalization in Data Access Layer**.
- **Rationale**: Preserves backwards compatibility for extension mobile clients while maintaining strict internal canonical IDs matching official BBS geospatial boundaries.
- **Downstream Impact**: Implemented in `AgriculturalDataRepository.resolve_upazila_id()`. Ref: [api-endpoints.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/api-endpoints.md).

---

## 12. Phase 11 Frontend Application & User Experience Decisions

---

### DEC-44: SPA / PWA Architecture with Vite 8 and React 19
- **Date**: 2026-10-10 (Phase 11)
- **Status**: **Approved**
- **Context**: Choosing the build system and frontend application runtime to deliver responsive, offline-ready interfaces within client budget constraints (`DEC-09`, `DEC-20`).
- **Alternatives Considered**:
  - *Option A*: Next.js / Remix SSR framework.
  - *Option B*: Create React App / Webpack.
  - *Option C (Selected)*: **Vite 8 + React 19 SPA**.
- **Rationale**: Generates ultra-compact static assets (<300kB JS uncompressed, 85kB gzipped); eliminates Node.js server-side runtime costs; provides sub-second HMR for local development; enables zero-latency edge caching.
- **Downstream Impact**: Implemented in `frontend/` directory with `vite.config.ts`. Ref: [phase-11-frontend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/frontend/phase-11-frontend-architecture.md).

---

### DEC-45: Pure Vanilla CSS Custom Properties Over Utility Frameworks
- **Date**: 2026-10-10 (Phase 11)
- **Status**: **Approved**
- **Context**: Deciding on the styling mechanism to implement the visual design system defined in Phase 7 (`DEC-20`).
- **Alternatives Considered**:
  - *Option A*: Tailwind CSS v3 or v4.
  - *Option B*: CSS-in-JS (Styled Components / Emotion).
  - *Option C (Selected)*: **Vanilla CSS Custom Properties in `frontend/src/index.css`**.
- **Rationale**: Zero runtime JavaScript overhead; complete control over outdoor sunlight high-contrast color tokens; eliminates external CSS build dependencies; production CSS bundle is only 13.5 kB (3.1 kB gzipped).
- **Downstream Impact**: Defined in `frontend/src/index.css`. Ref: [design-system.md](file:///Users/kazi/Projects/RITUCAST/docs/frontend/design-system.md).

---

### DEC-46: Client-Side Contextual Gating State Synchronization
- **Date**: 2026-10-10 (Phase 11)
- **Status**: **Approved**
- **Context**: Translating backend `DEC-17` contextual gating into an intuitive, mistake-proof user interaction flow.
- **Alternatives Considered**:
  - *Option A*: Multi-step wizard requiring page reloads between location, crop, and stage.
  - *Option B (Selected)*: **Sticky Context Selection Bar (`ContextSelector.tsx`) Synchronized with Root Application State**.
  - *Option C*: Allowing free-form queries and displaying backend 400 errors after failed queries.
- **Rationale**: Immediate visibility of selected Upazila, Crop, and Growth Stage; automatically populates valid phenological stages per crop; prevents invalid or ungated requests from ever reaching the network layer.
- **Downstream Impact**: Implemented in `frontend/src/components/ContextSelector.tsx`. Ref: [information-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/frontend/information-architecture.md).

---

### DEC-47: Automated Safety Banner and SAAO Fallback Routing on Advisory Suppression
- **Date**: 2026-10-10 (Phase 11)
- **Status**: **Approved**
- **Context**: Ensuring the UI strictly enforces the `DEC-10` automated suppression policy without confusing farmers or leaving them without guidance.
- **Alternatives Considered**:
  - *Option A*: Completely hide the advisory card or display a blank screen.
  - *Option B*: Render normal advice with a small footnote.
  - *Option C (Selected)*: **Prominent Amber Fallback Banner Display with SAAO Contact Protocols**.
- **Rationale**: Replaces actionable pump/harvest directives with clear, plain-language explanation of why advice was suppressed (e.g. NWP ensemble spread $\ge 50\%$ or telemetry $>36\text{h}$ old) and immediately directs the farmer to contact their local Sub-Assistant Agriculture Officer (SAAO).
- **Downstream Impact**: Implemented in `frontend/src/components/AdvisoryHubView.tsx`. Ref: [backend-integration.md](file:///Users/kazi/Projects/RITUCAST/docs/frontend/backend-integration.md).

---

## 8. Phase 12 End-to-End Integration & System Validation Decisions

---

### DEC-48: End-to-End System Integration Testing Topology and Test Fixture Isolation
- **Date**: 2026-10-10 (Phase 12)
- **Status**: **Approved**
- **Context**: Ensuring reliable, reproducible validation across all 5 architectural tiers (Ingestion, Processing, Models, REST API, React PWA) without relying on heavy external satellite downloads during automated testing.
- **Alternatives Considered**:
  - *Option A*: Only test each subsystem in unit isolation with mock data.
  - *Option B*: Require live 1GB+ satellite downloads from Copernicus and NASA on every test run.
  - *Option C (Selected)*: **Three-Tier Testing Topology**: Deterministic System E2E (`test_system_e2e.py`), Separate Bounded Live Smoke Tests (`test_live_smoke.py`), and Frontend User Journey E2E (`e2e_user_journey.test.tsx`).
- **Rationale**: Guarantees sub-10 second automated regression test execution; clearly isolates deterministic test fixtures (`data/sample/`) from live external services; provides graceful skipping for live smoke tests in offline environments.
- **Downstream Impact**: Implemented in `tests/integration/` and `frontend/src/test/e2e_user_journey.test.tsx`. Ref: [phase-12-validation-strategy.md](file:///Users/kazi/Projects/RITUCAST/docs/testing/phase-12-validation-strategy.md).

---

### DEC-49: Coercion of File Paths to Pathlib Objects Across Data Repositories
- **Date**: 2026-10-10 (Phase 12)
- **Status**: **Approved**
- **Context**: Resolving defect `DEF-12-01` where string directory paths passed into `AgriculturalDataRepository` raised `TypeError: unsupported operand type(s) for /: 'str' and 'str'`.
- **Alternatives Considered**:
  - *Option A*: Use `os.path.join` everywhere.
  - *Option B (Selected)*: **Explicit `Path()` Coercion in Repository Constructor**.
  - *Option C*: Enforce strict `pathlib.Path` type hints without runtime coercion.
- **Rationale**: Coercing strings to `Path` objects in `AgriculturalDataRepository.__init__` accepts both `str` and `Path` arguments without runtime friction, ensuring seamless interoperability across CLI scripts, test fixtures, and FastAPI route handlers.
- **Downstream Impact**: Implemented in `api/data_access/repository.py`. Ref: [repository.py](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py).

---

### DEC-50: Strict Safeguarding of Optional Recommendation Confidence in UI Rendering
- **Date**: 2026-10-10 (Phase 12)
- **Status**: **Approved**
- **Context**: Resolving defect `DEF-12-02` where `AdvisoryHubView.tsx` crashed when rendering recommendations lacking a `confidence` sub-object.
- **Alternatives Considered**:
  - *Option A*: Make confidence metadata mandatory on all backend responses.
  - *Option B (Selected)*: **Safeguard Confidence Badge Rendering with `{rec.confidence && ...}` and Defensive Defaults**.
  - *Option C*: Hide the recommendation card when confidence is missing.
- **Rationale**: Protects client application stability; handles partial or legacy advisory payloads gracefully; preserves the primary Tier 4 actionable recommendation card even if confidence scores are being calibrated.
- **Downstream Impact**: Implemented in `frontend/src/components/AdvisoryHubView.tsx`. Ref: [AdvisoryHubView.tsx](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/AdvisoryHubView.tsx).

---

### DEC-51: Containerized Decoupled Serverless Deployment with Google Cloud Run
- **Date**: 2026-10-10 (Phase 13)
- **Status**: **Approved**
- **Context**: Selecting a production hosting architecture that satisfies rural Bangladesh network characteristics (low latency to `asia-south1`), supports morning/evening peak traffic patterns, and stays strictly within the $\le \$65/\text{month}$ budget ceiling (`DEC-09`, `ADR-07`).
- **Alternatives Considered**:
  - *Option A*: Traditional Linux VPS (Hetzner / DigitalOcean).
  - *Option B*: AWS ECS Fargate + S3 / CloudFront.
  - *Option C*: Kubernetes cluster (GKE / EKS).
  - *Option D (Selected)*: **Decoupled OCI Containers on Google Cloud Run (`asia-south1`, Mumbai)**.
- **Rationale**: Cloud Run scales to zero instances when idle, incurring zero compute cost outside active requests. Generous free tier (2M requests, 360k vCPU-s) covers entire pilot workload at $0.00 to $5.00/month. Mumbai region ensures $<55\text{ms}$ latency to Bangladesh 3G networks. Standard OCI Knative specifications eliminate proprietary vendor lock-in.
- **Downstream Impact**: Informs `Dockerfile.backend`, `Dockerfile.frontend`, `deploy/cloudrun/service-backend.yaml`, `service-frontend.yaml`, and `deploy.sh`. Ref: [phase-13-deployment-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/deployment/phase-13-deployment-architecture.md).

---

### DEC-52: Immutable In-Image Parquet Storage Over Managed External Database
- **Date**: 2026-10-10 (Phase 13)
- **Status**: **Approved**
- **Context**: Selecting the data storage tier for operational pilot feature tables and administrative boundaries.
- **Alternatives Considered**:
  - *Option A*: Managed Cloud SQL PostgreSQL / PostGIS ($30–$60/month base cost).
  - *Option B*: Remote Cloud Storage (GCS) buckets read on every request.
  - *Option C (Selected)*: **Immutable In-Image Parquet Storage Packaged in Container (`/app/data/`)**.
- **Rationale**: Total pilot data footprint is $<110\text{KB}$. Storing Parquet feature tables directly inside the container image eliminates database subscription costs, eliminates database connection-pool exhaustion, provides sub-millisecond in-memory Arrow/Pandas queries, and ensures 100% deterministic reproducibility across local and cloud environments.
- **Downstream Impact**: Informs `Dockerfile.backend`, `.dockerignore`, and readiness probe dependencies. Ref: [data-and-model-artifacts.md](file:///Users/kazi/Projects/RITUCAST/docs/deployment/data-and-model-artifacts.md).

---

### DEC-53: NGINX Multi-Stage Frontend Container with Gzip, Dual-Port, and Strict Security Headers
- **Date**: 2026-10-10 (Phase 13)
- **Status**: **Approved**
- **Context**: Delivering the production React 19 / TypeScript SPA to rural smallholders on budget Android smartphones and variable cellular networks under the $1.5\text{MB}$ payload ceiling (`DEC-09`).
- **Alternatives Considered**:
  - *Option A*: Static CDN bucket without custom reverse-proxy capabilities.
  - *Option B*: Node.js runtime SSR server.
  - *Option C (Selected)*: **Multi-Stage Node Builder + NGINX Alpine Runtime with Dual-Port (80/8080) Listening, Gzip, and Security Headers**.
- **Rationale**: Gzip level 6 compresses the production bundle to $220.65\text{kB}$ ($<15\%$ of budget). NGINX alpine runtime consumes $<6\text{MB}$ memory. Dual-port listening enables out-of-the-box operation across local testing (port 80/3000) and Cloud Run (port 8080). Injects strict CSP, HSTS, X-Frame-Options, and X-Content-Type-Options headers.
- **Downstream Impact**: Informs `deploy/docker/Dockerfile.frontend` and `deploy/docker/nginx.conf`. Ref: [containerization.md](file:///Users/kazi/Projects/RITUCAST/docs/deployment/containerization.md).










