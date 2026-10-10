# Ritucast Scientific Transparency and Uncertainty Patterns

## 1. Executive Summary & Design Mandate

Agricultural decisions carry immediate physical and financial consequences for smallholders. Presenting uncertain predictions with unearned visual confidence is irresponsible and dangerous (`DEC-08`, `DEC-10`).

This specification establishes the visual and layout patterns that guarantee **scientific transparency, explicit data provenance, and honest uncertainty communication** across the Ritucast platform.

---

## 2. Visual Separation of the Four Information Tiers (`DEC-08`)

The interface visually partitions every piece of information into one of four distinct visual containers:

```
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 1: EMPIRICAL OBSERVATION (প্রত্যক্ষ পর্যবেক্ষণ)                     │
│ Border: 1px solid #CBD5E1 | Accent: Slate Blue | Source: BMD Station   │
│ "বিগত ২৪ ঘণ্টায় বৃষ্টিপাত: ০.০ মিমি (রাজশাহী বিএমডি স্টেশন)"              │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 2: DERIVED INDICATOR (হিসাবকৃত সূচক)                              │
│ Border: 1px solid #99F6E4 | Accent: Teal | Method: FAO-56 Penman       │
│ "দৈনিক বাষ্পীভবন (ET₀): ৪.২ মিমি/দিন | মাটির রস ঘাটতি: ১৬ মিমি"          │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 3: PROBABILISTIC FORECAST (পূর্বাভাস মডেল)                         │
│ Border: 1px dashed #38BDF8 | Accent: Azure | Consensus: 85%            │
│ "আগামীকাল বৃষ্টির সম্ভাবনা: ৭০% (মাঝারি বৃষ্টি, ১৫–২৫ মিমি)"             │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 4: ACTIONABLE RECOMMENDATION (কার্যকর পরামর্শ)                   │
│ Border: 2px solid #15803D | Surface: High Contrast | Gating: Verified  │
│ [🟢 সেচ স্থগিত রাখুন] + "মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন"           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Reusable Scientific Transparency Patterns

### 3.1 Standard Provenance Footer Pattern
Every Tier 1, Tier 2, and Tier 3 card terminates with an accessible, high-contrast provenance footer:
```html
<footer class="card-provenance">
  <div class="provenance-meta">
    <span class="provenance-time">🕒 উপাত্ত সংগ্রহের সময়: আজ সকাল ০৬:০০</span>
    <span class="provenance-source">উৎস: বাংলাদেশ আবহাওয়া অধিদপ্তর (বিএমডি) ও নাসা পাওয়ার</span>
  </div>
  <button class="btn-text provenance-toggle" aria-expanded="false">
    <svg aria-hidden="true" class="icon-info">...</svg>
    তথ্যসূত্র ও বিস্তারিত
  </button>
</footer>
```
- Tapping **"তথ্যসূত্র ও বিস্তারিত"** slides up a lightweight drawer displaying:
  - Upstream provider name and API endpoint.
  - Spatial resolution (e.g., $10\text{km}$ grid).
  - Processing pipeline version (`v1.0.0`).

---

### 3.2 Automated Advisory Suppression Visual Pattern (`DEC-10`, `ADR-08`)
When upstream weather forecast models disagree sharply (ensemble spread $>50\%$) or satellite data is $>36\text{ hours}$ old:
- **Visual Action**: The green/red actionable advisory card is **completely replaced** by the high-visibility amber suppression banner:

```
┌────────────────────────────────────────────────────────────────────────┐
│ ⚠️ স্বয়ংক্রিয় পরামর্শ সাময়িকভাবে স্থগিত                                  │
├────────────────────────────────────────────────────────────────────────┤
│ বর্তমান আবহাওয়া পূর্বাভাসের অনিশ্চয়তা বেশি থাকায় (মডেল মতভেদ > ৫০%)     │
│ স্বয়ংক্রিয় সেচ পরামর্শ সাময়িকভাবে স্থগিত রাখা হয়েছে।                     │
│                                                                        │
│ করণীয়: সেচ দেওয়ার পূর্বে আপনার জমির আইল ও মাটির রস নিজে হাত দিয়ে পরীক্ষা  │
│ করুন এবং স্থানীয় কৃষি কর্মকর্তার সাথে যোগাযোগ রাখুন।                    │
├────────────────────────────────────────────────────────────────────────┤
│ 🕒 সর্বশেষ যাচাই: আজ সকাল ০৮:০০ | মডেল: ECMWF vs GFS                    │
└────────────────────────────────────────────────────────────────────────┘
```
- The underlying Tier 1 empirical observations (temperature, yesterday's rainfall) remain fully legible below the banner.

---

### 3.3 Context Gating Incomplete Pattern (`DEC-17`)
When a user opens the application but has not confirmed their crop growth stage:
- Actionable advice is locked behind an accessible prompt card:
```
┌────────────────────────────────────────────────────────────────────────┐
│ 🌾 ফসলের বৃদ্ধির ধাপ নির্বাচন করুন                                     │
├────────────────────────────────────────────────────────────────────────┤
│ আপনার বোরো ধান বর্তমানে কোন পর্যায়ে রয়েছে? সঠিক পর্যায় নির্বাচন করলে     │
│ বিজ্ঞানসম্মত সেচ পরামর্শ পাওয়া যাবে:                                   │
│                                                                        │
│ [ চারা/কুশি ]  [ থোড় পর্যায় ]  [ ফুল ফোটা ]  [ দানা গঠন ]  [ পাকা ধান ]   │
└────────────────────────────────────────────────────────────────────────┘
```
- Once the user taps a chip, the card animates smoothly into the verified Tier 4 advisory.

---

### 3.4 Mandatory Field-Verification Warning Box
Every Tier 4 card includes a prominent, un-dismissable field-check alert box:
```html
<aside class="field-verification-alert">
  <svg class="alert-icon" aria-hidden="true">⚠️</svg>
  <p class="alert-copy">
    <strong>সতর্কবার্তা:</strong> সেচ বন্ধ করার আগে আপনার জমির আইল ও মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।
  </p>
</aside>
```
- Background: `#FEF3C7` (Warm Amber tint).
- Border: `1px solid #D97706`.
- Typography: $13\text{px}$, bold title, high contrast ($6.2:1$).
