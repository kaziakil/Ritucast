# Geographic and Temporal Display Guidelines

## 1. Geographic Scope & Display Conventions

Ritucast is intentionally bound to two validated pilot testbeds in Bangladesh during initial release (`DEC-06`):
1. **High Barind Tract** (AEZ-26):
   - **Godagari** (`BD-50-20-30`, Rajshahi Division)
   - **Tanore** (`BD-50-20-94`, Rajshahi Division)
   - *Primary Agricultural Risk*: Severe groundwater overdraft, drought, deep water table deficit.
2. **Haor Basin** (AEZ-21):
   - **Tahirpur** (`BD-60-90-86`, Sylhet Division)
   - **Sunamganj Sadar** (`BD-60-90-89`, Sylhet Division)
   - *Primary Agricultural Risk*: Pre-monsoon transboundary flash flooding from Meghalaya hills.

### 1.1 Canonical vs Display Identifiers
- Canonical Identifiers: Government BBS GeoCodes (`BD-50-20-30`, `BD-60-90-86`) or lower-case slugs (`godagari`, `tahirpur`).
- Display Identifiers: Fully localized Bangla names with English sub-labels (`গোদাগাড়ী (Godagari)`, `তাহিরপুর (Tahirpur)`).

### 1.2 Spatial Resolution Transparency
The frontend explicitly communicates the spatial footprint of underlying datasets:
- NASA POWER: $0.5^\circ \times 0.5^\circ$ grid (~50km) regional atmospheric observations.
- BMD Radar: Regional rainfall estimates.
- Sentinel-1 SAR: $20\text{m}$ spatial backscatter aggregation for surface water inundation.
- *Strict Notice*: District and Upazila summaries represent regional indicators, not sub-acre micro-field measurements (`DEC-06`).

---

## 2. Temporal Display & Timezone Conventions

### 2.1 Bangladesh Standard Time (BST)
All temporal markers, timestamps, and advisory validity ranges are presented in **Bangladesh Standard Time (BST = UTC+6)**.
- Format: `YYYY-MM-DD HH:mm:ss BST` (e.g., `2026-10-10 12:00:00 BST`).
- Relative Freshness: Highlighted in hours (e.g., "১২ ঘণ্টা পূর্বে সংগৃহীত").

### 2.2 Time Horizons for Analytics
1. **Tier 1 (Empirical Observations)**: Past 24 hours to 7-day retrospective aggregations.
2. **Tier 2 (Physical Water Balance)**: Daily time-step balance ($D_t$) updated at 00:00 BST.
3. **Tier 3 (Forecasts)**: 24h, 48h, and 72h lead times with daily aggregated rainfall probability and QPF.
4. **Tier 4 (Advisories)**: Valid for 24h to 48h depending on growth stage and upcoming weather events.

---

## 3. Missing Data & Quality Flags

- Missing meteorological observations are explicitly tagged as *"তথ্য অনুপলব্ধ"* rather than being displayed as zero rainfall.
- When satellite revisits are pending, the UI displays the timestamp of the latest valid pass along with the expected next acquisition window.
