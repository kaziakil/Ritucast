# Ritucast Typography System Specification

## 1. Executive Summary & Bilingual Strategy

Typography in Ritucast is engineered for two critical constraints:
1. **Flawless Bangla Unicode Rendering**: Complex conjuncts (*যুক্তাক্ষর* like ক্ষ, ষ্ণ, ঙ্গ, ণ্ড) must render crisply without letter clipping or baseline distortion across older Android WebViews (Android 8+).
2. **Tabular Metric Clarity**: Numerical measurements (e.g., $18.5\text{ MJ/m}^2$, $45\text{ mm}$, $6.85\text{ m}$) must feature fixed-width tabular alignment to prevent layout shifting during data refresh.

---

## 2. Font Family Stack

```css
/* Bangla Primary Font Stack */
--font-family-bangla: 'Hind Siliguri', 'Noto Sans Bengali', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Tabular & Numerical Font Stack */
--font-family-mono: 'JetBrains Mono', 'Roboto Mono', ui-monospace, monospace;

/* Fallback Latin Heading Stack */
--font-family-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif;
```

### Font Selection Rationale
- **Primary: Hind Siliguri & Noto Sans Bengali**:
  - Open-source Google Fonts with full open SIL Open Font Licenses.
  - Highly optimized for on-screen legibility at small sizes ($12\text{px}–14\text{px}$).
  - Open-source, lightweight WOFF2 subsets ($\le 38\text{KB}$ per weight), keeping client bundle size well within the $\le 1.5\text{MB}$ limit (`DEC-09`).
- **Tabular Figures (`tnum`)**:
  - The font stack enables OpenType tabular numbers (`font-variant-numeric: tabular-nums`) so that numbers in meteorological tables align vertically along decimal points.

---

## 3. Typographic Scale and Hierarchy

| Token Name | Intended Use / UI Context | Font Size | Font Weight | Line Height | Mobile Scaling |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `--font-size-display` | Primary Hero Advisory Status (e.g., সেচ দিন / স্থগিত) | **$28\text{px}$** ($1.75\text{rem}$) | Bold ($700$) | $36\text{px}$ ($1.28$) | $24\text{px}$ ($1.5\text{rem}$) |
| `--font-size-h1` | Main Page Title (`PAGE-01` to `05`) | **$22\text{px}$** ($1.375\text{rem}$) | Bold ($700$) | $30\text{px}$ ($1.36$) | $20\text{px}$ ($1.25\text{rem}$) |
| `--font-size-h2` | Section Titles & Module Headings | **$18\text{px}$** ($1.125\text{rem}$) | Semi-Bold ($600$)| $26\text{px}$ ($1.44$) | $17\text{px}$ ($1.06\text{rem}$) |
| `--font-size-h3` | Card Headers & Metric Titles | **$16\text{px}$** ($1.0\text{rem}$) | Semi-Bold ($600$)| $24\text{px}$ ($1.50$) | $15\text{px}$ ($0.94\text{rem}$) |
| `--font-size-body` | Primary Explanatory Paragraphs & Guidance Copy | **$15\text{px}$** ($0.9375\text{rem}$) | Regular ($400$)| $24\text{px}$ ($1.60$) | $14\text{px}$ ($0.875\text{rem}$) |
| `--font-size-body-bold` | Key Guidance Highlights & Form Labels | **$15\text{px}$** ($0.9375\text{rem}$) | Medium ($500$) | $24\text{px}$ ($1.60$) | $14\text{px}$ ($0.875\text{rem}$) |
| `--font-size-caption` | Supporting Text, Field-Check Alerts, Dropdown Options | **$13\text{px}$** ($0.8125\text{rem}$) | Regular ($400$)| $18\text{px}$ ($1.38$) | $13\text{px}$ ($0.8125\text{rem}$) |
| `--font-size-meta` | Data Provenance, Timestamps, Source Citations, Units | **$12\text{px}$** ($0.75\text{rem}$) | Regular ($400$)| $16\text{px}$ ($1.33$) | $12\text{px}$ ($0.75\text{rem}$) |

---

## 4. Specialized Agricultural Number and Unit Formatting

### 4.1 Numerical Metric Blocks
For high-importance environmental numbers (e.g., rainfall volume `৪৫ মিমি`, temperature `২৮° সে`):
```css
.metric-value-large {
  font-family: var(--font-family-bangla);
  font-size: 32px;
  font-weight: 700;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
  color: var(--color-text-primary);
}

.metric-unit {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-muted);
  margin-left: 4px;
}
```

### 4.2 Minimum Legibility Floor
- In adherence to accessibility standards, **no text on the platform may ever be smaller than $12\text{px}$**.
- Critical uncertainty and data suppression notices must remain at **$\ge 14\text{px}$** with **$1.5$ line-height** to prevent accidental misinterpretation by older farmers.

---

## 5. Line-Height & Readability Rules for Bangla

1. **Bangla Requires Taller Line Heights**:
   - Unlike Latin characters, Bangla script includes high ascending diacritics (*ই-কার, রেফ*) and deep descending vowel marks (*উ-কার, ঋ-কার*).
   - Standard Latin line heights ($1.2–1.3$) cause vertical collision of Bangla diacritics.
   - Ritucast strictly enforces a line height of **$\ge 1.5$** for all body paragraphs and **$\ge 1.3$** for headings.
2. **No Justified Text**:
   - All body text is left-aligned (`text-align: left`). Fully justified Bangla text generates severe, unnatural word gaps and breaks visual cadence.
3. **Hyphenation Disabled**:
   - CSS hyphenation (`hyphens: none`) is strictly enforced to prevent automated line-breaks within complex Bangla conjunct words.
