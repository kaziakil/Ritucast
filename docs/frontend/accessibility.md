# Frontend Accessibility Compliance (WCAG 2.2 AA)

## 1. Compliance Target

Ritucast is built in compliance with **WCAG 2.2 AA standards**, ensuring equitable access for rural farmers, low-literacy users, and individuals with visual impairments or motor limitations.

---

## 2. Implemented Accessibility Features

### 2.1 Keyboard Navigation & Focus Indicators
- **Logical Tab Order**: All interactive controls (`<button>`, `<select>`, `<a>`) follow natural visual reading order.
- **Visible Focus Rings**: Custom focus rings implemented via `:focus-visible` token (`--color-focus-ring`: `rgba(21, 128, 61, 0.4)` with 3px solid border and 2px offset).
- **Skip Navigation**: Accessible header landmarks and structured `<main>` containers enable screen-reader jumps.

### 2.2 Semantic HTML & ARIA Attributes
- **Landmarks**: `<header className="app-header">`, `<nav aria-label="Main Navigation">`, `<section aria-label="Context Selection">`, `<main>`, `<footer>`.
- **Form Association**: Explicit `<label htmlFor="...">` attributes linked directly to `<select id="...">` elements.
- **Live Regions & Statuses**:
  - `role="alert"` for the automated suppression alert banner (`DEC-10`).
  - `aria-current="page"` for the actively selected tab in navigation.
  - `aria-busy="true"` and `data-testid="advisory-loading-skeleton"` on dynamic loading containers.

### 2.3 Contrast & Color Independence
- **Strict Color Independence**: Risk levels and advisory severities never rely solely on color. Every indicator includes:
  - Text label in Bangla (e.g., "সতর্কবার্তা", "জরুরি", "স্বাভাবিক").
  - Distinct SVG icon (e.g., AlertTriangle, AlertOctagon, CheckCircle2).
  - Explicit numerical percentage or index score.
- **Contrast Ratios**:
  - Primary text on cards: `#0f172a` on `#ffffff` ($\ge 14:1$).
  - Brand green on white: `#15803d` on `#ffffff` ($\ge 4.8:1$).
  - Amber warning text: `#92400e` on `#fef3c7` ($\ge 5.2:1$).
  - Crimson emergency text: `#b91c1c` on `#fee2e2` ($\ge 5.6:1$).

### 2.4 Reduced Motion
- `@media (prefers-reduced-motion: reduce)` overrides disable all card transitions, pulsing skeletons, and progress bar animations, providing instant layout updates.
