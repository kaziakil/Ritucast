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



