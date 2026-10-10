# User Acceptance Test (UAT) Scenarios — Ritucast

## 1. Overview & Purpose

This document specifies the official **User Acceptance Testing (UAT) Catalog** for **Ritucast**, an agricultural intelligence and decision-support platform designed for smallholder farmers and Sub-Assistant Agriculture Officers (SAAOs) in Bangladesh.

The scenarios validate that the system correctly implements all core workflows, honors scientific safety gating, enforces accessibility standards, and behaves predictably across the two representative pilot agro-ecological zones:
1. **High Barind Tract** (Rajshahi Division: Godagari, Tanore Upazilas) — Drought monitoring, groundwater deficit, AWD irrigation scheduling.
2. **Haor Basin** (Sylhet Division: Sunamganj Sadar, Tahirpur Upazilas) — Pre-monsoon transboundary flash floods, early harvest alerts.

All tests trace directly to the 6 canonical user journeys formulated in [`docs/ux/user-journeys.md`](file:///Users/kazi/Projects/RITUCAST/docs/ux/user-journeys.md), functional requirements (`FR-LOC-01` to `FR-UX-01`), and architectural decisions (`DEC-08`, `DEC-09`, `DEC-10`, `DEC-17`).

---

## 2. Test Execution Environment & Profiles

### 2.1 User Profiles
- **Profile 1: Lead Farmer (চাষী ভাই)**: Low-to-moderate digital literacy; operates a budget Android device (2GB RAM, Android 8.1, 720p screen) outdoors under direct sunlight; primarily relies on Bengali terminology and visual hazard color cues.
- **Profile 2: Sub-Assistant Agriculture Officer (SAAO - উপ-সহকারী কৃষি কর্মকর্তা)**: Moderate-to-high digital literacy; provides advisory extension services across 3–5 villages; inspects scientific rationale breakdowns, empirical sensor inputs, and soil-water deficit calculations to explain advice to farmers.

### 2.2 Environmental Constraints
- **Network**: Simulated 3G mobile data (750 kbps download, 250 kbps upload, 150ms round-trip latency).
- **Display**: High-glare outdoor viewing conditions requiring WCAG 2.1 AA daylight contrast ($\ge 4.5:1$).
- **Interaction**: One-handed capacitive touchscreen touch targets ($\ge 48\times 48\text{px}$) per `DEC-09`.

---

## 3. UAT Test Scenarios Catalog

### UAT-SCN-01: Journey A — Daily Morning Advisory Check (High Barind AWD Scheduling)
- **Journey Reference**: [`docs/ux/user-journeys.md`](file:///Users/kazi/Projects/RITUCAST/docs/ux/user-journeys.md#user-journey-a-morning-advisory-check-godagari-boro-farmer)
- **Target Persona**: Lead Farmer in Godagari, Rajshahi (`BD-50-20-30`).
- **Crop & Stage**: Boro Rice (*Oryza sativa L.*), Tillering stage (কুশি পর্যায়).
- **Pre-Conditions**:
  - System backend operational and reporting healthy status (`/api/v1/health` and `/api/v1/readiness`).
  - Active season is Boro (November–May).
  - Weather observations and ECMWF/GFS forecasts updated within 24 hours.
- **Action Steps**:
  1. User accesses application URL on mobile browser.
  2. Confirms default Upazila is set to **গোদাগাড়ী (Godagari)** and Crop to **বোরো ধান (Boro Rice)**.
  3. Observes the 4-tier advisory card on the Advisory Hub view.
  4. Reads Tier 1 observations (7-day rainfall, mean temperature).
  5. Reads Tier 2 indicators (Soil water deficit $D_t = 24.0\text{ mm}$, FAO-56 $ET_0 = 3.8\text{ mm/day}$).
  6. Reads Tier 3 predictions (48h rain probability 65%, QPF 16.5 mm).
  7. Reads Tier 4 operational advisory: **আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন** (Postpone Irrigation).
  8. Inspects mandatory ground verification copy: *"সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*
- **Expected Results**:
  - All 4 information tiers are visibly distinct with appropriate Bengali badge headers (`পর্যবেক্ষণ`, `হিসাবকৃত সূচক`, `পূর্বাভাস`, `কার্যকর পরামর্শ`) per `DEC-08`.
  - Pumping cost savings estimate is displayed (e.g., ৫৫০–৭৫০ টাকা/বিঘা).
  - High confidence badge is visible with green indicator (`#15803D`).
- **Status**: **PASS** (Automated in `uat_accessibility.test.tsx` test 1).

---

### UAT-SCN-02: Journey B — Contextual Switch to Haor Flash Flood Zone
- **Journey Reference**: [`docs/ux/user-journeys.md`](file:///Users/kazi/Projects/RITUCAST/docs/ux/user-journeys.md#user-journey-b-context-switching-to-haor-basin)
- **Target Persona**: SAAO inspecting flood-prone testbed in Tahirpur, Sunamganj (`BD-60-90-89`).
- **Action Steps**:
  1. From the top Context Selector banner, open the Upazila dropdown.
  2. Select **তাহিরপুর (Tahirpur)**.
  3. Observe dynamic updates to the Context Selector metadata banner.
  4. Verify the active agro-ecological zone indicator switches from **High Barind Tract (AEZ-26)** to **Sylhet Basin / Haor (AEZ-21)**.
  5. Verify primary risk indicator updates to **আকস্মিক বন্যা (Flash Flood)**.
- **Expected Results**:
  - Upazila change triggers immediate background queries for Tahirpur data.
  - Contextual banner dynamically displays `Sylhet Basin / Haor` and `আকস্মিক বন্যা`.
  - Dropdown options maintain full touch target sizing ($\ge 48\text{px}$).
- **Status**: **PASS** (Automated in `uat_accessibility.test.tsx` test 2).

---

### UAT-SCN-03: Journey C — Pre-Monsoon Emergency Harvest Decision (Tahirpur)
- **Journey Reference**: [`docs/ux/user-journeys.md`](file:///Users/kazi/Projects/RITUCAST/docs/ux/user-journeys.md#user-journey-c-pre-monsoon-flash-flood-early-harvest-alert)
- **Target Persona**: SAAO / Boro Farmer in Tahirpur during mid-April pre-monsoon surge.
- **Crop & Stage**: Boro Rice, Dough / Maturity stage (দুধ/পাকা পর্যায়).
- **Simulated Trigger**:
  - Meghalaya catchment 48h rainfall $P_{48h} = 145\text{ mm}$ (critical threshold $>100\text{ mm}$).
  - Surma River water level $H = 8.10\text{ m}$ (danger level $8.0\text{ m}$).
  - Sentinel-1 SAR inundation rate $>30\%$.
  - Calculated Haor Flash Flood Index $I_{\text{flood}} = 0.82 \ge 0.70$ (EMERGENCY tier).
- **Action Steps**:
  1. User selects Tahirpur and navigates to the **হাওর বন্যা ঝুঁকি (Flood Hazard)** view.
  2. Inspects composite index gauge and sub-index values ($f_P, f_S, f_I$).
  3. Observes the emergency advisory card with red hazard styling (`#B91C1C`).
  4. Reads the early harvest action directive: **জরুরি ধান কর্তন শুরু করুন (৮০% পাকা ধান)**.
  5. Inspects safety action items (mobilize harvest labor, clear drainage khals, secure threshing yards).
- **Expected Results**:
  - Emergency alert prominently displayed without ambiguity.
  - Plain-language Bengali instructions clearly state that 80% matured grain should be harvested immediately to avoid total crop loss.
  - No overconfident guarantees of flood arrival timing (*"১০০% নিশ্চিত"* prohibited).
- **Status**: **PASS** (Automated in `uat_accessibility.test.tsx` test 3).

---

### UAT-SCN-04: Journey D — SAAO Scientific Rationale & Water Balance Inspection
- **Journey Reference**: [`docs/ux/user-journeys.md`](file:///Users/kazi/Projects/RITUCAST/docs/ux/user-journeys.md#user-journey-d-saao-deep-dive-soil-water-balance-inspection)
- **Target Persona**: SAAO explaining irrigation deferral to an inquiring farmer in Godagari.
- **Action Steps**:
  1. User navigates to the **পানি ভারসাম্য (Water Balance)** tab.
  2. Inspects the root-zone soil water balance card.
  3. Reads calibrated crop coefficient ($K_c = 1.10$), reference evapotranspiration ($ET_0 = 3.8\text{ mm/day}$), and crop evapotranspiration ($ET_c = 4.18\text{ mm/day}$).
  4. Reviews soil physical constants for Barind Paleosol clay loam:
     - Total Available Water ($\text{TAW} = 85.0\text{ mm}$).
     - Readily Available Water ($\text{RAW} = 42.5\text{ mm}$).
     - Current Soil Water Deficit ($D_t = 24.0\text{ mm}$).
  5. Confirms status reads **AWD শুকানো অনুমোদিত - সেচ অপ্রয়োজনীয়** ($D_t < \text{RAW}$).
  6. Navigates to **উপাত্তের উৎস (Provenance)** tab and verifies mathematical equations cited (`EQN-ET0-01`, `EQN-SWD-01`).
- **Expected Results**:
  - Numerical indicators match physics calculations exactly.
  - Transparent data lineage shows NASA POWER, BMD station, and FAO-56 methodology.
  - SAAO has authoritative, explainable evidence to reassure the farmer.
- **Status**: **PASS** (Automated in `uat_accessibility.test.tsx` test 4).

---

### UAT-SCN-05: Journey E — Automated Suppression Safe Fallback (`DEC-10`)
- **Journey Reference**: [`docs/ux/user-journeys.md`](file:///Users/kazi/Projects/RITUCAST/docs/ux/user-journeys.md#user-journey-e-automated-suppression-fallback)
- **Target Persona**: SAAO & Farmer under multi-model divergence.
- **Simulated Trigger**:
  - ECMWF IFS and NOAA GFS ensemble divergence exceeds 50% spread with rain probability between 40% and 60% (unresolvable forecast volatility).
- **Action Steps**:
  1. User accesses Advisory Hub when backend suppresses advisory output.
  2. Inspects recommendation card.
- **Expected Results**:
  - The operational recommendation is replaced with a clear yellow/amber suppression banner (`#B45309`).
  - Headline reads: **পরামর্শ সাময়িকভাবে স্থগিত** (Advisory Temporarily Suspended).
  - Clear explanation copy informs the farmer that atmospheric forecast models disagree significantly, and instructs them to inspect field soil moisture directly before turning on pumps.
  - No misleading or potentially crop-damaging advice is output.
- **Status**: **PASS** (Automated in `uat_accessibility.test.tsx` test 5).

---

### UAT-SCN-06: Journey F — Network Disruption & Offline Error Recovery
- **Journey Reference**: [`docs/ux/user-journeys.md`](file:///Users/kazi/Projects/RITUCAST/docs/ux/user-journeys.md#user-journey-f-offline-and-degraded-connectivity-handling)
- **Target Persona**: Farmer accessing Ritucast during rural 3G cellular outage.
- **Simulated Trigger**: Network fetch failure (`TypeError: Failed to fetch`).
- **Action Steps**:
  1. Advisory Hub initiates network request which fails.
  2. Inspects UI state.
  3. User clicks the **পুনরায় চেষ্টা করুন (Retry)** button after signal returns.
- **Expected Results**:
  - Loading spinner terminates promptly (no infinite hanging state).
  - User-friendly Bengali error banner displayed with `role="alert"`: *"উপাত্ত লোড করতে সমস্যা হয়েছে"*.
  - Retry button is clearly visible, keyboard-focusable, and has $\ge 48\text{px}$ touch target.
  - Triggering retry initiates a fresh data query.
- **Status**: **PASS** (Automated in `uat_accessibility.test.tsx` test 6).

---

## 4. Acceptance Criteria Compliance Summary

| Test ID | Journey | Primary Acceptance Criteria | Automated Test Reference | Result |
| :--- | :--- | :--- | :--- | :--- |
| **UAT-SCN-01** | Journey A | 4-Tier taxonomy, AWD advice, disclaimer copy | `uat_accessibility.test.tsx:288` | **PASS** |
| **UAT-SCN-02** | Journey B | Godagari $\to$ Tahirpur context switch & banner | `uat_accessibility.test.tsx:308` | **PASS** |
| **UAT-SCN-03** | Journey C | Haor flash flood emergency card ($I_{\text{flood}} \ge 0.70$) | `uat_accessibility.test.tsx:327` | **PASS** |
| **UAT-SCN-04** | Journey D | FAO-56 $ET_0$, $D_t$, TAW/RAW soil water balance | `uat_accessibility.test.tsx:343` | **PASS** |
| **UAT-SCN-05** | Journey E | Automated suppression on NWP volatility (`DEC-10`) | `uat_accessibility.test.tsx:389` | **PASS** |
| **UAT-SCN-06** | Journey F | Network error alert banner and retry mechanics | `uat_accessibility.test.tsx:405` | **PASS** |
