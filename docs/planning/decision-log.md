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
