# Ritucast Design System Accessibility Standards (WCAG 2.2 Level AA)

## 1. Executive Summary & Compliance Target

The Ritucast Design System enforces strict compliance with **WCAG 2.2 Level AA** accessibility standards.

Because smallholder farmers and field officers frequently operate devices outdoors in bright tropical sunlight with wet or soiled hands on budget smartphones, accessibility in Ritucast is a core operational requirement, not an optional compliance checkbox.

---

## 2. Accessibility Rules by WCAG 2.2 Criteria

---

### 2.1 Contrast (Minimum & Enhanced) (SC 1.4.3, SC 1.4.11)
- **Normal Text ($\le 18\text{px}$)**: Must achieve at least **$4.5 : 1$** contrast against background.
  - *Ritucast Primary Body*: `--color-text-primary` (`#111827`) on `--color-bg-surface` (`#FFFFFF`) achieves **$16.1 : 1$** (Exceeds AAA).
- **Large Text ($\ge 24\text{px}$ or bold $\ge 18\text{px}$)**: Must achieve at least **$3.0 : 1$** contrast.
- **UI Components & Graphical Objects (SC 1.4.11)**: Interactive control boundaries, radio buttons, and status borders must achieve at least **$3.0 : 1$** contrast against adjacent surfaces.

---

### 2.2 Non-Color-Only Information Architecture (SC 1.4.1)
- **Mandate**: Color must **never** be used as the sole visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element.
- **Implementation**:
  - Every status badge pairs color with an SVG glyph icon and explicit text label:
    - 🟢 Green + `[✓]` + *"পর্যাপ্ত রস / স্বাভাবিক"*
    - 🟡 Amber + `[⚠️]` + *"সেচ প্রয়োজন / সতর্কবার্তা"*
    - 🔴 Red + `[🚨]` + *"জরুরি সতর্কতা / বিপদসীমা"*
  - Multi-model ensemble agreement charts pair color with textual certainty chips (*"আস্থা: উচ্চ / মাঝারি / মতভেদ"*).

---

### 2.3 Physical Touch Targets (SC 2.5.8)
- **Minimum Target Area**: All interactive components (buttons, navigation tabs, location pills, accordion headers) must have a hit area of at least **$48 \times 48\text{px}$**.
- **Target Separation**: Adjacent interactive elements must maintain at least **$8\text{px}$** of visual and physical separation to prevent mis-taps.

---

### 2.4 Focus Appearance & Keyboard Navigation (SC 2.4.7, SC 2.4.11, SC 2.1.1)
- **Focus Indicator**: All focusable elements must display a high-contrast focus ring when navigated via keyboard or directional pad:
  ```css
  :focus-visible {
    outline: 2px solid var(--color-focus-ring); /* #0284C7 (Azure Blue) */
    outline-offset: 2px;
  }
  ```
- **Logical Tab Order**: Navigation strictly follows visual reading order (Top Header $\to$ Main Content $\to$ Bottom Nav).
- **Focus Trapping**: When a slide-up drawer or location modal opens, keyboard focus is trapped inside the overlay until dismissed.

---

### 2.5 Text Resizing & Scalability (SC 1.4.4)
- All font sizes and spacing values are expressed in relative units (`rem`), enabling seamless text scaling up to **$200\%$** via browser zoom without breaking card layouts or truncating text.
- Horizontal scrolling is strictly prevented across all standard viewport widths ($360\text{px}–1200\text{px}$).

---

### 2.6 Accessible Alternatives for Visual Data (SC 1.1.1)
- Every visual chart (48h rainfall probability, temperature line, soil water deficit dial) is programmatically paired with a semantic HTML table:
  ```html
  <figure aria-labelledby="chart-title">
    <div id="chart-title" class="sr-only">৪৮ ঘণ্টার বৃষ্টিপাতের পূর্বাভাসের সারণি</div>
    <!-- Visual SVG Bar Chart (hidden from screen reader) -->
    <svg aria-hidden="true">...</svg>
    
    <!-- Screen Reader Semantic Table -->
    <table class="sr-only">
      <thead><tr><th>সময়</th><th>সম্ভাবনা</th><th>পরিমাণ</th></tr></thead>
      <tbody><tr><td>দুপুর ১২টা</td><td>৭০%</td><td>১৮ মিমি</td></tr></tbody>
    </table>
  </figure>
  ```

---

### 2.7 Screen Reader Context & Bilingual Pronunciation (SC 3.1.2)
- Root HTML tag declares primary language: `<html lang="bn">`.
- Any English metadata or acronyms (e.g., *NASA POWER, Sentinel-1, FAO-56*) are wrapped in `<span lang="en">` to ensure correct speech synthesizer pronunciation.
- Interactive icon-only buttons include descriptive `aria-label` text in Bangla (e.g., `<button aria-label="আজকের পরামর্শ হোয়াটসঅ্যাপে শেয়ার করুন">`).

---

### 2.8 Motion & Flashing Safety (SC 2.3.1, SC 2.3.3)
- **Zero Seizure Hazard**: No visual component flashes more than 3 times in any 1-second period.
- **Prefers-Reduced-Motion**: Mandatory `@media (prefers-reduced-motion: reduce)` collapses all transitions and modal animations to $0\text{ms}$.
