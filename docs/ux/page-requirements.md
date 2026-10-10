# Ritucast Page-Level Content and Layout Requirements

## 1. Executive Summary & Layout Guidelines

This specification defines the structural content hierarchy, functional blocks, controls, data provenance elements, and interaction states for every initial-release page.

### Architectural Rules Enforced
1. **Content Priority**: Farmer operational decisions first; supporting empirical observations second; deep remote sensing metadata tucked into expandable drawers.
2. **Four-Tier Visual Separation (`DEC-08`)**: Each page clearly partitions Tier 1 (Observations), Tier 2 (Indicators), Tier 3 (Predictions), and Tier 4 (Recommendations).
3. **Strict Mobile-First Constraints (`DEC-09`)**: All views are designed to render cleanly within a 360px–420px viewport without horizontal scrolling; peak client heap memory $\le 45\text{MB}$.
4. **Scope Exclusions**: Final visual styling, color palettes, CSS tokens, and font files are strictly reserved for [Phase 7: Visual Design and Design System](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-06/handoff-to-phase-07.md).

---

## 2. Page-Level Specifications

---

### PAGE-01: আজকের পরামর্শ (Today's Advisory / Overview)
- **Route Path**: `/` or `/advisory`
- **Page Objective**: Provide instant operational clarity regarding whether to irrigate, harvest, or prepare for weather risks today.
- **Primary User Question**: *"আজ আমার জমিতে কী কাজ করা উচিত বা কী সতর্কতা নেওয়া প্রয়োজন?"*
- **Main Heading & Context**: *"আজকের কৃষি পরামর্শ — [উপজেলা নাম]"* (e.g., গোদাগাড়ী, রাজশাহী).
- **Primary Action**: "পরামর্শ শেয়ার করুন" (Share Advisory via WhatsApp/Web Share).
- **Secondary Actions**: "কেন এই পরামর্শ?" (Open Reasoning Drawer), "মাটির রস পরীক্ষা নির্দেশিকা" (Open Verification Guide).
- **Essential Content Blocks**:
  1. *Global Context Bar*: Location Chip `[গোদাগাড়ী ▾]`, Crop/Stage Chip `[বোরো ধান: থোড় পর্যায় ▾]`, Freshness Pill `[আপডেট: ৮:০০ টা]`.
  2. *Critical Alert Banner (Conditional)*: High flood warning or advisory suppression notice.
  3. *Tier 4 Recommendation Card*:
     - Action Badge: "সেচ স্থগিত রাখুন" (Postpone Irrigation) or "জরুরি ধান কর্তন" (Emergency Harvest).
     - Plain Bangla Justification: 2 sentences explaining the weather and soil rationale.
     - Economic Benefit Pill: Estimated cost savings (টাকা সাশ্রয়).
     - Mandatory Field Verification Notice (`DEC-10`): *"সেচ দেওয়ার পূর্বে জমির আইল ও মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*
  4. *Today's Environmental Snapshot (Tier 1 & 2)*: 3-column micro-card row:
     - তাপমাত্রা (Current Temp, °C)
     - ২৪ ঘণ্টা বৃষ্টিপাত (Rainfall, mm)
     - মাটির আর্দ্রতা অবস্থা (Soil Moisture Status: পর্যাপ্ত/ঘাটতি)
  5. *Quick Navigation Shortcuts*: Buttons routing to Detailed Weather (`PAGE-02`) or Soil/Flood (`PAGE-03`).
- **Data Provenance & Freshness**: Footer link: *"তথ্যসূত্র: বিএমডি ও নাসা পাওয়ার (সংগৃহীত: ১০ অক্টোবর, সকাল ০৬:০০)"*.
- **States**:
  - *Loading*: Skeleton placeholder cards mimicking the 3-section layout.
  - *Context Gating Failed*: Prompt card: *"সঠিক পরামর্শ পেতে অনুগ্রহ করে ফসলের ধাপ নিশ্চিত করুন"* with 1-tap stage buttons.
  - *Suppressed State*: Replaces action card with amber fallback banner advising manual field inspection.
- **Mobile Behavior**: Vertically stacked single-column flow; 16px horizontal screen padding.

---

### PAGE-02: আবহাওয়া ও পূর্বাভাস (Weather & Climate Forecast)
- **Route Path**: `/weather`
- **Page Objective**: Provide detailed atmospheric observations, 48-hour rainfall probabilities, and weekly trends for agricultural planning.
- **Primary User Question**: *"আগামী ৪৮ ঘণ্টায় কখন এবং কতটুকু বৃষ্টি হতে পারে?"*
- **Main Heading**: *"আবহাওয়া ও বৃষ্টিপাতের পূর্বাভাস"*
- **Primary Action**: "৪৮ ঘণ্টা পূর্বাভাস দেখুন" (Toggle to 48h view).
- **Secondary Actions**: "৭ দিনের ধারা" (Toggle weekly view), "উৎস ও নির্ভরযোগ্যতা" (Open Metadata Drawer).
- **Essential Content Blocks**:
  1. *Sub-Navigation Segmented Control*: [বর্তমান আবহাওয়া] [৪৮ ঘণ্টা পূর্বাভাস] [৭ দিনের ধারা].
  2. *Tier 1 Current Weather Panel*:
     - Primary metric: তাপমাত্রা (°C) ও অনুভূতির তাপমাত্রা (Feels-like °C).
     - Secondary metrics grid: আপেক্ষিক আর্দ্রতা (%), বাতাসের গতি ও দিক (km/h), সৌর বিকিরণ (MJ/m²), বিগত ২৪ ঘণ্টার বৃষ্টিপাত (mm).
     - Station origin: *"নিকটবর্তী বিএমডি স্টেশন: রাজশাহী বিমানবন্দর (দূরত্ব: ১৮ কিমি)"*.
  3. *Tier 3 48-Hour Rainfall Forecast Panel*:
     - Quantitative rain chance pill: *"বৃষ্টির সম্ভাবনা: ৬৫% (মাঝারি বৃষ্টি)"*.
     - 3-Hour Interval Precipitation Bar Chart: Horizontal scrollable time blocks showing expected rain volume (mm) and rain probability bar (%).
     - Multi-Model Consensus Indicator: *"মডেল একমত: উচ্চ (ECMWF ও GFS পূর্বাভাসের মিল ৮৫%)"*.
  4. *Weekly Outlook List (7 Days)*: High/low temperature ranges and daily rain icons with uncertainty decay markers.
- **Data Provenance**: Explicit citation: *"উৎস: বিএমডি, ইসিএমডব্লিউএফ আইএফএস ও জিএফএস এনডব্লিউপি মডেল"*.
- **States**:
  - *High Model Spread (>50%)*: Warning badge: *"পূর্বাভাসে মডেলের মতভেদ রয়েছে; বৃষ্টিপাতের সময় পরিবর্তন হতে পারে"*.
- **Accessibility**: Screen reader table summary accompanying the bar chart.

---

### PAGE-03A: মাটি ও সেচ (Soil & Irrigation — Barind Mode)
- **Route Path**: `/soil-irrigation`
- **Page Objective**: Guide deep tubewell irrigation scheduling and soil water management using Alternate Wetting and Drying (AWD) principles.
- **Primary User Question**: *"আমার ধানের শিকড় অঞ্চলে কতটুকু পানি আছে এবং পরবর্তী সেচ কখন লাগবে?"*
- **Main Heading**: *"মাটির আর্দ্রতা ও সেচ ব্যবস্থাপনা — বরেন্দ্র অঞ্চল"*
- **Primary Action**: "এডব্লিউডি পাইপ পরীক্ষা পদ্ধতি দেখুন" (View AWD Inspection Guide).
- **Essential Content Blocks**:
  1. *Tier 2 Root-Zone Soil Water Deficit Gauge*:
     - Semi-circular gauge or linear bar illustrating Current Depletion ($D_t$) vs Readily Available Water ($RAW$).
     - Status zone indicator: সবুজ (পর্যাপ্ত রস) $\to$ হলুদ (সতর্কতা অঞ্চল) $\to$ লাল (সেচ প্রয়োজন).
  2. *Evapotranspiration & Water Balance Table*:
     - রেফারেন্স বাষ্পীভবন ($ET_0$): ৪.২ মিমি/দিন (FAO-56 Penman-Monteith).
     - ফসলের পানি চাহিদা ($ET_c = K_c \times ET_0$): ৪.৮ মিমি/দিন ($K_c = 1.15$ থোড় পর্যায়).
     - কার্যকর বৃষ্টিপাত ($P_{\text{eff}}$): ০.০ মিমি.
     - বর্তমান মাটির ঘাটতি ($D_t$): ১৮ মিমি ($RAW = 28$ মিমি).
  3. *Alternate Wetting and Drying (AWD) Field Tube Guide*:
     - Step-by-step illustrated diagram showing how to observe the water table inside the perforated plastic pipe (পানি মাটির নিচে ১৫ সেমি যাওয়ার আগে সেচ না দেওয়ার নিয়ম).
  4. *Cost Savings Card*: Total irrigation hours and diesel/electricity expenses saved during the season.
- **Data Provenance**: *"গণনা পদ্ধতি: এফএও-৫৬ পেনম্যান-মন্টিথ সমীকরণ ও নাসা পাওয়ার সৌর বিকিরণ"*.

---

### PAGE-03B: বন্যা ও প্লাবন (Flood & Inundation — Haor Mode)
- **Route Path**: `/flood-hazard`
- **Page Objective**: Monitor transboundary flash-flood threats to pre-monsoon Boro rice and guide emergency harvest mobilization.
- **Primary User Question**: *"হাওরে আকস্মিক বন্যা আসার ঝুঁকি কতটুকু এবং ধান কাটার প্রস্তুতি নেওয়া দরকার কি?"*
- **Main Heading**: *"আকস্মিক বন্যা ও প্লাবন ঝুঁকি — হাওর অববাহিকা"*
- **Primary Action**: "জরুরি কর্তন নির্দেশনা দেখুন" (View Harvest Action Plan).
- **Essential Content Blocks**:
  1. *Tier 2 Composite Flood Hazard Gauge*:
     - 3-Level Threat Meter based on $I_{\text{flood}}$ (`DEC-16`):
       - স্বাভাবিক (Normal: $0.00–0.49$)
       - সতর্কবার্তা (Watch: $0.50–0.74$)
       - জরুরি সতর্কতা (Emergency Alert: $0.75–1.00$)
  2. *Contributing Environmental Proxies Grid (3 Cards)*:
     - *Card A (Catchment Rain)*: মেঘালয় চেরাপুঞ্জি ৪৮ ঘণ্টা বৃষ্টিপাত ($P_{\text{cat}}$) = ১৪০ মিমি (থ্রেশহোল্ড ১০০ মিমি).
     - *Card B (River Stage)*: সুরমা নদী (সুনামগঞ্জ পয়েন্ট) পানি উচ্চতা = ৬.৮৫ মিটার (বিপদসীমা ৭.২৫ মি; দূরত্ব ০.৪০ মি; বৃদ্ধির হার +০.৭ মি/২৪ ঘণ্টা).
     - *Card C (Satellite Inundation)*: সেন্টিনেল-১ এসএআর রাডার প্লাবিত এলাকা = ১২% (বিগত ৬ দিনের পরিবর্তন +৫%).
  3. *Phenological Harvest Matrix*:
     - যদি ধান $\ge ৮০\%$ পাকা থাকে $\to$ **অবিলম্বে ধান কেটে ঘরে তুলুন**.
     - যদি ধান দুধ/দানা গঠন পর্যায়ে থাকে $\to$ **ফসলরক্ষা বাঁধ তদারকি জোরদার করুন**.
- **Data Provenance**: *"উৎস: বিডব্লিউডিবি সুরমা নদী গেজ, নাসা জিপিএম বৃষ্টিপাত ও সেন্টিনেল-১ সার রাডার"*.

---

### PAGE-04: মানচিত্র ও বিশ্লেষণ (Geospatial Diagnostic Map)
- **Route Path**: `/map`
- **Page Objective**: Provide regional geospatial context and visual confirmation of rainfall, moisture, and flood anomalies.
- **Primary User Question**: *"আশেপাশের উপজেলা এবং পুরো অঞ্চলে আবহাওয়া ও বন্যার পরিস্থিতি কেমন?"*
- **Main Heading**: *"আঞ্চলিক মানচিত্র ও বিশ্লেষণ"*
- **Behavior**: **Lazy-Loaded**. Map container initializes only upon tab selection.
- **Essential Content Blocks**:
  1. *Map Canvas*: Full-width interactive MapLibre GL JS vector map centered on active Upazila.
  2. *Layer Control Chips (Top Overlay)*:
     - [উপজেলা সীমানা] [৪৮ ঘণ্টা বৃষ্টিপাত] [প্লাবিত এলাকা (সার)] [মাটির রস ঘাটতি].
  3. *Map Legend (Bottom Left Overlay)*: Color scale explaining metric thresholds and units.
  4. *Coarse Resolution Notice Banner*:
     - *"⚠️ বিজ্ঞপ্তি: স্যাটেলাইট উপাত্ত আঞ্চলিক পরিস্থিতি (১০ কিমি গ্রিড) প্রদর্শন করে; এটি একক জমির প্লট সীমানা নির্দেশ করে না।"*
- **Mobile Behavior**: Map canvas height capped at 65vh on mobile; sticky card at bottom summarizing the selected polygon's zonal statistics.

---

### PAGE-05: সহায়িকা ও তথ্যসূত্র (Help, Sources & Methodology)
- **Route Path**: `/help`
- **Page Objective**: Provide transparent methodology explanations, data provenance tracking, terminology glossary, and extension contacts.
- **Essential Content Blocks**:
  1. *Methodology Cards*: Accordions explaining FAO-56 Penman-Monteith, AWD irrigation, and satellite radar sensing.
  2. *Data Sources Registry Link (`/help/sources`)*: Upstream provider statuses and update latency logs.
  3. *Agronomic Glossary Link (`/help/glossary`)*: Plain Bangla definitions for technical terms.
  4. *DAE Emergency Contacts (`/help/contacts`)*: Names, phone numbers, and block assignments for SAAOs in pilot Upazilas.
