# Recommendation Engine Specification — Ritucast

## 1. Executive Summary & Purpose

The **Ritucast Recommendation Engine** translates derived environmental indicators into actionable, explainable operational guidance for smallholders and Sub-Assistant Agriculture Officers (SAAOs).

In strict alignment with the Recommendation Safety Framework ([recommendation-safety-framework.md](file:///Users/kazi/Projects/RITUCAST/docs/science/recommendation-safety-framework.md)), recommendations are **deterministic, context-gated, and suppression-aware**. Speculative chemical pesticide prescriptions and uncalibrated parcel yield promises are strictly prohibited (`DEC-06`).

---

## 2. Recommendation Safety Rules & Guardrails

1. **Mandatory Contextual Gating (`DEC-17`)**:
   - Zero generic advisory cards. Every recommendation requires verified confirmation of: (1) Administrative Upazila, (2) Active Crop (Boro rice), and (3) Active Phenological Stage.
2. **Prohibited Recommendation Classes (`DEC-06`)**:
   - **NO Chemical Pesticide / Fungicide Prescriptions (`MOD-DIS-01`)**: Satellite spectral bands cannot identify specific pathogens (e.g. bacterial leaf blight vs. brown plant hopper damage). Ritucast never issues chemical spraying commands.
   - **NO Fertilizer Dosage Prescriptions from NDVI**: Satellite NDVI measures canopy greenness, which is confounded by waterlogging, transplanting density, and harvest senescence.
   - **NO Direct Tubewell Actuation**: Farmers maintain 100% human-in-the-loop operational control over irrigation pumps.
3. **Automated Suppression Standard (`DEC-10`)**:
   - When data is $>36\text{h}$ old or ensemble spread exceeds $50\%$ with ambiguous rain probability ($40–60\%$), advisories automatically transition to `SUPPRESSED` status with an SAAO consultation fallback notice.

---

## 3. Master Recommendation Rule Specifications

### 3.1 RULE-IRR-01: Pre-Rain Irrigation Postponement Advisory
- **Rule ID**: `RULE-IRR-01`
- **Product Mapping**: `FR-ADV-01`, `FR-ADV-03`
- **Target Geography**: High Barind Tract (Godagari `BD-50-20-30`, Tanore `BD-50-20-90`).
- **Target Crop & Stage**: Boro rice (*Oryza sativa L.*), Vegetative (Tillering) or Early Panicle Initiation.
- **Trigger Conditions**:
  1. 48h Quantitative Precipitation Forecast ($QPF_{48\text{h}}$) $\ge 20.0\text{ mm}$.
  2. 48h Precipitation Probability ($P_{\text{prob}}$) $\ge 65\%$.
  3. Root-zone soil water depletion $D_t < (TAW - 25.0\text{ mm})$ ($D_t < 31.0\text{ mm}$).
  4. Multi-model ensemble spread $\le 35\%$.
- **Headline (Bangla)**: **"সেচ স্থগিত রাখুন (পরামর্শ)"**
- **Plain-Language Explanation (Bangla)**:
  > *"আগামী ৪৮ থেকে ৭২ ঘণ্টার মধ্যে আপনার এলাকায় উল্লেখযোগ্য বৃষ্টির সম্ভাবনা রয়েছে (সম্ভাবনা ৬৫–৮০%, আনুমানিক ২০–৩৫ মিমি)। নলকূপ চালু করার আগে অপেক্ষা করুন। বৃষ্টি হলে সেচের জ্বালানি খরচ সাশ্রয় হবে।"*
- **Action Items (Bangla)**:
  1. পরবর্তী ৪৮ ঘণ্টা গভীর বা অগভীর নলকূপ চালু করা স্থগিত রাখুন।
  2. জমির আইল ভালোভাবে মেরামত করুন যাতে বৃষ্টির পানি জমিতে ধরে রাখা যায়।
  3. যদি বৃষ্টি ২০ মিলিমিটারের কম হয়, তবে মাটির আর্দ্রতা পরীক্ষা করে সেচ দিন।
- **Mandatory Field Notice**: *"সেচ বন্ধ রাখার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন। যদি জমি ইতিমধ্যে ফেটে গিয়ে থাকে, তবে হালকা পানি দিন।"*

### 3.2 RULE-IRR-02: Critical Root-Zone Moisture Deficit Alert
- **Rule ID**: `RULE-IRR-02`
- **Product Mapping**: `FR-ADV-01`, `FR-ENV-03`
- **Target Geography**: High Barind Tract (Godagari, Tanore).
- **Target Crop & Stage**: Boro rice, Vegetative (Tillering).
- **Trigger Conditions**:
  1. Root-zone soil water depletion $D_t \ge RAW$ ($D_t \ge 19.6\text{ mm}$).
  2. 5-day forecasted precipitation sum $\sum P_{5\text{d}} < 5.0\text{ mm}$.
  3. Recent 24h rainfall $< 15.0\text{ mm}$.
- **Headline (Bangla)**: **"সেচ প্রদান করুন (পরামর্শ)"**
- **Plain-Language Explanation (Bangla)**:
  > *"মাটির আর্দ্রতা সংকটজনক মাত্রায় নেমে গেছে এবং আগামী ৫ দিনে বৃষ্টির সম্ভাবনা নেই। ফসলের স্বাভাবিক বৃদ্ধি বজায় রাখতে জমিতে সেচ প্রদান করুন।"*
- **Action Items (Bangla)**:
  1. অনতিবিলম্বে জমিতে ৫–৭ সেন্টিমিটার উচ্চতায় সেচ প্রদান করুন।
  2. পরবর্তী সেচের আগে পর্যায়ক্রমিক ভিজানো ও শুকানো (AWD) পদ্ধতি মেনে চলুন।
- **Mandatory Field Notice**: *"সেচ প্রদান করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*

### 3.3 RULE-FLD-01: Haor Basin Pre-Flood Emergency Harvest Alert
- **Rule ID**: `RULE-FLD-01`
- **Product Mapping**: `FR-ADV-02`, `FR-ADV-03`
- **Target Geography**: Haor Basin (Sunamganj Sadar `BD-60-90-86`, Tahirpur `BD-60-90-89`).
- **Target Crop & Stage**: Boro rice, Dough Stage / Physiological Maturity ($\ge 80\%$ grain yellowing).
- **Trigger Conditions**:
  1. Composite Flash Flood Hazard Index $I_{\text{flood}} \ge 0.75$.
  2. Transboundary catchment 48h rainfall $P_{\text{cat}} \ge 100.0\text{ mm}$.
  3. Surma river stage $H \ge (DL - 0.50\text{ m})$ ($H \ge 7.75\text{ m}$ PWD).
  4. 24h rate of river stage rise $\frac{\Delta H}{\Delta t} \ge 0.50\text{ m/day}$.
  5. Grain maturity $\ge 80\%$ (or days since transplanting $\ge 125$).
- **Headline (Bangla)**: **"জরুরি ধান কর্তন প্রস্তুতি (জরুরি সতর্কবার্তা)"**
- **Plain-Language Explanation (Bangla)**:
  > *"উজান থেকে মেঘালয়ের পাহাড়ি ঢল ও নদীর পানি দ্রুত বৃদ্ধি পাওয়ায় আগামী ৪৮–৭২ ঘণ্টার মধ্যে হাওড়ে আকস্মিক বন্যার উচ্চ ঝুঁকি রয়েছে। যেসকল জমির ধান ৮০% পেকেছে (শীষের শতকরা ৮০ ভাগ ধান সোনালী হয়েছে), অবিলম্বে দলবদ্ধভাবে বা কম্বাইন হারভেস্টার দিয়ে ধান কেটে নিরাপদ স্থানে নিয়ে যান।"*
- **Action Items (Bangla)**:
  1. যেসব জমির ধান ৮০% পেকেছে, বিলম্ব না করে দ্রুত কর্তন সম্পন্ন করুন।
  2. কেটে আনা ধান তাৎক্ষণিকভাবে উঁচু স্থান বা ড্রায়ারে শুকানোর ব্যবস্থা করুন।
  3. হাওড়ের বাঁধের অবস্থা পর্যবেক্ষণে স্থানীয় ইউনিয়ন পরিষদ ও কৃষি কর্মকর্তার সাথে সার্বক্ষণিক যোগাযোগ রাখুন।
- **Mandatory Anti-Panic Notice**: *"যেসব জমির ধান এখনও কাঁচা বা দুধ অবস্থায় রয়েছে, সেগুলো কাটা যাবে না। বাঁধের অবস্থা পর্যবেক্ষণে স্থানীয় ইউনিয়ন পরিষদ ও কৃষি কর্মকর্তার সাথে যোগাযোগ রাখুন।"*

### 3.4 RULE-TMP-01: Booting Stage Cold Injury Warning
- **Rule ID**: `RULE-TMP-01`
- **Target Crop & Stage**: Boro rice, Booting / Panicle Initiation.
- **Trigger Conditions**: $T_{\text{min}} \le 15.0^\circ\text{C}$ for $\ge 3$ consecutive days.
- **Headline (Bangla)**: **"শৈত্যপ্রবাহ ও বন্ধ্যাত্ব ঝুঁকি (সতর্কবার্তা)"**
- **Action Directives (Bangla)**:
  1. সন্ধ্যায় জমিতে ৫–৭ সেমি গভীরতায় সেচের পানি প্রবেশ করান।
  2. সকালে অতিরিক্ত ঠান্ডা পানি নিষ্কাশন করে নতুন পানি দিন।
  3. শৈত্যপ্রবাহ চলাকালীন ইউরিয়া সারের উপরিপ্রয়োগ বন্ধ রাখুন।

### 3.5 RULE-TMP-02: Anthesis Terminal Heat Stress Warning
- **Rule ID**: `RULE-TMP-02`
- **Target Crop & Stage**: Boro rice, Anthesis / Flowering.
- **Trigger Conditions**: $T_{\text{max}} \ge 35.0^\circ\text{C}$ for $\ge 2$ consecutive days.
- **Headline (Bangla)**: **"তীব্র তাপদাহ সতর্কতা (সতর্কবার্তা)"**
- **Action Directives (Bangla)**:
  1. সকাল ৯টা থেকে দুপুর ১২টা পর্যন্ত জমির ক্যানোপি ঠান্ডা রাখতে ৩–৫ সেমি পানি ধরে রাখুন।
  2. তীব্র রোদে ফুল শুকিয়ে যাওয়া রোধে বিকেলে হালকা সেচ দিন।
