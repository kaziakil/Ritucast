# Ritucast Component Design System Specification

## 1. Executive Summary & Component Hierarchy

The Ritucast Component System defines the reusable UI building blocks necessary to deliver the approved initial release screens (`PAGE-00` to `PAGE-05`) specified in [Phase 6: Page Requirements](file:///Users/kazi/Projects/RITUCAST/docs/ux/page-requirements.md).

Every component strictly adheres to:
1. **The 48px Touch-Target Rule (WCAG 2.2 SC 2.5.8)**.
2. **The Non-Color-Only Rule (WCAG 2.2 SC 1.4.1)**.
3. **The Four-Tier Information Taxonomy (`DEC-08`)**.
4. **Zero-Tailwind, Native CSS Token Consumption (`ADR-03`, `DEC-20`)**.

---

## 2. Core Component Specifications

---

### 2.1 Component: Standard 5-Section Advisory Card (`CMP-CARD-01`)
- **Purpose**: The universal information container used for Tier 1 observations, Tier 2 indicators, and Tier 4 recommendations.
- **Anatomy**:
  1. *Section A: Header*: Tier Category Pill (e.g., `পরামর্শ` or `হিসাবকৃত সূচক`) + Card Title.
  2. *Section B: Operational Status Badge*: High-contrast action pill (e.g., 🟢 `[✓] সেচ স্থগিত রাখুন`).
  3. *Section C: Plain Bangla Copy*: 2–3 concise sentences explaining the condition and practical advice.
  4. *Section D: Action & Economic Benefit*: Monetary cost-savings pill (e.g., `আনুমানিক সাশ্রয়: ৫০০–৭০০ টাকা`) + WhatsApp Share CTA.
  5. *Section E: Provenance Footer*: Data provider citations, observation timestamp, and mandatory field-verification notice (`DEC-10`).
- **Variants**:
  - `variant-tier1` (Neutral slate border, observation metrics).
  - `variant-tier2` (Subtle teal border, physical water balance indicators).
  - `variant-tier4` (Deep emerald/crimson border, high-contrast operational action).
  - `variant-suppressed` (Amber warning border, safe manual soil-check fallback notice).
- **States**: Default, Hover (`--color-bg-card-hover`), Focused, Loading Skeleton.
- **Accessibility**: Semantic `<article>` with `<h2/h3>` heading; high contrast ($\ge 7:1$).
- **When NOT to Use**: Do not use for simple global headers or standalone navigation buttons.

---

### 2.2 Component: Global App Bar & Location Chip (`CMP-NAV-01`)
- **Purpose**: Persistent top navigation landmark showing brand, active Upazila context, and connectivity status.
- **Anatomy**:
  - Left: Ritucast Logo mark + text.
  - Center/Right: **Location Pill Button** (`[ 📍 গোদাগাড়ী ▾ ]`). Tapping opens the Location Modal.
  - Far Right: Connectivity Pill (`[ 📡 অনলাইন / অফলাইন ]`) or Stage Badge.
- **Interaction**: Minimum 48px touch target; 1px solid border; accessible aria-haspopup.
- **Responsive Behavior**: Sticky top positioning (`position: sticky; top: 0; z-index: 100`).

---

### 2.3 Component: Mobile Bottom Navigation Bar (`CMP-NAV-02`)
- **Purpose**: Primary mobile navigation anchor across the 5 core application destinations.
- **Anatomy**: 5 Tab Items:
  1. `[ 🌾 পরামর্শ ]` (`/advisory`)
  2. `[ 🌦 আবহাওয়া ]` (`/weather`)
  3. `[ 💧 মাটি / বন্যা ]` (`/soil-irrigation` or `/flood-hazard` based on region)
  4. `[ 🗺 মানচিত্র ]` (`/map` — lazy-loaded)
  5. `[ ℹ তথ্য ]` (`/help`)
- **States**: Inactive (`--color-text-muted`), Active (`--color-brand-primary` + bold label + 2px top indicator bar).
- **Ergonomics**: Fixed to bottom viewport; height 64px; touch targets 64x48px.
- **Responsive Adaptation**: On screens $\ge 640\text{px}$, transitions to a top tab bar or desktop header.

---

### 2.4 Component: Primary & Secondary Action Buttons (`CMP-ACT-01`)
- **Purpose**: User-triggered operational actions (e.g., Share Advisory, Confirm Stage, Retry).
- **Variants**:
  - `btn-primary`: Background `--color-brand-primary`; text `#FFF`; height 48px; border-radius 8px.
  - `btn-secondary`: Background `#FFF`; border `1px solid --color-brand-primary`; text `--color-brand-primary`.
  - `btn-share`: Background `#25D366` (WhatsApp Emerald) or brand primary; WhatsApp icon + *"পরামর্শ শেয়ার করুন"*.
- **States**: Default, Hover, Pressed (`transform: scale(0.98)`), Focused (`outline: 2px solid --color-focus-ring`), Disabled (`--color-control-disabled`).

---

### 2.5 Component: Crop Growth Stage Selector Chips (`CMP-INP-01`)
- **Purpose**: Enables farmers and SAAOs to confirm active phenology in $\le 1$ tap to satisfy context gating (`DEC-17`).
- **Anatomy**: Horizontal flex wrap container with 5 toggle chips:
  - `[ চারা/কুশি ]` `[ থোড় পর্যায় ]` `[ ফুল ফোটা ]` `[ দানা গঠন ]` `[ পাকা ধান ]`
- **States**:
  - Inactive: Background `#FFF`; border `1px solid --color-border-default`; text `--color-text-secondary`.
  - Active: Background `--primitive-green-100`; border `2px solid --color-brand-primary`; text `--color-brand-primary`; bold font.
- **Accessibility**: Implemented as `<fieldset>` with semantic `<input type="radio">` hidden visually.

---

### 2.6 Component: 48-Hour Precipitation Probability Bar (`CMP-VIZ-01`)
- **Purpose**: Visualizes upcoming 3-hour rainfall forecast blocks on `PAGE-02`.
- **Anatomy**:
  - Horizontal block sequence: Time label (`দুপুর ১২টা`) $\to$ Vertical rain probability bar (%) $\to$ Estimated amount (`১৮ মিমি`).
  - Bar height proportional to precipitation probability ($0\%–100\%$).
- **Accessibility**: Screen reader invisible data table (`sr-only`) detailing the exact hourly values.

---

### 2.7 Component: Semi-Circular Soil Moisture Deficit Gauge (`CMP-VIZ-02`)
- **Purpose**: Visualizes root-zone water balance ($D_t$ vs $RAW$) for Barind irrigation.
- **Anatomy**:
  - Semi-circular vector arc divided into 3 color segments:
    - Green segment: $0 \to RAW$ (পর্যাপ্ত রস / Safe).
    - Amber segment: Approaching critical deficit.
    - Red segment: Beyond $RAW$ (সেচ প্রয়োজন / Stressed).
  - Physical needle indicating current $D_t$ value.
  - Center text displaying: *"বর্তমান ঘাটতি: ১৮ মিমি (নিরাপদ সীমা: ২৮ মিমি)"*.

---

### 2.8 Component: Slide-Up Bottom Drawer (`CMP-MOD-01`)
- **Purpose**: Contextual overlays for data provenance, explainability ("কেন এই পরামর্শ?"), and location search.
- **Behavior**: Slides smoothly up from bottom viewport (`transform: translateY(0)`, duration 250ms).
- **Dismissal**: Drag handle at top; explicit "বন্ধ করুন" (Close) button; backdrop tap; ESC key. Focus trapped inside drawer.

---

### 2.9 Component: Automated Suppression Fallback Banner (`CMP-ALT-01`)
- **Purpose**: Upholds the `DEC-10` safety mandate when forecasts are stale (>36h) or ensemble spread >50%.
- **Anatomy**:
  - Amber border (`2px solid --color-status-warning-border`) and warm tint background (`--color-status-warning-bg`).
  - Icon: Prominent warning triangle `[⚠️]`.
  - Title: **"স্বয়ংক্রিয় পরামর্শ সাময়িকভাবে স্থগিত"**.
  - Body: Plain explanation of forecast volatility + mandatory reminder to inspect field moisture manually.
- **Behavior**: Completely supplants the standard Tier 4 actionable recommendation card.
