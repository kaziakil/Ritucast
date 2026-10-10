# Frontend Design System & Visual Standards

## 1. Design System Philosophy

The Ritucast Design System is engineered to balance modern visual aesthetics with strict field practicalities. In accordance with `[design-tokens.md](file:///Users/kazi/Projects/RITUCAST/docs/design/design-tokens.md)` and `DEC-20`, styling is implemented purely through **Vanilla CSS Custom Properties** in `[index.css](file:///Users/kazi/Projects/RITUCAST/frontend/src/index.css)`, eliminating runtime CSS overhead while optimizing readability under direct tropical sunlight.

---

## 2. Color Palette & Semantic Tokens

### 2.1 Primitive Color Scale
```css
/* Brand Emerald / Agriculture Palette */
--primitive-green-50:  #f0fdf4;
--primitive-green-100: #dcfce7;
--primitive-green-600: #16a34a;
--primitive-green-700: #15803d;  /* Master Brand Color */
--primitive-green-800: #166534;
--primitive-green-900: #14532d;

/* Sky / Hydrology Palette */
--primitive-sky-50:    #f0f9ff;
--primitive-sky-100:   #e0f2fe;
--primitive-sky-700:   #0369a1;
--primitive-sky-900:   #0c4a6e;

/* Amber / Warning Palette */
--primitive-amber-50:  #fffbeb;
--primitive-amber-100: #fef3c7;
--primitive-amber-600: #d97706;
--primitive-amber-800: #92400e;

/* Crimson / Emergency Palette */
--primitive-red-50:    #fef2f2;
--primitive-red-100:   #fee2e2;
--primitive-red-600:   #dc2626;
--primitive-red-700:   #b91c1c;
--primitive-red-900:   #7f1d1d;

/* Slate / Neutral Palette */
--primitive-slate-50:  #f8fafc;
--primitive-slate-100: #f1f5f9;
--primitive-slate-200: #e2e8f0;
--primitive-slate-600: #475569;
--primitive-slate-700: #334155;
--primitive-slate-900: #0f172a;
```

### 2.2 Semantic Information Tiers (`DEC-08`)
| Tier Level | Name | Theme Border | Background Token | Badge Styling |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | Empirical Observations | `#0284c7` (Sky) | `var(--primitive-sky-50)` | Blue pill badge |
| **Tier 2** | Derived Indicators | `#059669` (Teal) | `var(--primitive-green-50)` | Green pill badge |
| **Tier 3** | Probabilistic Forecasts | `#7c3aed` (Purple)| `#f5f3ff` | Purple pill badge |
| **Tier 4** | Actionable Advisories | `#15803d` (Brand) | `#ffffff` | Brand green / Amber severity border |

---

## 3. Typography Hierarchy

The typography system pairs **Hind Siliguri** (Google Fonts) for native Bangla text rendering with **Inter** for Latin technical identifiers and units, and **JetBrains Mono** for numerical values and coordinate strings.

| Token | Size | Line Height | Weight | Typical Element |
| :--- | :--- | :--- | :--- | :--- |
| `--font-size-h1` | 1.85rem (29.6px) | 1.25 | 700 Bold | Page / Hub Major Headlines |
| `--font-size-h2` | 1.40rem (22.4px) | 1.30 | 700 Bold | Section / Card Titles |
| `--font-size-h3` | 1.15rem (18.4px) | 1.35 | 600 SemiBold | Sub-card Headings |
| `--font-size-body` | 1.00rem (16.0px) | 1.55 | 400 Regular | Paragraph Text & Explanations |
| `--font-size-caption`| 0.85rem (13.6px) | 1.45 | 500 Medium | Metric Labels & Footnotes |
| `--font-size-meta` | 0.75rem (12.0px) | 1.40 | 600 SemiBold | Provenance Badges & Timestamps |

---

## 4. Outdoor High-Contrast & Sunlight Readability

To accommodate farmers reading advisories on smartphone screens in bright open rice paddies:
1. **WCAG 2.2 AA Contrast Standards**: All text elements meet at least 4.5:1 contrast against their backgrounds; critical headline numbers exceed 7:1.
2. **Elevation & Shadowing**: Uses outdoor-calibrated double-layer drop shadows (`--shadow-card`, `--shadow-lg`) providing distinct card boundaries even when screen brightness is diminished.
3. **No Decorative Ambiguity**: Visual cards avoid low-contrast grey-on-white text, faint borders, or complex blurred backdrops that wash out under sunlight.

---

## 5. Mobile Ergonomics & Touch Targets

- **48px Minimum Touch Target**: Buttons, selects, and tab toggles enforce a minimum height of 48px (`--touch-target-min`) for easy thumb activation with wet or soiled fingers.
- **Sticky Context Header**: The Upazila, Crop, and Stage bar sticks cleanly beneath the top navigation bar with a z-index of 90, maintaining immediate context during long vertical scrolling.
- **Card Spacing Grid**: Uses an 8pt base grid (`--spacing-xs` = 4px, `--spacing-sm` = 8px, `--spacing-md` = 16px, `--spacing-lg` = 24px, `--spacing-xl` = 32px).
