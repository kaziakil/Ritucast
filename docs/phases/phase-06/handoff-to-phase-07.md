# Phase 6 to Phase 7 Handoff Specification

## 1. Executive Summary & Purpose

- **From**: Phase 06 — Information Architecture and User Journey Design
- **To**: Phase 07 — Visual Design and Design System
- **Date**: 2026-10-10
- **Status**: **READY FOR PHASE 07 INITIATION**

This document delivers the structural information architecture, component blueprints, accessibility standards, and page requirements established in Phase 6 to the Phase 7 Visual Design team.

The Phase 7 team is tasked with transforming these wireframe-level requirements into a polished, high-contrast, culturally resonant, mobile-first **Design System and Visual Design** using **Vanilla CSS Custom Properties (Design Tokens)** (`ADR-03`, `DEC-20`).

---

## 2. Priority Order for Visual Design Execution

The Phase 7 team should design visual screens and component tokens in the following prioritized order:

1. **Priority 1: Core Design Tokens (`index.css`)**:
   - Color palette tokens (Solar-contrast light theme, semantic status colors).
   - Bangla typography scale (Heading 1 through Caption using Noto Sans Bengali or Hind Siliguri).
   - Spacing, elevation, border-radius, and 48px touch-target tokens.
2. **Priority 2: Standard 5-Section Card Component**:
   - The universal container used for Tier 1 observations, Tier 2 indicators, and Tier 4 recommendations.
3. **Priority 3: `PAGE-01: আজকের পরামর্শ` (Today's Advisory / Overview)**:
   - Primary landing screen; Tier 4 recommendation cards; quick weather snapshot.
4. **Priority 4: `PAGE-02: আবহাওয়া ও পূর্বাভাস` (Weather & 48h Rain Forecast)**:
   - 3-Hour precipitation probability bar chart; multi-model consensus meter.
5. **Priority 5: `PAGE-03A: মাটি ও সেচ` (Barind Soil Water Deficit Gauge)**:
   - Semi-circular root-zone depletion gauge; AWD plastic pipe guide.
6. **Priority 6: `PAGE-03B: বন্যা ও প্লাবন` (Haor Flash Flood Threat Meter)**:
   - 3-Level threat meter ($I_{\text{flood}}$); upstream Meghalaya rainfall card.
7. **Priority 7: Global Header & Bottom Navigation Bar**:
   - Location chip modal, offline sync pill, and 5-item mobile nav bar.

---

## 3. Key Architectural & UX Mandates Governing Visual Design

### 3.1 Strict Styling Technology Mandate (`ADR-03`, `DEC-20`)
- **Technology**: **Vanilla CSS Custom Properties (Design Tokens)**.
- **Strict Prohibition**: **Do NOT use Tailwind CSS**, Bootstrap, or heavy third-party CSS component frameworks.
- **Budget**: Production compiled CSS must remain **$\le 50\text{KB}$ uncompressed** to protect the overall client bundle budget ($\le 1.5\text{MB}$) and ensure Time-to-Interactive $\le 3.5\text{s}$ over 3G.

### 3.2 Four-Tier Visual Taxonomy (`DEC-08`)
The visual design must provide distinct container treatments and category pills for each information tier:
- **Tier 1 (Empirical Observation)**: Neutral slate card border; blue data accent; sub-label: `প্রত্যক্ষ পর্যবেক্ষণ`.
- **Tier 2 (Derived Indicator)**: Subtle primary tint background; teal indicator gauge; sub-label: `হিসাবকৃত সূচক`.
- **Tier 3 (Probabilistic Forecast)**: Dotted or dashed probability band; amber uncertainty pill; sub-label: `পূর্বাভাস মডেল`.
- **Tier 4 (Actionable Recommendation)**: High-contrast solid primary card; bold action badge (🟢 সেচ স্থগিত / 🔴 সেচ দিন / 🚨 জরুরি ধান কর্তন); mandatory field-verification icon `[⚠️]`.

### 3.3 High-Contrast Solar Theme (Sunlight Legibility)
- Farmers read advice outdoors in intense sunlight.
- Pure white background (`#FFFFFF`) or subtle warm off-white (`#F8FAF8`) with deep charcoal text (`#111827`) achieving **$\ge 7:1$ contrast ratio** (exceeding WCAG 2.2 AA).
- Card containers must use sharp borders (`1px solid #E5E7EB`) rather than faint, washed-out drop shadows.

### 3.4 Non-Color-Only Accessibility Mandate (WCAG 2.2 SC 1.4.1)
- Never use green, amber, or red in isolation.
- Every colored badge must contain a distinct glyph icon and explicit text label:
  - Normal / Safe: Green + `[✓]` + *"স্বাভাবিক / পর্যাপ্ত"*
  - Watch / Warning: Amber + `[⚠️]` + *"সতর্কবার্তা"*
  - Emergency / Danger: Red + `[🚨]` + *"জরুরি সতর্কতা"*

### 3.5 Touch Targets (WCAG 2.2 SC 2.5.8)
- All interactive elements must measure at least **$48 \times 48\text{px}$** with minimum 8px padding.

---

## 4. Master Specification Reference Links

The Phase 7 design team must consult these Phase 6 specifications during implementation:
- [UX Design Principles](file:///Users/kazi/Projects/RITUCAST/docs/ux/ux-principles.md)
- [Information Architecture](file:///Users/kazi/Projects/RITUCAST/docs/ux/information-architecture.md)
- [Sitemap Specification](file:///Users/kazi/Projects/RITUCAST/docs/ux/sitemap.md)
- [Critical User Journeys](file:///Users/kazi/Projects/RITUCAST/docs/ux/user-journeys.md)
- [Page Content & Layout Blueprints](file:///Users/kazi/Projects/RITUCAST/docs/ux/page-requirements.md)
- [Geographic Context Model](file:///Users/kazi/Projects/RITUCAST/docs/ux/geographic-context-and-selection.md)
- [Agricultural Insight Model](file:///Users/kazi/Projects/RITUCAST/docs/ux/agricultural-insight-information-model.md)
- [Trust & Uncertainty Patterns](file:///Users/kazi/Projects/RITUCAST/docs/ux/trust-and-uncertainty-patterns.md)
- [Accessibility & Localization](file:///Users/kazi/Projects/RITUCAST/docs/ux/accessibility-localization-and-connectivity.md)
- [Interaction State Matrix](file:///Users/kazi/Projects/RITUCAST/docs/ux/interaction-and-state-specification.md)

---

## 5. Verification Sign-Off

- **Phase 6 Lead**: Approved (Information Architecture & User Journeys Complete)
- **Phase 7 Readiness**: **GREEN (Unblocked — Ready for Design Tokens & Visual Prototyping)**
