# Ritucast User Groups, Needs, and Constraints

## 1. Executive Summary & Audience Framework

This specification defines the user groups for the Ritucast platform based on the approved findings from [Phase 1: Target Users](file:///Users/kazi/Projects/RITUCAST/docs/project/target-users.md) and [Phase 2: Personas & Journeys](file:///Users/kazi/Projects/RITUCAST/docs/product/user-needs-and-journeys.md).

To prevent scope creep while maximizing ground-level agricultural impact, Ritucast adopts a **Dual-Anchor Audience Model**:
1. **Primary Anchor A**: Department of Agricultural Extension (DAE) **Sub-Assistant Agriculture Officers (SAAOs)**.
2. **Primary Anchor B**: Village-level **Progressive Lead Farmers**.

---

## 2. User Group Prioritization Matrix

```
                        ┌──────────────────────────────────────────────┐
                        │              PRIMARY AUDIENCE                │
                        │  1. SAAOs (DAE Field Extension Officers)     │
                        │  2. Lead Farmers (Barind & Haor Testbeds)    │
                        └──────────────────────┬───────────────────────┘
                                               │
                        ┌──────────────────────▼───────────────────────┐
                        │             SECONDARY AUDIENCE               │
                        │  3. Upazila Agriculture Officers (UAOs)      │
                        │  4. Local Deep Tubewell (DTW) Pump Managers  │
                        └──────────────────────┬───────────────────────┘
                                               │
                        ┌──────────────────────▼───────────────────────┐
                        │               FUTURE AUDIENCE                │
                        │  5. General Smallholders (via SAAO/IVR)       │
                        │  6. Agricultural Researchers & Agronomists   │
                        └──────────────────────────────────────────────┘
```

---

## 3. Detailed Profile: Primary User Groups

### 3.1 Primary User 1: Sub-Assistant Agriculture Officer (SAAO)
- **Archetype / Persona**: Tariqul Islam, 38, SAAO, DAE Godagari, Rajshahi (`PRS-01`).
- **Role & Responsibilities**: Advises 800–1,200 smallholder farming households across an agricultural "Block" (approx. 2–3 villages). Conducts daily field visits, leads courtyard training meetings (*Uthan Boithok*), and compiles weekly crop progress reports for the Upazila Agriculture Office.
- **Goals**:
  - Deliver timely, accurate, science-backed irrigation and disaster advice to his farmers.
  - Save time compiling weather and crop water demand data for weekly DAE reports.
  - Prevent crop losses and boost his reputation and credibility within the farming community.
- **Key Decisions**:
  - When to advise farmers in the Block to halt tubewell pumping ahead of expected rainfall.
  - When to sound an urgent early-harvest alarm for low-lying Haor Boro rice.
  - How to resolve conflicting weather forecasts reported by farmers.
- **Required Information**:
  - 48-hour to 7-day quantitative rainfall probability and multi-model consensus.
  - Upazila-level root-zone soil water deficit ($D_t$) and evapotranspiration ($ET_0$).
  - Transboundary Meghalaya catchment rainfall and Surma river gauge surge rates (for Haor SAAOs).
  - Clear, pre-formatted Bangla advisory summaries that can be shared via WhatsApp groups or printed.
- **Common Questions**:
  - *"আগামী ৪৮ ঘণ্টায় কি বৃষ্টি হওয়ার সম্ভাবনা নিশ্চিত? কৃষকদের কি আজ সেচ বন্ধ রাখতে বলব?"*
  - *"উজানে মেঘালয়ে কতটুকু বৃষ্টি হয়েছে? তাহিরপুরের হাওরে পানি নামতে কত সময় লাগবে?"*
- **Digital Literacy**: Moderate to High. Daily user of Android smartphones, WhatsApp, Facebook, and governmental portals (BAMIS). Familiar with basic digital charts, but lacks remote sensing expertise.
- **Device & Connectivity Constraints**: Mid-range Android smartphone (3GB–4GB RAM), variable 3G/4G coverage; frequently operates in remote field blocks with weak or intermittent connectivity.
- **Likely Adoption Barriers**: Administrative fatigue from multiple government apps; fear of giving incorrect advice that could ruin a farmer's crop.
- **Trust & Comprehension Requirements**: Needs clear explanation of why an advisory was generated; transparent data sources (e.g., BMD, NASA) to cite to farmers.

---

### 3.2 Primary User 2: Progressive Lead Farmer (High Barind Tract)
- **Archetype / Persona**: Md. Mokhlesur Rahman, 46, Lead Farmer, Tanore, Rajshahi (`PRS-02`).
- **Role & Responsibilities**: Cultivates 6.5 bighas of Boro rice and winter vegetables. Rents irrigation water from deep tubewell (DTW) pumps at high hourly diesel/electricity rates (400–600 BDT/hour). Serves as an informal opinion leader for 15–20 neighboring smallholders.
- **Goals**:
  - Reduce diesel and electricity expenses by eliminating unneeded irrigation cycles.
  - Protect high-yield Boro rice from drought stress during sensitive reproductive stages (panicle initiation and flowering).
  - Maximize yield and net profit per bigha.
- **Key Decisions**:
  - Whether to turn on the irrigation pump today or wait 2 days for forecasted rain.
  - Whether soil moisture is adequate under Alternate Wetting and Drying (AWD).
- **Required Information**:
  - Clear binary operational guidance: "সেচ দিন" (Apply Irrigation) vs "সেচ স্থগিত রাখুন" (Postpone Irrigation).
  - 48-hour rain likelihood and estimated rainfall amount.
  - Current soil moisture condition translated into simple visual scales (পর্যাপ্ত / মধ্যম / ঘাটতি).
- **Common Questions**:
  - *"আজ সেচ দিলে কি কাল বৃষ্টি হয়ে সেচের টাকা পানিতে যাবে?"*
  - *"জমির মাটিতে যে রস আছে, তাতে কি আর ২ দিন সেচ ছাড়া চলা যাবে?"*
- **Digital Literacy**: Low to Moderate. Uses Android smartphone primarily for YouTube, IMO/WhatsApp voice calls, and Facebook. Prefers large touch targets, bold typography, voice audio snippets, and minimal text entry.
- **Device & Connectivity Constraints**: Budget Android phone (2GB RAM, Android 8/9, cracked screen, low battery life), intermittent 3G connection.
- **Likely Adoption Barriers**: Deep-seated risk aversion; habitual calendar-based irrigation; fear that postponing irrigation will cause permanent yield loss.
- **Trust & Comprehension Requirements**: Simple visual confirmation that rain is on the way; mandatory reassurance that he should check the field bund (*Ail*) soil with his own hands before turning off the pump.

---

### 3.3 Primary User 3: Vulnerable Wetland Farmer (Haor Basin)
- **Archetype / Persona**: Joynal Abedin, 52, Boro Rice Farmer, Tahirpur, Sunamganj (`PRS-03`).
- **Role & Responsibilities**: Farms 4 bighas of monoculture Boro rice in low-lying Haor wetland basins. Operates under extreme seasonal vulnerability: a single pre-monsoon flash flood in April can submerge the entire year's harvest within 24 hours.
- **Goals**:
  - Receive 48–72 hours of advance warning before transboundary flash floods breach the embankment (*Dharir Bandh*).
  - Safely harvest 80%–85% mature Boro crop before floodwaters arrive.
- **Key Decisions**:
  - Whether to mobilize emergency labor and combine harvesters immediately to cut semi-mature paddy (80% ripe).
  - Whether to invest in reinforcing local earthen embankments.
- **Required Information**:
  - Simple 3-tier Flood Hazard Meter: স্বাভাবিক (Normal) / সতর্কবার্তা (Watch) / জরুরি সতর্কতা (Emergency Alert).
  - Rate of river rise in nearby river (Surma/Jadukata) and upstream Cherrapunji/Meghalaya rainfall.
  - Recommended harvest action based on crop maturity stage.
- **Common Questions**:
  - *"মেঘালয়ে কি ভারী বৃষ্টি হচ্ছে? আমাদের হাওরে পানি কবে ঢুকবে?"*
  - *"৮০% পাকা ধান কি এখনই কেটে ফেলব, নাকি আর দুই দিন অপেক্ষা করব?"*
- **Digital Literacy**: Low. Relies heavily on visual alerts, color codes, community announcements, and word-of-mouth.
- **Device & Connectivity Constraints**: Budget Android smartphone (2GB RAM) shared with family members; poor connectivity in remote Haor villages.
- **Likely Adoption Barriers**: Panic selling of immature grain due to false alarms; fatalistic distrust of government early warnings.
- **Trust & Comprehension Requirements**: Transparent explanation of flood indices; high sensitivity without excessive false alarms.

---

## 4. Secondary and Future User Groups

### 4.1 Secondary User 1: Upazila Agriculture Officer (UAO)
- **Role**: Supervises 15–25 SAAOs across an entire Upazila.
- **Needs in Ritucast**: Upazila-wide aggregated dashboard showing which Unions are facing severe water deficits or flood threats; tool to broadcast standardized advisories.
- **Phase 6 Scope**: View-only access to Upazila-level summary screens; full multi-block administrative analytics deferred to Phase 16/18.

### 4.2 Secondary User 2: Deep Tubewell (DTW) Pump Manager / BMDA Operator
- **Role**: Operates communal deep tubewells in Barind, selling water to 20–50 farmers.
- **Needs in Ritucast**: Block-level weekly irrigation demand forecast to plan pump maintenance, fuel purchases, and scheduling.
- **Phase 6 Scope**: Covered through Lead Farmer / SAAO views; specialized pump scheduling views deferred.

### 4.3 Future Users (Explicitly Deferred)
- **General Smallholders with Feature Phones**: Served via SAAO intermediation and community meetings in initial release; direct SMS/IVR deferred to Phase 17/18.
- **Agricultural Researchers**: Raw NetCDF raster downloads and statistical correlation tools deferred to Phase 18.
- **Agrochemical Dealers**: Commercial input sales integration explicitly excluded (`DEC-06`).

---

## 5. User Needs vs Requirements Traceability

| User Group | Core Need | Addressed by PRD Requirement | Addressed by UX Architecture |
| :--- | :--- | :--- | :--- |
| **SAAO** | Quick Upazila weather & forecast check | `FR-ENV-01`, `FR-ENV-02` | Overview Screen: Tier 1 & Tier 3 Weather Cards |
| **SAAO** | Shareable Bangla advisory card | `FR-ADV-01`, `FR-DSH-04` | One-click WhatsApp text and image card export |
| **Barind Farmer** | Binary irrigation decision | `FR-ADV-02`, `RULE-IRR-01` | Actionable Irrigation Card (সেচ দিন / স্থগিত রাখুন) |
| **Barind Farmer** | Verify field soil moisture status | `FR-ENV-03`, `FR-ADV-03` | Soil Water Deficit Gauge ($D_t$ vs $RAW$) |
| **Haor Farmer** | Flash-flood advance warning | `FR-ENV-04`, `RULE-FLD-01` | Haor Inundation Alert Card & Meghalaya Rain Meter |
| **Haor Farmer** | Emergency harvest advice | `FR-ADV-04`, `RULE-FLD-01` | Harvest Readiness & Stage-Gated Advisory |
