# Responsive Design & Multi-Device Ergonomics

## 1. Responsive Viewport Targets

Ritucast is built mobile-first, targeting the full range of devices prevalent across Bangladesh:
- **Mobile Phones (Primary Target)**: 360px – 480px width (e.g., Symphony, Walton, Samsung Galaxy A-series).
- **Tablets (Extension Officers)**: 768px – 1024px width (e.g., Samsung Galaxy Tab, iPad).
- **Desktops / Laptops (DAE / BMD Command Centers)**: 1280px+ width.

---

## 2. Layout Adaptations

### 2.1 Navigation Bar
- **Desktop**: Horizontal nav links with side-by-side brand mark and live readiness status pill.
- **Mobile**: Sticky header with horizontally scrolling tab navigation bar (`overflow-x: auto`) and touch-friendly padding.

### 2.2 Sticky Context Selection Bar
- **Desktop**: 4-column inline CSS grid (`repeat(auto-fit, minmax(220px, 1fr))`) placing Upazila, Crop, Stage, and Refresh button on a single line.
- **Mobile**: Stacks controls vertically with full-width `<select>` elements and prominent 48px touch targets.

### 2.3 Indicator & Forecast Grids
- **Desktop**: Multi-column responsive cards (`repeat(auto-fit, minmax(280px, 1fr))`).
- **Mobile**: Single-column vertical card stack with 16px lateral padding.

---

## 3. Touch Target Standards

- All interactive controls enforce a minimum physical area of **48px $\times$ 48px** (`--touch-target-min`).
- Dropdown menus utilize native operating system pickers for rapid thumb interaction without pinch-to-zoom glitches.
