# Ritucast Trust, Uncertainty, and Data Quality UX Patterns

## 1. Executive Summary & Core Philosophy

This specification defines the user experience patterns for communicating data freshness, confidence levels, sensor limitations, and automated advisory suppression.

### Non-Negotiable Guardrails
1. **Never Equate Low Confidence with Low Risk**: An uncertain forecast (e.g., erratic convective storm cloudburst) must never be displayed as a calm "low risk" state. It must be explicitly communicated as an uncertain or high-volatility state.
2. **Never Use Color Alone**: Every status, alert, and hazard indicator must pair color with a distinct icon and descriptive Bangla text label to ensure accessibility for color-blind users and low-contrast mobile screens (WCAG 2.2 SC 1.4.1).
3. **Never Claim False Field-Level Precision**: Coarse remote sensing observations (10km–36km grids) must be transparently identified as regional agro-climatic context, never as sub-acre parcel measurements.
4. **Automated Suppression Mandate (`DEC-10`, `ADR-08`)**: When weather forecasts are stale (>36h) or model ensemble spread exceeds 50%, the system must automatically suppress actionable advice and render the safe manual verification notice.

---

## 2. Standardized State Taxonomy

The interface enforces an unambiguous distinction between 8 distinct epistemic states:

| State Taxonomy | Bangla Interface Label | Visual Icon | Definition & Meaning | What the User Can Do | What Must NOT Be Implied |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Confirmed Observation** | নিশ্চিত পর্যবেক্ষণ | 🟢 `[✓]` | Direct empirical reading from a validated physical sensor (e.g., BMD rain gauge, verified satellite pass). | View observation and proceed with confidence. | Does not imply field-specific microclimate. |
| **Elevated Risk** | উচ্চ ঝুঁকি | 🔴 `[⚠️]` | Verified indicators have exceeded dangerous physical thresholds (e.g., flash flood surge or critical water deficit). | Take immediate protective action. | Does not imply 100% certainty of catastrophic damage. |
| **Low Confidence** | কম আস্থা | 🟡 `[❓]` | Input data exists, but multi-model ensemble spread is wide ($40\%–60\%$ probability) or satellite latency is elevated. | View forecast with caution; inspect field. | **Must NEVER imply "low risk" or safety.** |
| **Insufficient Evidence** | অপর্যাপ্ত প্রমাণ | ⚪ `[ℹ️]` | Missing vital parameters (e.g., crop stage unknown, or weather sensor missing 2 key variables). | Complete context selection or check back later. | Must not imply zero risk or standard conditions. |
| **Stale Data** | পুরনো উপাত্ত | 🟠 `[🕒]` | Data exceeds freshness budget ($>24\text{h}$ old for forecast; $>36\text{h}$ for satellite). | View timestamp; refresh or rely on local weather. | Must not appear as live or current. |
| **Unavailable / Missing** | সাময়িক অনুপলব্ধ | 🔘 `[✕]` | Upstream provider outage (e.g., NASA POWER API downtime or CDSE satellite orbit gap). | View fallback local BMD readings; retry later. | Must not show false zero readings. |
| **Not Applicable** | প্রযোজ্য নয় | ➖ `[–]` | Module not relevant to active zone (e.g., flash flood module viewed in drought-prone Barind). | Switch to active regional modules. | Must not imply zero flood hazard. |
| **Not Yet Processed** | প্রক্রিয়াকরণাধীন | ⏳ `[⌛]` | Satellite pass sensed within 2 hours but zonal statistics still calculating in pipeline. | View previous cycle's verified data. | Must not display partially aggregated rasters. |

---

## 3. Trust Presentation Patterns

### 3.1 Freshness & Provenance Card Footer Pattern
Every Tier 1, 2, and 3 card includes a standardized provenance footer:
```
┌────────────────────────────────────────────────────────────────────────┐
│ [Card Body: 48h Rain Forecast Bar Chart]                               │
├────────────────────────────────────────────────────────────────────────┤
│ 🕒 উপাত্ত সংগ্রহের সময়: আজ সকাল ০৬:০০ | উৎস: বিএমডি ও নাসা পাওয়ার        │
│ [ ℹ️ বিস্তারিত ও সূত্র ]                                                │
└────────────────────────────────────────────────────────────────────────┘
```
- Tapping **"বিস্তারিত ও সূত্র"** slides up a drawer showing the upstream sensor name, spatial resolution, and last sync timestamp.

### 3.2 Automated Suppression Pattern (`DEC-10`, `ADR-08`)
When automated suppression is active:
```
┌────────────────────────────────────────────────────────────────────────┐
│ ⚠️ স্বয়ংক্রিয় পরামর্শ সাময়িকভাবে স্থগিত                                  │
├────────────────────────────────────────────────────────────────────────┤
│ বর্তমান আবহাওয়া পূর্বাভাসের অনিশ্চয়তা বেশি থাকায় (মডেল মতভেদ > ৫০%)     │
│ স্বয়ংক্রিয় সেচ পরামর্শ সাময়িকভাবে স্থগিত রাখা হয়েছে।                     │
│                                                                        │
│ করণীয়: সেচ দেওয়ার পূর্বে আপনার জমির আইল ও মাটির রস নিজে হাত দিয়ে পরীক্ষা  │
│ করুন এবং স্থানীয় কৃষি কর্মকর্তার সাথে যোগাযোগ রাখুন।                    │
└────────────────────────────────────────────────────────────────────────┘
```
- This replaces the green/red Tier 4 action card entirely.
- The underlying Tier 1 empirical weather observations remain viewable below the banner.

### 3.3 Context Gating Incomplete Pattern (`DEC-17`)
When Upazila, Crop, or Growth Stage is unconfirmed:
```
┌────────────────────────────────────────────────────────────────────────┐
│ 🌾 ফসলের বৃদ্ধির ধাপ নির্বাচন করুন                                     │
├────────────────────────────────────────────────────────────────────────┤
│ আপনার ধান বর্তমানে কোন পর্যায়ে রয়েছে? সঠিক পর্যায় নির্বাচন করলে সঠিক সেচ  │
│ পরামর্শ পাবেন:                                                         │
│                                                                        │
│ [ চারা/কুশি ]  [ থোড় পর্যায় ]  [ ফুল ফোটা ]  [ দানা গঠন ]  [ পাকা ধান ]   │
└────────────────────────────────────────────────────────────────────────┘
```
- Actionable advice is locked until the user taps one of the stage chips.

### 3.4 Multi-Model Forecast Consensus Pattern
On `PAGE-02: আবহাওয়া`, forecast consensus is visualized through a 3-tier meter:
- **মডেল একমত: উচ্চ (High Consensus)**: ECMWF and GFS forecasts agree within 15% $\to$ Normal advisory mode.
- **মডেল একমত: মাঝারি (Moderate Consensus)**: ECMWF and GFS agree within 30% $\to$ Informational note on possible timing shifts.
- **মডেল একমত: মতভেদ রয়েছে (Divergence / Uncertainty)**: Model spread $>50\%$ with rain chance between 40%–60% $\to$ Automated suppression triggered.

---

## 4. Linguistic Guardrails & Prohibited Terms

To maintain scientific integrity and prevent overconfidence, the UI enforces strict copy standards:

| Prohibited Term | Why It Is Banned | Approved Replacement Bangla Copy |
| :--- | :--- | :--- |
| *"১০০% নিশ্চিত"* | Violates scientific uncertainty principles. | *"প্রবল সম্ভাবনা রয়েছে"* (High probability) |
| *"নিশ্চিত বৃষ্টি"* | Numerical weather models are probabilistic. | *"বৃষ্টিপাতের সম্ভাবনা ৮০%"* (80% rain likelihood) |
| *"ফলনের নিশ্চয়তা"* | Agricultural yield depends on hundreds of factors beyond weather. | *"ফসলের পানির চাপ কমানোর পরামর্শ"* (Moisture stress mitigation) |
| *"কোনো ঝুঁকি নেই"* | Implies absolute safety and disarms vigilance. | *"বর্তমান ঝুঁকি স্বাভাবিক মাত্রায়"* (Current hazard level is normal) |
| *"আপনার জমির সঠিক পরিমাপ"* | Coarse satellite pixels cannot resolve smallholder parcels. | *"পুরো উপজেলার আঞ্চলিক গড় চিত্র"* (Upazila regional average) |
