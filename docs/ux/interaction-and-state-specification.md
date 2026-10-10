# Ritucast Interaction and State Specification

## 1. Executive Summary & Design System States

This specification establishes the standardized state machine and visual interaction requirements for all UI components in the Ritucast application.

By defining explicit specifications for all 14 interaction states, Ritucast ensures predictable user behavior, graceful failure degradation, and strict prevention of misleading agricultural claims.

---

## 2. Master State Matrix

| State ID | State Name | Occurrence Condition | Primary Visual Presentation | User Action Options | Cached Data Permitted? | What Must NOT Be Implied |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **`ST-01`** | **Initial / First Visit** | App opened without saved Upazila or crop preferences. | Clean onboarding modal prompting region and pilot Upazila selection. | Select pilot Upazila; confirm Boro rice; proceed. | No | Must not imply national availability yet. |
| **`ST-02`** | **Loading** | Network request in flight ($<2.5\text{s}$). | Animated skeleton placeholder cards matching final layout geometry. | Wait; back button remains active. | Yes (in background) | Must not show jarring full-screen spinners. |
| **`ST-03`** | **Success / Ideal** | Verified current data received from backend API. | High-contrast 4-tier cards with action badges, metrics, and plain Bangla text. | Read advice; share to WhatsApp; view details. | N/A | Must not claim 100% certainty or yield guarantees. |
| **`ST-04`** | **Empty State** | Section has no active items (e.g., zero active flood alerts in Barind). | Friendly illustration with reassurance text: *"কোনো সক্রিয় সতর্কতা নেই"*. | View general weather or switch to soil moisture. | No | Must not show broken blank space. |
| **`ST-05`** | **No Matching Results** | Search query in Upazila picker yields no match. | Text: *"কোনো উপজেলা পাওয়া যায়নি"*; lists pilot Upazila chips. | Clear search; tap one of 4 pilot Upazilas. | No | Must not freeze or close modal abruptly. |
| **`ST-06`** | **Invalid Input** | Out-of-bounds user filter or corrupted session data. | Inline validation notice: *"অনুগ্রহ করে সঠিক তথ্য নির্বাচন করুন"*. | Select valid option from dropdown or reset. | No | Must not submit broken requests to API. |
| **`ST-07`** | **Partial Data** | Satellite pass has $<70\%$ spatial coverage due to cloud or orbital gap. | Amber pill: *"আংশিক উপাত্ত (৭০% কভারেজ)"*; relies on weather models. | View available indicators with explicit caveat. | Yes | Must not claim zero flood extent or zero drought. |
| **`ST-08`** | **Stale Data** | Upstream weather $>24\text{h}$ old or satellite $>36\text{h}$ old. | Orange status badge: *"উপাত্ত পুরনো (আপডেট প্রক্রিয়াধীন)"*; shows sync age. | View timestamp; pull down to refresh; verify locally. | Yes (with badge) | **Must NEVER masquerade as live data.** |
| **`ST-09`** | **Unavailable Service** | Backend API or upstream NASA/ESA provider returns 503 / timeout. | Card notice: *"সার্ভারের সাথে সংযোগ স্থাপন করা যাচ্ছে না"*; retry button. | Tap "পুনরায় চেষ্টা করুন" (Retry); view cached data. | Yes | Must not display false default zeros. |
| **`ST-10`** | **Insufficient Evidence** | Missing critical context (Crop Stage unconfirmed) or missing variables. | Interactive prompt card: *"সঠিক পরামর্শ পেতে ফসলের বৃদ্ধির ধাপ নির্বাচন করুন"*. | Tap 1-click stage chip; unlock advisory card. | No | **Must NEVER emit an un-gated recommendation.** |
| **`ST-11`** | **Permission Denied** | User denies browser geolocation or Web Share API fails. | Seamless fallback: defaults to manual Upazila search or clipboard text copy. | Pick Upazila manually; copy advisory text. | N/A | Must not block access to core features. |
| **`ST-12`** | **Offline Mode** | Device loses cellular connection in remote field. | Persistent top banner: *"📡 অফলাইন মোড (সর্বশেষ আপডেট: সকাল ৮:০০)"*. | Read cached advisory and AWD guide; refresh disabled. | Yes | Must not imply live connectivity. |
| **`ST-13`** | **Recoverable Error** | Request failed due to momentary network drop ($<10\text{s}$). | Toast banner: *"নেটওয়ার্ক সমস্যা। পুনরায় চেষ্টা করা হচ্ছে..."* with Retry CTA. | Tap "পুনরায় চেষ্টা করুন" (Retry) or wait for auto-retry. | Yes | Must not lose user's selected location context. |
| **`ST-14`** | **Unrecoverable Error** | Critical JavaScript runtime failure or state corruption. | Safe crash screen: *"সাময়িক ত্রুটি ঘটেছে"* with [অ্যাপ রিস্টার্ট করুন] button. | Tap restart button to clear corrupted local state. | No | Must not loop indefinitely or show raw stack traces. |

---

## 3. Detailed Behavioral Specifications for Critical States

### 3.1 `ST-02`: Skeleton Loading Pattern
- **Layout**: Renders gray pulsing rectangular blocks mirroring the exact dimensions of:
  - The Location Bar (height: 48px).
  - The Tier 4 Advisory Card (height: 180px).
  - The 3 Environmental Micro-Cards (height: 90px).
- **Duration Budget**: If loading exceeds 3.5 seconds, displays an inline retry button: *"নেটওয়ার্ক কিছুটা ধীরগতির। [পুনরায় লোড করুন]"*.

### 3.2 `ST-10`: Insufficient Evidence / Context Gating Pattern
- **Trigger**: `GET /api/v1/advisories` called without a confirmed phenological growth stage.
- **Enforcement**:
  - The Tier 4 Action Card container is **locked**.
  - A friendly prompt card appears:
    > **"🌾 আপনার ধান এখন কোন ধাপে আছে?"**
    > *"সঠিক পরামর্শ পেতে বৃদ্ধির পর্যায় নির্বাচন করুন:"*
    > `[ চারা/কুশি ]` `[ থোড় পর্যায় ]` `[ ফুল ফোটা ]` `[ দানা গঠন ]` `[ পাকা ধান ]`
  - Tapping a chip updates application state in $<100\text{ms}$ and renders the advisory.

### 3.3 `ST-12`: Offline PWA Degradation Pattern
- **Trigger**: `navigator.onLine === false`.
- **Enforcement**:
  - Header displays a high-visibility persistent banner:
    > **"📡 অফলাইন মোড — সংরক্ষিত তথ্য প্রদর্শিত হচ্ছে (আপডেট: সকাল ০৮:০০)"**
  - All interactive advisory cards remain readable from Cache Storage.
  - Interactive map tile fetching is gracefully disabled with a note: *"মানচিত্র দেখতে ইন্টারনেট সংযোগ প্রয়োজন"*.
