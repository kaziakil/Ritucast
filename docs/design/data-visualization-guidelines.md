# Ritucast Data Visualization Guidelines

## 1. Executive Summary & Agronomic Visualization Principles

Ritucast's data visualization system transforms multi-source environmental data (satellite observations, numerical weather predictions, soil water balance calculations) into immediate operational clarity.

### Core Principles
1. **Never Truncate Axes Misleadingly**: Rainfall and soil moisture bars must always anchor to zero.
2. **Never Compare Apples to Oranges**: Never plot variables with different units, spatial resolutions, or temporal integration periods on a single confusing multi-axis graph.
3. **Always Accompany Visuals with Semantic Tables**: In adherence to accessibility standards, every SVG chart or canvas gauge must be backed by an accessible semantic HTML table (`sr-only`) detailing the exact numerical series.
4. **Coarse Resolution Transparency**: Maps and spatial grids must visually indicate their spatial granularity (e.g., 10km grid cells) to prevent false assumptions of sub-acre precision (`RSK-03`).

---

## 2. Visualization Standards by Environmental Indicator

---

### 2.1 48-Hour Precipitation Probability & Volume Chart
- **Visual Form**: Combined 3-Hour Interval Precipitation Bar + Volume Pill.
- **Visual Encoding**:
  - Horizontal axis: 3-hour time blocks (e.g., `সকাল ৬টা`, `সকাল ৯টা`, `দুপুর ১২টা`, `বিকাল ৩টা`...).
  - Primary bar height: **Rainfall Probability (%)** ($0\%–100\%$) rendered in cyan-blue (`--primitive-sky-500`).
  - Text badge above bar: Expected precipitation volume in millimeters (e.g., `১৮ মিমি` in `--color-brand-sky`).
  - Baseline: Fixed at $0\%$.
- **Uncertainty Band**: When NWP multi-model ensemble spread is elevated ($>30\%$), render a hatched vertical error band indicating the spread range between GFS and ECMWF.
- **Screen Reader Fallback**:
  ```html
  <table class="sr-only">
    <caption>৪৮ ঘণ্টার বৃষ্টিপাতের পূর্বাভাস সারণি</caption>
    <thead><tr><th>সময়</th><th>সম্ভাবনা</th><th>পরিমাণ</th></tr></thead>
    <tbody><tr><td>দুপুর ১২টা</td><td>৭০%</td><td>১৮ মিমি</td></tr></tbody>
  </table>
  ```

---

### 2.2 Temperature & Thermal Stress Line Chart
- **Visual Form**: Dual continuous line chart (Maximum & Minimum Daily Temperatures).
- **Visual Encoding**:
  - Top Line (Max Temp): Coral Red (`#DC2626`) with solid circular point markers ($4\text{px}$).
  - Bottom Line (Min Temp): Cobalt Blue (`#2563EB`) with hollow point markers.
  - Shaded Reference Band: Optimal Boro Rice vegetative range ($22^\circ\text{C}–30^\circ\text{C}$) shaded in very faint green tint.
  - Critical Stress Line: Horizontal dashed line at **$35^\circ\text{C}$** labeled `তাপমাত্রা ঝুঁকি সীমা (Heat Stress Threshold)`.

---

### 2.3 Barind Root-Zone Soil Water Deficit Semi-Circular Dial (`CMP-VIZ-02`)
- **Visual Form**: 180-Degree Semi-Circular Dial Gauge comparing current depletion ($D_t$) against Readily Available Water ($RAW$).
- **Visual Encoding**:
  - Arc Radius: $120\text{px}$; stroke width $14\text{px}$.
  - Segment 1 ($0 \to RAW$, e.g., $0–28\text{mm}$): Emerald Green (`--primitive-green-700`) labeled *"পর্যাপ্ত রস"*.
  - Segment 2 ($RAW \to TAW$, e.g., $28–56\text{mm}$): Crimson Red (`--primitive-red-700`) labeled *"সেচ প্রয়োজন"*.
  - Indicator Needle: Sharp black triangle pointer indicating active depletion value (e.g., $18\text{mm}$).
  - Center Typography: Bold $24\text{px}$ text showing: **১৮ মিমি / ২৮ মিমি**.

---

### 2.4 Haor Composite Flash Flood Threat Gauge ($I_{\text{flood}}$)
- **Visual Form**: 3-Segment Stepped Threat Meter (`DEC-16`).
- **Visual Encoding**:
  - Stepped horizontal progress bar divided into 3 distinct status zones:
    1. **স্বাভাবিক (Normal: $0.00–0.49$)**: Green fill + `[✓]` glyph.
    2. **সতর্কবার্তা (Watch: $0.50–0.74$)**: Amber fill + `[⚠️]` glyph.
    3. **জরুরি সতর্কতা (Emergency Alert: $0.75–1.00$)**: Red fill + `[🚨]` glyph.
  - Physical Value Callout: Below the bar, display the contributing components in a 3-item sub-card row:
    - মেঘালয় বৃষ্টি: `১৪০ মিমি` (বিপদসীমা $\ge ১০০$ মিমি)
    - সুরমা নদী বৃদ্ধি: `+০.৭০ মি/২৪ঘণ্টা`
    - রাডার প্লাবিত এলাকা: `১২%`

---

## 3. Geospatial Map Visualization Guidelines

Detailed standards for the lazy-loaded `PAGE-04: মানচিত্র ও বিশ্লেষণ` view ([ADR-06](file:///Users/kazi/Projects/RITUCAST/docs/architecture/decisions/ADR-06-maplibre-vector-maps.md)):

### 3.1 Administrative Boundaries & Centering
- **Vector Boundaries**: Upazila administrative polygons styled with clean 1.5px slate borders (`#64748B`).
- **Active Pilot Upazilas**: Highlighted with an emerald boundary (`2px solid --color-brand-primary`) and semi-transparent fill (`rgba(21, 128, 61, 0.08)`).
- **Selected Area Focus**: Tapping an Upazila fits bounds with a smooth zoom transition ($150\text{ms}$).

### 3.2 Raster Overlay Styling
- **Precipitation Heatmap**: Standard meteorological blue-cyan ramp with discrete color stops ($0, 10, 25, 50, 100\text{ mm}$).
- **Sentinel-1 SAR Surface Water**: High-contrast cobalt blue polygons (`#1D4ED8`) overlaid on muted topographic terrain.
- **Discrete Legend Overlay**: Always visible in bottom-left corner of the map canvas, indicating units, color stops, and grid cell size (e.g., *"প্রতিটি গ্রিড ১০x১০ কিমি"*).

### 3.3 Coarse Resolution Disclaimer
- A permanent translucent banner anchors to the top of the map container:
  > *"⚠️ বিজ্ঞপ্তি: স্যাটেলাইট উপাত্ত পুরো উপজেলার সামগ্রিক প্রবণতা (১০ কিমি গ্রিড) প্রদর্শন করে; এটি একক জমির প্লট পরিমাপ নয়।"*
