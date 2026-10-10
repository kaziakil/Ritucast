# Ritucast Geographic Context and Selection Model

## 1. Executive Summary & Geographic Scope

This specification defines how the Ritucast user interface handles geographic location, administrative hierarchy, spatial persistence, and resolution boundaries.

### Core Boundaries & Guardrails
1. **Administrative Unit of Analysis**: The platform operates strictly at the **Upazila (উপজেলা)** administrative level for the initial release (`DEC-03`).
2. **Dual-Zone Pilot Testbeds**:
   - **High Barind Tract** (Rajshahi Division): **Godagari (গোদাগাড়ী)** and **Tanore (তানোর)**.
   - **Haor Basin** (Sylhet Division): **Sunamganj Sadar (সুনামগঞ্জ সদর)** and **Tahirpur (তাহিরপুর)**.
3. **Strict Exclusion of Farm Parcel Precision (`DEC-06`, `RSK-03`)**: Ritucast does not collect, display, or promise sub-acre plot boundaries or GPS coordinates. Satellite observations (10km–36km grids) are aggregated to Upazila zonal statistics. The UI explicitly communicates that indicators represent regional agro-climatic conditions.

---

## 2. Geographic Hierarchy & Administrative Model

```
[ National Tier: Bangladesh ] (Coarse Agro-Meteorological Background)
      │
      ├── [ Division: Rajshahi ]
      │         └── [ District: Rajshahi ]
      │                   ├── [ Upazila: Godagari (গোদাগাড়ী) ] (Pilot Testbed 1)
      │                   └── [ Upazila: Tanore (তানোর) ]      (Pilot Testbed 2)
      │
      └── [ Division: Sylhet ]
                └── [ District: Sunamganj ]
                          ├── [ Upazila: Sunamganj Sadar (সুনামগঞ্জ সদর) ] (Pilot Testbed 3)
                          └── [ Upazila: Tahirpur (তাহিরপুর) ]             (Pilot Testbed 4)
```

---

## 3. Geographic Selection Behavior & Interaction Patterns

### 3.1 Primary Selection Mechanism: Text/Chip Modal (Non-Map-Based)
- **Rationale**: Budget Android devices on 3G connections experience high latency and WebGL crashes if forced to render an interactive map solely to pick a location (`DEC-09`, `ADR-06`).
- **Interaction**:
  1. The user taps the **Location Pill** in the top header (`[ 📍 গোদাগাড়ী ▾ ]`).
  2. A slide-up bottom sheet opens instantly (<100ms).
  3. The sheet provides:
     - Search input field: *"উপজেলা খুঁজুন..."* with fuzzy Bangla autocomplete.
     - Grouped quick-select chips:
       - **বরেন্দ্র অঞ্চল (খরা ও সেচ)**: `[ গোদাগাড়ী ]` `[ তানোর ]`
       - **হাওর অববাহিকা (বন্যা ও ধান কর্তন)**: `[ সুনামগঞ্জ সদর ]` `[ তাহিরপুর ]`
  4. Selection is instantaneous on tap; the modal auto-dismisses and updates application context.

### 3.2 Secondary Selection Mechanism: Map-Based Tap (Diagnostic Map Tab)
- When using `PAGE-04: মানচিত্র ও বিশ্লেষণ`, tapping an administrative polygon updates the active Upazila context after a confirmation tooltip: *"এই উপজেলার তথ্য দেখতে চান? [হাঁ, দেখুন]"*.

### 3.3 Default Geographic Context
- **First Visit**: Displays `/onboarding` modal prompting location selection.
- **Subsequent Visits**: Context restores from `localStorage.getItem('ritucast_upazila_id')`.
- **Fallback Default**: If local storage is corrupted or cleared, defaults to **Godagari (গোদাগাড়ী, রাজশাহী)** with a contextual notice: *"বর্তমান অবস্থান: গোদাগাড়ী (পরিবর্তন করতে ট্যাপ করুন)"*.

---

## 4. State Persistence and Dynamic View Adaptation

### 4.1 Persistence Across Navigation
- The active Upazila ID is stored in client state (React Context / Zustand) and mirrored in URL search params (`?upazila=godagari`) and `localStorage`.
- All tab transitions (`/advisory` $\leftrightarrow$ `/weather` $\leftrightarrow$ `/map`) retain the selected Upazila context seamlessly.

### 4.2 Dynamic Regional Module Adaptation
When the user switches Upazilas, the application dynamically reconfigures its navigation and data contracts:

| Active Upazila | Agro-Ecological Zone | Module 3 Tab Rendered | Core Scientific Model |
| :--- | :--- | :--- | :--- |
| **Godagari** | AEZ 26: High Barind Tract | **মাটি ও সেচ (Soil & Irrigation)** | FAO-56 Penman-Monteith, AWD Water Deficit ($D_t$) |
| **Tanore** | AEZ 26: High Barind Tract | **মাটি ও সেচ (Soil & Irrigation)** | FAO-56 Penman-Monteith, AWD Water Deficit ($D_t$) |
| **Sunamganj Sadar** | AEZ 21: Sylhet Basin / Haor | **বন্যা ও প্লাবন (Flood & Inundation)** | Multi-factor Haor Flood Index ($I_{\text{flood}}$) |
| **Tahirpur** | AEZ 21: Sylhet Basin / Haor | **বন্যা ও প্লাবন (Flood & Inundation)** | Multi-factor Haor Flood Index ($I_{\text{flood}}$) |

---

## 5. Handling Unsupported Areas & Data Gaps

### 5.1 Unsupported Upazila Handling
If a user searches for an Upazila outside the two pilot zones (e.g., *মিরপুর, কুষ্টিয়া* or *কালিয়াকৈর, গাজীপুর*):
- The autocomplete shows the item disabled with an informative tag: `[পরবর্তী ধাপে অন্তর্ভুক্ত]`.
- Tapping it displays an explanatory card:
  > **"পাইলট বহির্ভূত এলাকা"**
  > *"রিতুকাস্ট বর্তমানে বরেন্দ্র অঞ্চল (গোদাগাড়ী, তানোর) এবং হাওর অঞ্চলে (সুনামগঞ্জ সদর, তাহিরপুর) পরীক্ষামূলকভাবে সেবা দিচ্ছে। খুব শীঘ্রই আপনার উপজেলায় সেবা চালু করা হবে। ডেমো দেখতে যেকোনো একটি পাইলট উপজেলা নির্বাচন করুন।"*
  > Primary button: `[ গোদাগাড়ী দেখুন ]` `[ তাহিরপুর দেখুন ]`

### 5.2 Insufficient Spatial Data Coverage
If satellite revisit latency (e.g., Sentinel-1 SAR orbit gap) leaves an Upazila with partial spatial coverage ($<70\%$ valid pixels):
- The UI retains the Upazila context but displays a data quality badge:
  > *"আংশিক স্যাটেলাইট উপাত্ত (৭০% কভারেজ); বৃষ্টিপাত ও আবহাওয়া তথ্যের ভিত্তিতে সূচক প্রস্তুত।"*
- The system never silently shows zero flood extent or zero moisture deficit.

---

## 6. Spatial Precision Copy & Disclaimers

To protect farmer trust and prevent misinterpretation of coarse remote sensing data (`RSK-03`):
1. **Mandatory Grid Scale Disclaimer on Map**:
   > *"উপগ্রহ চিত্রে প্রদর্শিত তথ্য পুরো উপজেলার সামগ্রিক প্রবণতা নির্দেশ করে (প্রতিটি গ্রিড ১০x১০ কিমি)। এটি কোনো একক জমির বা প্লটের পরিমাপ নয়।"*
2. **Mandatory Field-Level Verification Rule**:
   > *"সেচের সিদ্ধান্ত নেওয়ার পূর্বে আপনার নিজ জমির মাটির রস পরীক্ষা করুন।"*
