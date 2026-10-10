# Ritucast: User Personas, Jobs-to-Be-Done & Critical Journeys

## 1. Product Personas (Dual-Anchor Model)

---

### Primary Persona 1: Tariqul Islam — Frontline Extension Officer (DAE SAAO)
- **Role & Location**: Sub-Assistant Agriculture Officer (SAAO), Godagari Upazila, Rajshahi Division.
- **Demographics**: 38 years old; Diploma in Agriculture; government employee.
- **Responsibilities**: Advises 1,200 smallholder farming households across 4 villages (*Union Block*); holds weekly courtyard meetings (*Uthan Boithok*); reports crop damage and acreage to Upazila Agriculture Officer (UAO).
- **Device & Connectivity**: Walton Primo Android smartphone (3GB RAM, 720p display); intermittent 3G/4G connectivity in village fields; high cellular data cost sensitivity.
- **Language & Literacy**: Fluent in administrative and agronomic Bangla; comfortable with agricultural terms (e.g., *আমন*, *বোরো*, *ইউরিয়া উপরিপ্রয়োগ*); minimal patience for dense scientific English.
- **Core Pain Points**:
  - Receives generic district-level weather PDF bulletins once or twice a week, which lack field-level irrigation guidance.
  - Farmers constantly ask whether they should start deep tubewell pumping or wait for incoming rain; Tariqul lacks real-time soil moisture balance indicators to answer confidently.
- **Goals with Ritucast**:
  - Quickly check upazila-level moisture balances and 72-hour precipitation risks before morning farmer meetings.
  - Present visual, credible evidence to farmers to demonstrate why pumping can be safely postponed.

---

### Primary Persona 2: Rafiqul Alam — Progressive Lead Farmer & Tubewell Manager
- **Role & Location**: Lead Farmer and BMDA Deep Tubewell Operator, Tanore Upazila, Rajshahi Division.
- **Demographics**: 44 years old; cultivates 5.5 acres (Boro rice in winter, T. Aman in monsoon, Mustard/Potato in rabi); manages water allocation for 25 neighboring plots.
- **Device & Connectivity**: Xiaomi Redmi budget smartphone (3GB RAM); uses YouTube and IMO regularly; variable 4G at homestead, weak signal in low fields.
- **Language & Literacy**: Bangla speaker; limited English; prefers large typography, visual status icons, and audio-assisted explanations over dense text.
- **Core Pain Points**:
  - Electricity and diesel for tubewell pumping cost up to 2,500 BDT per acre per irrigation run; running pumps right before an unpredicted heavy downpour results in wasted money and waterlogged fields.
  - Weather apps on his phone show generic rain icons that fail to materialize, destroying his trust in digital forecasts.
- **Goals with Ritucast**:
  - Check whether expected rain within the next 48 hours is heavy enough to cancel tomorrow’s scheduled tubewell pumping.
  - Protect his investment by identifying critical moisture stress before his rice crop reaches panicle emergence.

---

### Secondary Persona: Shahidul Karim — Haor Cooperative Harvester Lead
- **Role & Location**: Lead Farmer & Combine Harvester Contractor, Tahirpur Upazila, Sunamganj (Haor Basin).
- **Demographics**: 49 years old; coordinates harvesting logistics for a local farmer group.
- **Core Pain Points**:
  - Upstream flash floods from Meghalaya hills can submerge low-lying haors in less than 48 hours.
  - If he harvests too early, grains are immature; if he waits too long, the entire standing crop is submerged and lost.
- **Goals with Ritucast**:
  - Receive early radar and upstream rainfall accumulation alerts 3–5 days ahead of flood crests to mobilize combine harvesters before road links flood.

---

## 2. Jobs-to-Be-Done (JTBD) Framework

| Job ID | Situation / Trigger | Job to Be Done (Core Task) | Desired Outcome | Existing Limitation | Ritucast Solution | Success Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **JTBD-01** | Boro rice is in active vegetative/flowering stage during dry February–March. | Determine whether to run tubewell pumping today or postpone. | Avoid spending 2,000 BDT/acre on pumping without subjecting rice to moisture stress. | Farmers rely on surface soil visual cracks or fixed 5-day pumping schedules regardless of rain. | Calculates 72h $P_{\text{eff}} - ET_c$ water balance using NASA POWER and SMAP; outputs clear Bangla postponement advisory. | Pumping postponed prior to rain event $\ge 15\text{mm}$; zero moisture-stress symptoms in crop. |
| **JTBD-02** | Boro rice reaches 80% grain maturity in early April across low-lying Haor basins. | Decide whether to commence emergency early harvesting before flash flood arrives. | Harvest standing crop before floodwaters submerge the haor bowl, preventing total crop write-off. | River water level gauges measure main rivers, failing to warn of overland flash flood arrival until water enters fields. | Sentinel-1 SAR waterlogging change detection combined with upstream Meghalaya GPM rainfall tracking. | Harvester mobilized 48h prior to inundation; crop harvested at $\ge 80\%$ maturity. |
| **JTBD-03** | Farmer plans fertilizer top-dressing (Urea) or pesticide spraying during Aman or Boro season. | Identify a 24- to 48-hour dry weather window free of heavy rain and high winds. | Ensure expensive agrochemical inputs are not washed away by immediate rain or drifted by high winds. | Generic forecasts give 24h probability but don't specify rainfall intensity or wind speed thresholds. | Agronomic "Safe Spraying & Fertilizer Window" indicator evaluating rainfall rate ($<2\text{mm/h}$) and wind ($<15\text{km/h}$). | Inputs applied during valid window; no fertilizer wash-off recorded. |
| **JTBD-04** | SAAO prepares for weekly farmer courtyard meetings (*Uthan Boithok*). | Review regional soil-moisture deficit trends and weather warnings across the Union. | Provide consistent, scientifically verified agronomic guidance to 50+ attending farmers. | SAAO must manually synthesize disparate radio bulletins and district PDFs. | One-screen Upazila Agro-Climatic Intelligence summary with printable/shareable Bangla cards. | SAAO presents Ritucast cards; meeting consensus reached in under 10 minutes. |

---

## 3. Critical User Journeys (Initial Release)

---

### User Journey 1: Location & Crop Configuration (UJ-01)
- **User Goal**: Quickly configure the relevant agricultural location (Division $\rightarrow$ District $\rightarrow$ Upazila) and active crop stage without complex registration forms.
- **Preconditions**: User opens the Ritucast mobile web application on a mobile browser.
- **Main Steps**:
  1. Application loads the home screen within 3.5 seconds; displays a prominent location selector defaulting to the last cached upazila or geographic prompt.
  2. User taps location dropdown; selects Division (e.g., *Rajshahi*), District (*Rajshahi*), and Upazila (*Godagari*).
  3. User selects active crop from a visual list (*Boro Rice*, *Potato*, *Mustard*).
  4. User selects approximate crop stage (*Transplanting*, *Vegetative / Tillering*, *Flowering / Panicle Initiation*, *Ripening / Harvest*).
  5. System validates the selection against active seasonal calendars and updates the operational dashboard.
- **Alternative / Failure Path**:
  - *No cellular connection*: System automatically loads the last cached upazila and crop configuration from IndexedDB/localStorage and displays an "অফলাইন মোড" (Offline Mode) badge.
  - *Invalid / Out-of-Season Crop*: System alerts the user: *"এই মৌসুমে এই ফসলটি সচরাচর চাষ হয় না"* (This crop is unusual for this season) and defaults to current season mega-crops.
- **Acceptance Criteria**: Entire configuration completed in $\le 4$ taps; loads in $<2\text{s}$ on cached runs.

---

### User Journey 2: Dry-Spell Moisture Deficit & Irrigation Postponement Decision (UJ-02)
- **User Goal**: Rafiqul Alam (Lead Farmer) checks whether to run deep tubewell pumping for his Boro rice field tomorrow morning.
- **Preconditions**: Location set to Godagari; crop set to Boro Rice (Vegetative/Tillering stage); meteorological forecast predicts 20mm rainfall within 48 hours.
- **Main Steps**:
  1. Rafiqul opens Ritucast; immediately views the top **Primary Advisory Card**.
  2. The card displays a high-contrast amber/blue banner: **"পরামর্শ: আগামী ৩ দিন সেচ বন্ধ রাখুন"** (Advisory: Postpone irrigation for the next 3 days).
  3. Card highlights key summary metrics:
     - প্রত্যাশিত বৃষ্টিপাত: ১৫–২৫ মিমি (Expected rain: 15–25mm).
     - মাটির আর্দ্রতার অবস্থা: পর্যাপ্ত (Soil moisture: Adequate).
     - আনুমানিক জ্বালানি সাশ্রয়: ১,৮০০–২,২০০ টাকা/একর (Est. savings: 1,800–2,200 BDT/acre).
  4. Rafiqul confirms the advisory, shares the advisory card screenshot to his local tubewell WhatsApp group, and notifies farmers that pumping is postponed until Thursday.
- **Alternative / Failure Path**:
  - *Forecast uncertainty is high (rainfall probability between 35% and 55%)*: System changes advisory text to: *"সতর্কতা: বৃষ্টির সম্ভাবনা অনিশ্চিত। সেচ দেয়ার পূর্বে জমির আইল ও মাটির আর্দ্রতা নিজে পর্যবেক্ষণ করুন।"* (Warning: Rain uncertain. Inspect field bunds and moisture directly before pumping).
- **Acceptance Criteria**: Advisory clearly communicates action (postpone vs pump), expected rainfall quantity, and confidence tier; zero technical jargon on the primary card face.

---

### User Journey 3: Flash-Flood Inundation & Emergency Harvest Mobilization (UJ-03)
- **User Goal**: Shahidul Karim (Haor Cooperative Lead) checks flood risk in Tahirpur, Sunamganj to decide whether to mobilize combine harvesters for 80% ripe Boro rice.
- **Preconditions**: Location set to Tahirpur; crop set to Boro Rice (Ripening stage); heavy transboundary rainfall detected in upstream Meghalaya catchments.
- **Main Steps**:
  1. Shahidul opens Ritucast; is greeted by a high-priority red alert card: **"জরুরি সতর্কতা: পাহাড়ি ঢল ও আগাম বন্যার উচ্চ ঝুঁকি"** (Emergency Alert: High risk of flash floods and transboundary runoff).
  2. The card displays:
     - উজানে ভারী বৃষ্টিপাত: ৪৮ ঘণ্টায় ১২০+ মিমি (Upstream heavy rain: 120+ mm in 48h).
     - হাওরে পানি বৃদ্ধির পূর্বাভাস: পরবর্তী ২–৩ দিন (Haor water rise forecast: next 2–3 days).
     - পরামর্শ: ৮০% পরিপক্ক ধান দ্রুত কাটার প্রস্তুতি নিন (Action: Mobilize to harvest 80% mature rice immediately).
  3. Shahidul contacts local combine harvester operators and mobilizes labor gangs for dawn harvesting.
- **Alternative / Failure Path**:
  - *Radar pass data unavailable*: System clearly states: *"স্যাটেলাইট রাডার পর্যবেক্ষণ হালনাগাদ হচ্ছে; সতর্কতাটি উজানের বৃষ্টিপাত ও নদী পূর্বাভাসের ওপর ভিত্তি করে তৈরি।"* (Radar updating; alert is based on upstream rainfall and river forecasts).
- **Acceptance Criteria**: Critical alert displays with non-color-only emergency iconography; explicitly references upstream rainfall metrics.

---

### User Journey 4: Investigating Advisory Evidence & Uncertainty (UJ-04)
- **User Goal**: Tariqul Islam (SAAO) reviews the scientific reasoning behind an irrigation postponement advisory to explain it to skeptical farmers during a courtyard meeting.
- **Preconditions**: User views an active advisory card on the dashboard.
- **Main Steps**:
  1. Tariqul taps the **"কেন এই পরামর্শ? (প্রমাণ ও বিশ্লেষণ)"** (Why this advice? Evidence & Analysis) button at the bottom of the advisory card.
  2. An accessible explainability drawer slides open, presenting a structured breakdown:
     - **পর্যবেক্ষণ (Observations)**: গত ৭ দিনে মোট বৃষ্টিপাত (৫ মিমি), বর্তমান মাটির আর্দ্রতা সূচক (৬০%)।
     - **পূর্বাভাস (Forecasts)**: আগামী ৪৮ ঘণ্টার বৃষ্টিপাতের সম্ভাবনা (৭৫%, ২০–২৫ মিমি), গড় তাপমাত্রা (২৮°সে)।
     - **ফসলের পানির ভারসাম্য (Water Balance)**: বোরো ধানের বর্তমান দৈনিক পানির চাহিদা (৪.৫ মিমি/দিন)। প্রত্যাশিত বৃষ্টিপাত আগামী ৫ দিনের চাহিদা মেটাবে।
     - **নির্ভরযোগ্যতা সূচক (Confidence Level)**: উচ্চ (High - ৮৫% মডেল ঐক্যমত)।
  3. Tariqul shows this visual breakdown on his smartphone screen to the assembled farmers, explaining that irrigating now would cause fertilizer leaching and waste diesel.
- **Acceptance Criteria**: Drawer opens in $<200\text{ms}$; displays separate observation and forecast vectors; uses standardized DAE-approved Bangla agronomic terminology.

---

## 4. Traceability Links

- [Product Strategy](file:///Users/kazi/Projects/RITUCAST/docs/product/product-strategy.md)
- [Product Requirements Document](file:///Users/kazi/Projects/RITUCAST/docs/requirements/product-requirements.md)
- [Recommendation Quality & Scientific Safety](file:///Users/kazi/Projects/RITUCAST/docs/requirements/recommendation-quality-and-safety.md)
- [Requirements Traceability Matrix](file:///Users/kazi/Projects/RITUCAST/docs/requirements/requirements-traceability.md)
