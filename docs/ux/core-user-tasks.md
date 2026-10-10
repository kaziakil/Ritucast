# Ritucast Core User Tasks Specification

## 1. Executive Summary & Task Taxonomy

This specification translates the functional requirements from [Phase 2: PRD](file:///Users/kazi/Projects/RITUCAST/docs/requirements/product-requirements.md) and the agronomic rules from [Phase 4](file:///Users/kazi/Projects/RITUCAST/docs/science/agricultural-rule-specifications.md) into concrete, user-executable tasks.

Tasks are prioritized into:
- **Must-Have (Initial Release / MCP)**: Essential for daily decision-making in the dual-zone testbeds.
- **Should-Have (Phase 11–14 Enhancement)**: High-value usability features to be added before final release.
- **Future (Phases 17–18)**: Advanced analytical capabilities deferred to subsequent expansion phases.

---

## 2. Master Core Tasks Inventory

| Task ID | Task Name | Primary User | Release Priority | Traceable PRD Requirement |
| :--- | :--- | :--- | :--- | :--- |
| **`TSK-01`** | Select and Confirm Geographic Location | All | **Must-Have** | `FR-LOC-01`, `FR-LOC-02` |
| **`TSK-02`** | Confirm Active Crop and Growth Stage | SAAO, Lead Farmer | **Must-Have** | `FR-LOC-03`, `DEC-17` |
| **`TSK-03`** | View Upazila Weather & 48h Rain Forecast | All | **Must-Have** | `FR-ENV-01`, `FR-ENV-02` |
| **`TSK-04`** | Check Barind Soil Water Deficit & Irrigation Advice | Barind Farmer, SAAO | **Must-Have** | `FR-ADV-02`, `RULE-IRR-01` |
| **`TSK-05`** | Monitor Haor Flash-Flood Risk & Harvest Advisory | Haor Farmer, SAAO | **Must-Have** | `FR-ADV-04`, `RULE-FLD-01` |
| **`TSK-06`** | Inspect Advisory Reasoning & Data Freshness | SAAO, Lead Farmer | **Must-Have** | `FR-ADV-03`, `DEC-08`, `DEC-10` |
| **`TSK-07`** | Share Advisory Card via WhatsApp / Social Media | SAAO, Lead Farmer | **Must-Have** | `FR-DSH-04`, `DEC-09` |
| **`TSK-08`** | View Interactive Geospatial Map (Diagnostic) | SAAO, UAO | **Should-Have** | `FR-DSH-03`, `ADR-06` |
| **`TSK-09`** | Access Offline Cached Advisory | All (in field) | **Must-Have** | `NFR-REL-02`, `ASM-02` |
| **`TSK-10`** | Compare Historical Weekly Weather Trends | SAAO, Researcher | **Future** | `FR-ENV-05` (Deferred) |

---

## 3. Detailed Must-Have Task Specifications

### TSK-01: Select and Confirm Geographic Location
- **User Intent**: Establish the geographic context so all weather, soil, and flood data reflect the user's specific area.
- **Required Inputs**: Administrative Division, District, and Upazila (e.g., Rajshahi $\to$ Godagari; Sylhet $\to$ Tahirpur).
- **Preconditions**: User has opened the app.
- **Expected Result**: App sets active Upazila in local storage; displays active location banner at top of viewport; loads Upazila-specific agro-climatic data.
- **Data Dependencies**: `GET /api/v1/upazilas` (`DATA-BND-01`).
- **Failure & Empty States**:
  - Unsupported Upazila: Friendly notice explaining Ritucast is currently piloting in Barind and Haor; provides option to explore pilot testbeds.
  - Offline with no cache: Message prompting user to reconnect to select location.
- **Success Criteria**: User establishes location in $\le 2$ taps within 5 seconds.

---

### TSK-02: Confirm Active Crop and Growth Stage (Context Gating)
- **User Intent**: Provide the crop context needed to generate scientifically accurate irrigation or harvest advice (`DEC-17`).
- **Required Inputs**: Crop type (Default: Boro Rice) and current growth stage (Nursery, Vegetative/Tillering, Panicle Initiation, Flowering, Grain Filling, Maturity).
- **Preconditions**: Location confirmed (`TSK-01`).
- **Expected Result**: Unlocks Tier 4 recommendation cards; tailors crop coefficient ($K_c$) and root depth ($Z_r$) to the active stage.
- **Data Dependencies**: Crop phenology configuration (`DATA-AGR-01`).
- **Failure & Empty States**:
  - User skips stage selection: Tier 4 card is gated with a prompt: *"সঠিক পরামর্শ পেতে অনুগ্রহ করে ফসলের বর্তমান বৃদ্ধির ধাপ নির্বাচন করুন।"* Tier 1/2 environmental data remains visible.
- **Success Criteria**: 100% of generated recommendations have verified Upazila, Crop, and Stage context.

---

### TSK-03: View Upazila Weather & 48h Rain Forecast
- **User Intent**: Check current weather and upcoming rain to plan daily farm activities.
- **Required Inputs**: Active Upazila.
- **Expected Result**: Displays Tier 1 temperature, humidity, and solar radiation, alongside Tier 3 48-hour rainfall probability (%), expected amount (mm), and ensemble confidence band.
- **Data Dependencies**: `GET /api/v1/weather/observations`, `GET /api/v1/weather/forecasts` (`DATA-MET-01`, `DATA-FCST-01`).
- **Failure & Empty States**:
  - Stale forecast data (>36h): Amber badge *"পূর্বাভাস কিছুটা পুরনো (আপডেট প্রক্রিয়াধীন)"*; confidence score degraded.
- **Success Criteria**: User understands whether rain is expected within 3 seconds.

---

### TSK-04: Check Barind Soil Water Deficit & Irrigation Advice
- **User Intent**: Decide whether to turn on the irrigation pump today or postpone pumping to save fuel and groundwater.
- **Required Inputs**: Confirmed Barind Upazila (Godagari/Tanore), Crop (Boro Rice), and Stage.
- **Expected Result**:
  - Clear operational banner: **"আজ সেচ দেওয়ার প্রয়োজন নেই"** (Postpone) or **"আজ সেচ দিন"** (Apply).
  - Visual soil water deficit gauge showing root-zone moisture level vs critical depletion threshold ($RAW$).
  - Estimated diesel/electricity cost savings.
- **Data Dependencies**: `GET /api/v1/water-balance/barind`, `GET /api/v1/advisories/recommendations` (`RULE-IRR-01`).
- **Failure & Empty States**:
  - Multi-model ensemble divergence >50%: Automated suppression triggered; advisory replaced with safe fallback: *"পূর্বাভাসে অনিশ্চয়তা বেশি থাকায় স্বয়ংক্রিয় সেচ পরামর্শ সাময়িকভাবে স্থগিত। জমিতে গিয়ে মাটির রস পরীক্ষা করুন।"*
- **Success Criteria**: Farmer makes an informed, confident irrigation decision without needing mathematical calculations.

---

### TSK-05: Monitor Haor Flash-Flood Risk & Harvest Advisory
- **User Intent**: Assess early-season flash-flood threat to low-lying Boro paddy and determine if emergency harvest is required.
- **Required Inputs**: Confirmed Haor Upazila (Sunamganj Sadar/Tahirpur), Crop (Boro Rice), and Stage.
- **Expected Result**:
  - 3-Tier Hazard Status: **স্বাভাবিক (Normal)** / **সতর্কতা (Watch)** / **জরুরি সতর্কবার্তা (Emergency Alert)**.
  - Upstream Meghalaya 48h rainfall sum ($P_{\text{cat}}$) and nearby Surma river gauge rate of rise ($\Delta H/\Delta t$).
  - Recommended harvest action (e.g., *"ধান ৮০% পাকলে দ্রুত কেটে ফেলুন"*).
- **Data Dependencies**: `GET /api/v1/flood-hazard/haor`, `GET /api/v1/advisories/recommendations` (`RULE-FLD-01`, `DEC-16`).
- **Failure & Empty States**:
  - BWDB river gauge data missing: System computes flood index using GPM satellite rainfall and flags degraded confidence (*"নদীর পানির উচ্চতা তথ্য অনুপলব্ধ; স্যাটেলাইট তথ্যের ভিত্তিতে সতর্কবার্তা"*).
- **Success Criteria**: Farmer understands the hazard level and appropriate harvest response with zero ambiguity.

---

### TSK-06: Inspect Advisory Reasoning & Data Freshness
- **User Intent**: Understand *why* the system recommends an action and verify that the underlying satellite/weather data is trustworthy and current.
- **Required Inputs**: Tap on "কেন এই পরামর্শ?" (Why this advice?) or "তথ্যসূত্র ও সময়" (Sources & Time).
- **Expected Result**: Expandable drawer showing:
  - Contributing factors (e.g., "আগামী ৪৮ ঘণ্টায় ২৫ মিমি বৃষ্টির সম্ভাবনা ৭০%", "মাটিতে পর্যাপ্ত রস বিদ্যমান").
  - Data sources and observation timestamps (e.g., BMD, NASA POWER, Sentinel-1).
  - Mandatory field-verification notice.
- **Data Dependencies**: Advisory metadata payload (`DEC-08`, `DEC-10`).
- **Success Criteria**: SAAO can explain the scientific rationale to farmers during field visits.

---

### TSK-07: Share Advisory Card via WhatsApp / Social Media
- **User Intent**: Disseminate today's agricultural advisory to farmer groups, family, or neighboring villages.
- **Required Inputs**: Tap "পরামর্শ শেয়ার করুন" (Share Advisory).
- **Expected Result**:
  - Invokes native Web Share API with pre-formatted Bangla advisory text and link.
  - Fallback on legacy devices: Copies summary text to clipboard or generates lightweight image card for WhatsApp.
- **Data Dependencies**: Client-side share handler (`FR-DSH-04`).
- **Success Criteria**: SAAO broadcasts advisory to 50+ farmers in under 10 seconds.

---

### TSK-09: Access Offline Cached Advisory
- **User Intent**: Review the latest advisory while standing in remote fields without cellular reception.
- **Required Inputs**: Open app while offline.
- **Expected Result**: App loads instantly via Service Worker; displays an "অফলাইন মোড" (Offline Mode) banner; shows the last synchronized advisory with explicit timestamp (e.g., *"আজ সকাল ৮:০০ টায় সংরক্ষিত"*).
- **Data Dependencies**: Client Cache Storage / IndexedDB (`NFR-REL-02`).
- **Success Criteria**: Complete advisory viewable with zero network latency.
