# Ritucast Master Design Tokens Specification

## 1. Executive Summary & Token Architecture

This specification establishes the official design token architecture for Ritucast, formatted as native **Vanilla CSS Custom Properties** (`:root`) adhering strictly to [ADR-03](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-03-react-typescript-vanilla-css.md) and [DEC-20](file:///Users/kazi/Projects/RITUCAST/docs/planning/decision-log.md).

### 2-Tier Token Hierarchy
```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Foundational Primitive Tokens (Raw Scales: Green-700, Gray-900, etc)│
├────────────────────────────────────────────────────────────────────────┤
│ 2. Semantic Contextual Tokens (Functional: --color-brand-primary, etc) │
└────────────────────────────────────────────────────────────────────────┘
```
All UI components, cards, and pages must strictly consume **Semantic Tokens**, never hardcoding raw hex values or ad-hoc pixel values.

---

## 2. Complete CSS Custom Properties Code Blueprint

```css
/* ==========================================================================
   Ritucast Design System: Master Design Tokens (index.css)
   ========================================================================== */

:root {
  /* ------------------------------------------------------------------------
     1. Foundational Color Primitives
     ------------------------------------------------------------------------ */
  --primitive-green-900: #14532D;
  --primitive-green-800: #166534;
  --primitive-green-700: #15803D;
  --primitive-green-600: #16A34A;
  --primitive-green-100: #DCFCE7;
  --primitive-green-50:  #F0FDF4;

  --primitive-slate-900: #0F172A;
  --primitive-slate-800: #1E293B;
  --primitive-slate-700: #334155;
  --primitive-slate-500: #64748B;
  --primitive-slate-200: #E2E8F0;
  --primitive-slate-100: #F1F5F9;

  --primitive-amber-800: #92400E;
  --primitive-amber-700: #B45309;
  --primitive-amber-600: #D97706;
  --primitive-amber-100: #FEF3C7;
  --primitive-amber-50:  #FFFBEB;

  --primitive-red-800:   #991B1B;
  --primitive-red-700:   #B91C1C;
  --primitive-red-600:   #DC2626;
  --primitive-red-100:   #FEE2E2;
  --primitive-red-50:    #FEF2F2;

  --primitive-sky-700:   #0369A1;
  --primitive-sky-600:   #0284C7;
  --primitive-sky-500:   #0EA5E9;
  --primitive-sky-100:   #E0F2FE;

  --primitive-neutral-950: #030712;
  --primitive-neutral-900: #111827;
  --primitive-neutral-700: #374151;
  --primitive-neutral-500: #6B7280;
  --primitive-neutral-300: #D1D5DB;
  --primitive-neutral-200: #E5E7EB;
  --primitive-neutral-50:  #F9FAFB;
  --primitive-white:       #FFFFFF;

  /* ------------------------------------------------------------------------
     2. Semantic Colors (Surfaces & Backgrounds)
     ------------------------------------------------------------------------ */
  --color-bg-canvas:        #F8FAF8;
  --color-bg-surface:       var(--primitive-white);
  --color-bg-subtle:        var(--primitive-slate-100);
  --color-bg-card-hover:    var(--primitive-neutral-50);

  /* ------------------------------------------------------------------------
     3. Semantic Colors (Text & Typography)
     ------------------------------------------------------------------------ */
  --color-text-primary:     var(--primitive-neutral-900);
  --color-text-secondary:   var(--primitive-neutral-700);
  --color-text-muted:       var(--primitive-slate-500);
  --color-text-inverse:     var(--primitive-white);

  /* ------------------------------------------------------------------------
     4. Semantic Colors (Brand & Accents)
     ------------------------------------------------------------------------ */
  --color-brand-primary:       var(--primitive-green-700);
  --color-brand-primary-hover: var(--primitive-green-800);
  --color-brand-secondary:     var(--primitive-slate-900);
  --color-brand-accent:        var(--primitive-amber-600);
  --color-brand-sky:           var(--primitive-sky-600);

  /* ------------------------------------------------------------------------
     5. Semantic Colors (Borders & Dividers)
     ------------------------------------------------------------------------ */
  --color-border-default:   var(--primitive-neutral-200);
  --color-border-strong:    var(--primitive-neutral-500);
  --color-divider:          var(--primitive-slate-200);

  /* ------------------------------------------------------------------------
     6. Semantic Status & Risk Colors
     ------------------------------------------------------------------------ */
  --color-status-success:      var(--primitive-green-800);
  --color-status-success-bg:   var(--primitive-green-50);
  --color-status-success-border: var(--primitive-green-600);

  --color-status-warning:      var(--primitive-amber-700);
  --color-status-warning-bg:   var(--primitive-amber-50);
  --color-status-warning-border: var(--primitive-amber-600);

  --color-status-critical:     var(--primitive-red-700);
  --color-status-critical-bg:  var(--primitive-red-50);
  --color-status-critical-border: var(--primitive-red-600);

  --color-status-info:         var(--primitive-sky-700);
  --color-status-info-bg:      var(--primitive-sky-100);
  --color-status-info-border:  var(--primitive-sky-500);

  --color-status-neutral:      var(--primitive-slate-700);
  --color-status-neutral-bg:   var(--primitive-slate-100);

  /* ------------------------------------------------------------------------
     7. Interactive & Focus Tokens
     ------------------------------------------------------------------------ */
  --color-focus-ring:          var(--primitive-sky-600);
  --color-control-disabled:    var(--primitive-neutral-300);
  --color-control-disabled-text: var(--primitive-slate-500);

  /* ------------------------------------------------------------------------
     8. Typography Scale
     ------------------------------------------------------------------------ */
  --font-family-bangla: 'Hind Siliguri', 'Noto Sans Bengali', -apple-system, sans-serif;
  --font-family-mono:   'JetBrains Mono', 'Roboto Mono', ui-monospace, monospace;

  --font-size-display: 1.75rem;   /* 28px */
  --font-size-h1:      1.375rem;  /* 22px */
  --font-size-h2:      1.125rem;  /* 18px */
  --font-size-h3:      1.0rem;    /* 16px */
  --font-size-body:    0.9375rem; /* 15px */
  --font-size-caption: 0.8125rem; /* 13px */
  --font-size-meta:    0.75rem;   /* 12px */

  --font-weight-regular: 400;
  --font-weight-medium:  500;
  --font-weight-semibold: 600;
  --font-weight-bold:    700;

  --line-height-display: 1.28;
  --line-height-heading: 1.35;
  --line-height-body:    1.60;
  --line-height-caption: 1.38;

  /* ------------------------------------------------------------------------
     9. Spacing Scale (8pt grid)
     ------------------------------------------------------------------------ */
  --spacing-2xs: 2px;
  --spacing-xs:  4px;
  --spacing-sm:  8px;
  --spacing-md:  12px;
  --spacing-lg:  16px;
  --spacing-xl:  24px;
  --spacing-2xl: 32px;
  --spacing-3xl: 48px;

  /* ------------------------------------------------------------------------
     10. Physical Touch Target & Ergonomics
     ------------------------------------------------------------------------ */
  --touch-target-min: 48px;

  /* ------------------------------------------------------------------------
     11. Border Radius Scale
     ------------------------------------------------------------------------ */
  --radius-xs:   4px;
  --radius-sm:   6px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-xl:   16px;
  --radius-pill: 9999px;

  /* ------------------------------------------------------------------------
     12. Elevation & Shadows (Outdoor Tuned)
     ------------------------------------------------------------------------ */
  --shadow-none: none;
  --shadow-sm:   0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md:   0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg:   0 10px 15px -3px rgba(0, 0, 0, 0.1);

  /* ------------------------------------------------------------------------
     13. Motion & Animation Timings (Reduced-Motion Aware)
     ------------------------------------------------------------------------ */
  --duration-fast:   150ms;
  --duration-normal: 250ms;
  --ease-standard:   cubic-bezier(0.4, 0, 0.2, 1);
}

/* Reduced Motion Override (WCAG 2.2 SC 2.3.3) */
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast:   0ms;
    --duration-normal: 0ms;
  }
}
```

---

## 3. Implementation Handoff Rules for Phase 11
1. **Zero External Stylesheet Bloat**: All tokens are declared in the root stylesheet `index.css`.
2. **Payload Target**: The complete compiled CSS stylesheet containing all tokens and utility classes will measure **$< 45\text{KB}$ uncompressed**, comfortably respecting the performance budget (`DEC-09`).
