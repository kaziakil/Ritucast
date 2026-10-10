# Ritucast Accessibility, Localization, and Low-Connectivity Specification

## 1. Executive Summary & Standards Framework

This specification defines the UX and technical presentation standards for accessibility, language localization, and performance in low-bandwidth rural environments.

### Target Standards
- **Accessibility**: Compliance with **WCAG 2.2 Level AA** standards.
- **Localization**: **Bangla-First (বাংলা-প্রথম)** with authentic agrarian terminology and English secondary support.
- **Connectivity**: Resilient operation over **rural 2G/3G cellular networks** with offline-first PWA caching (`DEC-09`, `NFR-USE-02`, `NFR-PER-01`).

---

## 2. Accessibility Specification (WCAG 2.2 Level AA)

### 2.1 Touch Targets and Physical Ergonomics (SC 2.5.8)
- Target users include farmers operating devices outdoors with dirty, wet, or calloused hands on scratched budget smartphone screens.
- **Touch-Target Minimum**: All interactive buttons, chips, links, and navigation icons must satisfy a minimum hit area of **$48 \times 48\text{px}$** with at least $8\text{px}$ of physical separation between adjacent targets.

### 2.2 Color Contrast and Glare Resilience (SC 1.4.3, SC 1.4.11)
- Rural users view smartphones in direct sunlight in open fields.
- **Text Contrast**: Normal text ($\le 18\text{px}$) must achieve at least **$4.5:1$** contrast against background.
- **Large Text & Headings**: Must achieve at least **$3.0:1$** contrast.
- **UI Components & Icons**: Active controls and boundaries must achieve at least **$3.0:1$** contrast against adjacent backgrounds.
- **High-Contrast Solar Theme**: Phase 7 design system must support high-contrast light mode optimized for sunlight readability.

### 2.3 Non-Color-Only Information Architecture (SC 1.4.1)
- Approximately 8% of male farmers in Bangladesh experience some form of red-green color deficiency.
- Color must **never** be the sole indicator of status, risk, or action:
  - Success/Normal: Green color paired with `[✓]` checkmark icon and text label "স্বাভাবিক / পর্যাপ্ত".
  - Alert/Warning: Amber color paired with `[⚠️]` triangle icon and text label "সতর্কবার্তা".
  - Danger/Emergency: Red color paired with `[🚨]` bell/siren icon and text label "জরুরি সতর্কতা".

### 2.4 Screen Reader Compatibility & Semantic HTML (SC 1.3.1, SC 4.1.2)
- Strict semantic HTML tags (`<main>`, `<nav>`, `<article>`, `<section>`, `<header>`, `<footer>`).
- Interactive elements must possess explicit `aria-label` or accessible names in Bangla (e.g., `<button aria-label="গোদাগাড়ী উপজেলা নির্বাচন করুন">`).
- **Accessible Alternatives for Visual Charts & Gauges**: Every SVG chart and canvas bar must be paired with an invisible or toggleable semantic table containing exact values (e.g., `<table class="sr-only">` summarizing the 48-hour rainfall hourly sequence).

### 2.5 Keyboard & Focus Management (SC 2.4.7, SC 2.1.1)
- Full operability via directional keypads and external Bluetooth keyboards.
- High-visibility focus ring: minimum 2px solid border with 2px offset.

---

## 3. Localization and Terminology Standards

### 3.1 Primary Language: Bangla-First
- All primary navigation, headings, advisory recommendations, error messages, and metrics are written in fluent, grammatically standard Bangla.
- An optional header toggle (`[ EN ]`) switches interface strings to English for international researchers and program officers.

### 3.2 Agricultural Terminology & Idiom Mapping

| Technical Data Term | Banned Literal Translation | Approved Agrarian Bangla Term | Practical Farmer Meaning |
| :--- | :--- | :--- | :--- |
| **Reference $ET_0$** | রেফারেন্স ইভাপোট্রান্সপিরেশন | **দৈনিক বাষ্পীভবন** | বাতাস ও রোদে দৈনিক পানি উড়ে যাওয়ার পরিমাণ |
| **Crop Water Deficit ($D_t$)**| মাটির পানির ঘাটতি মান | **মাটিতে রসের ঘাটতি** | ধানের শিকড়ে কতটুকু পানি কমে গেছে |
| **Alternate Wetting & Drying**| পর্যায়ক্রমিক আর্দ্রতা ও শুষ্কতা | **এডব্লিউডি / পর্যায়ক্রমিক সেচ** | পাইপে পানি মেপে মেপে সেচ দেওয়ার সাশ্রয়ী পদ্ধতি |
| **Flash Flood** | ফ্ল্যাশ ফ্লাড | **পাহাড়ি ঢল / আকস্মিক বন্যা** | মেঘালয় থেকে নেমে আসা দ্রুতগতির তীব্র বন্যা |
| **Panicle Initiation** | প্যানিকল ইনিশিয়েশন | **থোড় পর্যায় / ধানে থোড় আসা** | শিষ বের হওয়ার ঠিক আগের সংবেদনশীল পর্যায় |
| **Flowering / Anthesis** | ফুল ফোটা | **ধানে ফুল আসার পর্যায়** | পরাগায়নের সময় (চিটা হওয়ার ঝুঁকি থাকে) |
| **Precipitation Probability** | বৃষ্টিপাতের সম্ভাবনা সূচক | **বৃষ্টির সম্ভাবনা (%)** | আগামী ৪৮ ঘণ্টায় বৃষ্টি হওয়ার শতকরা সম্ভাবনা |
| **Ensemble Spread** | এনসেম্বল স্প্রেড | **মডেলের মতভেদ** | বিভিন্ন আবহাওয়া পূর্বাভাসের মধ্যে পার্থক্যের মাত্রা |

### 3.3 Numeric and Date Formats
- **Numerals**: Both English numerals (`0, 1, 2...`) and Bangla numerals (`০, ১, ২...`) are widely understood by SAAOs and farmers. Ritucast adopts standard Bangla numerals (`০, ১, ২...`) for body copy and metrics with optional user setting.
- **Time Zone**: All timestamps displayed in Bangladesh Standard Time (**BST, UTC+6**) formatted in 12-hour format with AM/PM equivalents (e.g., *"সকাল ০৮:০০ টা"*, *"বিকাল ০৪:৩০ টা"*).
- **Units**:
  - Rainfall: মিলিমিটার (`মিমি`)
  - Temperature: ডিগ্রি সেলসিয়াস (`°সে`)
  - Area: বিঘা (`বিঘা`) and একর (`একর`)
  - Cost: টাকা (`টাকা`)

---

## 4. Low-Connectivity & Offline Performance

### 4.1 Strict Payload Budgets (`DEC-09`, `ADR-03`)
- **Initial JS/CSS Bundle**: $\le 1.5\text{MB}$ uncompressed ($\le 350\text{KB}$ gzipped/Brotli).
- **Time-to-Interactive (TTI)**: $\le 3.5\text{s}$ over simulated 3G network conditions ($1.6\text{ Mbps}$ download, $300\text{ms}$ RTT).
- **Peak Client Heap Memory**: $\le 45\text{MB}$ on 2GB RAM budget Android hardware.

### 4.2 Progressive Web App (PWA) Offline-First Architecture (`ADR-01`)
- **Service Worker Lifecycle**:
  - Pre-caches core app shell (`index.html`, `index.css`, primary JS chunks, SVG icons, Bangla font subset).
  - Runtime cache: Caches the latest responses for `GET /api/v1/upazilas`, `GET /api/v1/weather/*`, and `GET /api/v1/advisories/*` for the active Upazila.
- **Field Offline Experience**:
  - When a farmer opens Ritucast in a low-lying haor or deep field block without cellular coverage, the app loads in $<1.0\text{s}$ from Cache Storage.
  - A persistent top pill alerts the user:
    > **"📡 অফলাইন মোড (সর্বশেষ আপডেট: আজ সকাল ০৮:০০)"**
  - Full advisory text, rainfall predictions, and AWD tube guides remain completely legible.

### 4.3 Map Asset Deferral (`ADR-06`)
- MapLibre GL JS v3 (approx. 220KB gzipped) and vector tile streams are **never loaded on initial app launch**.
- Only when the user explicitly taps the "মানচিত্র ও বিশ্লেষণ" tab does the browser asynchronously fetch map bundles.
