# Phase 5 to Phase 6 Handoff Specification

## 1. Executive Summary & Purpose

- **From**: Phase 05 — System Architecture and Technology Decisions
- **To**: Phase 06 — Information Architecture and User Journey Design
- **Date**: 2026-10-10
- **Status**: **READY FOR PHASE 06 INITIATION**

This document establishes the binding architectural constraints, data contracts, and design implications established in Phase 5 that must guide the Information Architecture (IA) and User Journey design in Phase 6.

---

## 2. Key Architectural Constraints Governing Phase 6

### 2.1 Four-Tier Information Taxonomy (`DEC-08`)
The UI information architecture designed in Phase 6 must visually distinguish and categorize all information into four distinct levels:
1. **Tier 1: Observations (পর্যবেক্ষণ)**: Direct empirical sensor values (e.g., recorded rainfall, current temperature, SAR flood extent).
2. **Tier 2: Derived Indicators (হিসাবকৃত সূচক)**: Modeled physical values (e.g., FAO-56 Penman-Monteith $ET_0$, daily soil water deficit $D_t$, Haor flash-flood hazard index $I_{\text{flood}}$).
3. **Tier 3: Probabilistic Forecasts (পূর্বাভাস)**: Predictions with explicit confidence intervals and probabilities (e.g., 48-hour rainfall probability, multi-model ensemble spread).
4. **Tier 4: Actionable Recommendations (পরামর্শ)**: Actionable agronomic guidance (e.g., delay irrigation by 24 hours, accelerate Boro harvest) accompanied by plain-language agronomic explanations and mandatory field-verification reminders.

### 2.2 Mandatory Contextual Gating (`DEC-17`)
The information architecture and user flow must enforce that **no Tier 4 advisory card is ever rendered** without confirmed context:
- Upazila selection (e.g., Godagari, Tanore, Sunamganj Sadar, Tahirpur).
- Active Crop selection (Boro Rice).
- Active Phenological Growth Stage (e.g., Nursery, Vegetative, Panicle Initiation, Flowering, Grain Filling, Maturity).

If any contextual parameter is missing, the UI must route the user through a progressive onboarding/selection flow or default to regional baseline indicators only.

### 2.3 Automated Suppression & Safe Fallback States (`DEC-10`, `ADR-08`)
Phase 6 must design explicit user states and UI components for automated advisory suppression:
- When upstream weather or satellite data is $>36\text{ hours}$ old.
- When NWP multi-model ensemble spread exceeds $50\%$ with rain probability between $40\%$ and $60\%$.
- When physical sensor readings fail range checks.

The screen design must present a clear, non-alarming fallback banner advising manual field inspection:
> *"বর্তমান আবহাওয়া পূর্বাভাসের অনিশ্চয়তা বেশি থাকায় স্বয়ংক্রিয় সেচ পরামর্শ সাময়িকভাবে স্থগিত রাখা হয়েছে। সেচ দেওয়ার পূর্বে জমির মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*

### 2.4 Low-Spec Mobile & Low-Bandwidth Performance Budget (`DEC-09`)
- Rural target users operate budget Android devices (2GB–3GB RAM, Android 8+) on variable 3G networks.
- Initial client payload is capped at $\le 1.5\text{MB}$; Time-to-Interactive (TTI) must remain $\le 3.5\text{s}$; peak client heap memory must not exceed $\le 45\text{MB}$.
- **Journey Implication**: The primary entry journey ("Quick Action Advisory") must be card- and text-based. Interactive vector map views (MapLibre GL JS) must be deferred to an optional "Diagnostic / Spatial Analysis" sub-tab or modal to prevent map rendering from blocking the primary critical path.

### 2.5 Dual-Zone Pilot Journey Differentiation
Phase 6 user journeys must accommodate two distinct agro-ecological workflows:
1. **High Barind Tract (Rajshahi: Godagari, Tanore)**:
   - Primary user intent: Groundwater conservation, diesel pump expenditure reduction, irrigation scheduling.
   - Core metrics: Soil water deficit ($D_t$), 48-hour rain likelihood, irrigation trigger status (Apply Sech / Postpone Sech).
2. **Haor Basin (Sylhet: Sunamganj Sadar, Tahirpur)**:
   - Primary user intent: Pre-monsoon flash flood survival, early crop harvesting decisions.
   - Core metrics: Meghalaya upstream catchment rainfall ($P_{\text{cat}}$), Surma river gauge rate of rise ($\Delta H / \Delta t$), Sentinel-1 flood extent, harvest readiness percentage.

---

## 3. Data Contracts and Screen Mapping

| API Endpoint | Expected Frontend UI View | Key Visual Elements |
| :--- | :--- | :--- |
| `GET /api/v1/upazilas` | Region Selection / Onboarding | Dropdown / search modal for 4 pilot Upazilas; sets session context. |
| `GET /api/v1/weather/observations` | Tier 1 Empirical Weather Card | Current temp, solar radiation, BMD 24h rainfall bar chart. |
| `GET /api/v1/water-balance/barind` | Tier 2 Barind Soil Moisture Card | Daily $ET_0$, depletion gauge ($D_t$ vs $RAW$), root depth. |
| `GET /api/v1/flood-hazard/haor` | Tier 2 Haor Flood Alert Card | Upstream rain sum, river stage meter, inundation hazard level. |
| `GET /api/v1/advisories/recommendations` | Tier 4 Actionable Advisory Card | Recommended action badge, plain Bangla justification, verification notice. |

---

## 4. Phase 6 Deliverables Checklist for the Incoming Team

The Phase 6 engineering and design team should produce:
- [ ] `docs/ux/information-architecture.md`: Site map, navigation structure, and screen hierarchy.
- [ ] `docs/ux/user-journeys.md`: Farmer and Sub-Assistant Agriculture Officer (SAAO) step-by-step task flows for Barind and Haor testbeds.
- [ ] `docs/ux/low-fidelity-wireframes.md`: Text-based / structured wireframe specifications for mobile-first screens.
- [ ] `docs/ux/state-matrix.md`: UI specifications for Loading, Stale Data, Suppressed Advisory, Offline, and Error states.
- [ ] `docs/phases/phase-06/handoff-to-phase-07.md`: Handoff package for visual design and design system.

---

## 5. Verification Sign-Off

- **Phase 5 Lead**: Approved (System Architecture & Technology Decisions Complete)
- **Phase 6 Readiness**: **GREEN (Unblocked)**
