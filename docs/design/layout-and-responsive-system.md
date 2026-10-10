# Ritucast Layout, Spacing, and Responsive System

## 1. Executive Summary & Design Foundations

Ritucast follows a **Mobile-First 8-Point Grid System** specifically tuned for budget Android smartphones (360px–420px viewports) while scaling cleanly to tablet and desktop monitors.

### Architectural Rules Enforced
1. **8pt Grid Consistency**: All layout dimensions, margins, paddings, and component heights align to an 8-point base grid (with a 4-point sub-grid for compact micro-badges).
2. **Sharp Borders Over Heavy Shadows**: In intense direct sunlight, soft CSS box-shadows wash out completely. Ritucast relies on crisp 1px solid borders (`var(--color-border-default)`) for card separation, using elevation shadows solely for floating overlays and bottom navigation.
3. **48px Physical Touch Target Floor (WCAG 2.2 SC 2.5.8)**: All primary interactive controls must satisfy a minimum hit area of **$48 \times 48\text{px}$** with at least **$8\text{px}$** of physical separation.

---

## 2. Spacing Scale Tokens

```css
:root {
  --spacing-2xs: 2px;   /* Micro-indicators, border offsets */
  --spacing-xs:  4px;   /* Badge internal padding, icon-text gap */
  --spacing-sm:  8px;   /* Chip padding, compact list gap */
  --spacing-md:  12px;  /* Micro-card padding, card inner margins */
  --spacing-lg:  16px;  /* Standard mobile screen margin & card padding */
  --spacing-xl:  24px;  /* Section separation, desktop column gap */
  --spacing-2xl: 32px;  /* Major page header spacing */
  --spacing-3xl: 48px;  /* Hero landmark margins */
}
```

---

## 3. Responsive Breakpoints

| Breakpoint Name | Media Query Range | Primary Target Devices | Layout Geometry |
| :--- | :--- | :--- | :--- |
| **`compact-sm`** | $< 360\text{px}$ | Legacy/budget Android (Walton, Symphony 4.5") | Single-column; 12px screen padding; tight font scaling. |
| **`compact-md`** (Default) | $360\text{px}–639\text{px}$ | Standard budget smartphones (Xiaomi, Samsung 2GB RAM) | Single-column stacked cards; 16px screen padding; bottom nav. |
| **`medium`** | $640\text{px}–1023\text{px}$| Android tablets (used by DAE Upazila officers) | 2-Column responsive grid; persistent top-tab nav; 24px padding. |
| **`expanded`** | $\ge 1024\text{px}$ | Desktop workstations (DAE headquarters, researchers) | 3-Column dashboard; max-width $1200\text{px}$; side navigation drawer. |

---

## 4. Container Width & Screen Padding

```css
:root {
  --container-max-mobile: 480px;   /* Optimal reading column on mobile */
  --container-max-desktop: 1200px; /* Maximum content width on desktop */
  --page-padding-mobile: 16px;     /* Screen horizontal padding on mobile */
  --page-padding-desktop: 32px;    /* Screen horizontal padding on desktop */
}
```
- On mobile ($<640\text{px}$), the container expands to 100% width minus `--page-padding-mobile` (16px on left and right).
- On desktop ($\ge 1024\text{px}$), the layout centers within `--container-max-desktop` (1200px) with auto margins.

---

## 5. Border-Radius and Elevation Tokens

### 5.1 Border-Radius Scale
```css
:root {
  --radius-xs:   4px;    /* Small data tags, status indicators */
  --radius-sm:   6px;    /* Action chips, dropdown menus */
  --radius-md:   8px;    /* Standard cards, input fields, buttons */
  --radius-lg:   12px;   /* Hero recommendation card, slide-up sheets */
  --radius-xl:   16px;   /* Modal dialogs, bottom sheets */
  --radius-pill: 9999px; /* Status pills, toggle switches */
}
```

### 5.2 Elevation & Shadow Scale (Outdoor Tuned)
```css
:root {
  /* Flat border card (Primary style for outdoor sunlight) */
  --shadow-none: none;
  --border-card: 1px solid var(--color-border-default);

  /* Subtle card elevation (indoor/desktop) */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);

  /* Dropdown & chip modal elevation */
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);

  /* Floating Bottom Navigation & Modals */
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
```

---

## 6. Responsive Adaptation Rules for Core Components

### 6.1 Standard 5-Section Advisory Card
- **Mobile ($<640\text{px}$)**: Full-width stacked element; 16px internal padding; vertical action button row.
- **Desktop ($\ge 1024\text{px}$)**: 2-Column split inside card: Left side features the bold operational status badge and plain Bangla advice; Right side features the economic benefit pill, share button, and field-check reminder.

### 6.2 Data Tables and Hourly Precipitation Blocks
- **Mobile**: Horizontal scroll container with scroll snap (`overflow-x: auto; scroll-snap-type: x mandatory`). Never truncate table columns or wrap numbers awkwardly.
- **Desktop**: Full tabular grid with visible column headers and fixed decimal alignment.

### 6.3 Map Container Resizing (`ADR-06`)
- **Mobile**: Fixed height at `60vh` with bottom sheet overlay for active polygon zonal statistics. Map controls located at top-right with minimum 48px hit areas.
- **Desktop**: Expands to `calc(100vh - 120px)` with a persistent 360px left sidebar displaying Upazila zonal statistics.
