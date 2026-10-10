# Ritucast: Product-Level Data Requirements Specification

## 1. Scope & Purpose of Data Requirements

This document establishes the **functional data specifications** required to support Ritucast's initial release scope. It defines the variables, resolutions, latencies, and validation boundaries that **Phase 3 (Dataset Research and Validation)** must rigorously audit.

Phase 2 specifies **what data the product requires**; Phase 3 will determine **which specific API endpoints and data products satisfy these requirements**.

---

## 2. Product-Level Data Requirements Matrix

---

### Category 1: Gridded Agro-Meteorology & Atmospheric Forcing (`DR-MET`)

- **Requirement ID**: `DR-MET-01`
- **Candidate Data Sources**: NASA POWER Agrometeorology API, Bangladesh Meteorological Department (BMD) synoptic feeds.
- **Agricultural Purpose**: Driving the FAO-56 Penman-Monteith Reference Evapotranspiration ($ET_0$) calculation and identifying extreme temperature stress (cold fog injury, heatwave spikelet sterility).
- **Decisions Supported**: Dry-season irrigation scheduling (`FR-ADV-01`), safe spray windows (`FR-ADV-03`), cold injury seedbed protection.
- **Required Geographic Coverage**: National coverage across Bangladesh ($20.5^\circ\text{N} - 26.7^\circ\text{N}$, $88.0^\circ\text{E} - 92.7^\circ\text{E}$).
- **Required Temporal Coverage & Freshness**: Daily observations from 2015–present for baseline climatology; daily operational forecast updates refreshed every $\le 12\text{ hours}$.
- **Desired Resolution**:
  - Spatial: $\le 0.5^\circ \times 0.5^\circ$ ($\approx 50\text{km}$); interpolatable to Upazila centroids.
  - Temporal: Daily aggregates (minimum/maximum temperature, daily sum solar radiation, daily mean wind speed, daily mean dew point).
- **Required Variables**:
  1. $T_{2M\_MAX}$, $T_{2M\_MIN}$ (Air Temperature at 2m, °C)
  2. $ALLSKY\_SFC\_SW\_DWN$ (All Sky Insolation Incident on Horizontal Surface, $MJ/m^2/day$)
  3. $RH2M$ (Relative Humidity at 2m, %)
  4. $WS2M$ (Wind Speed at 2m, $m/s$)
- **Missing-Data Behavior & Tolerance**: If operational forecast is missing for day $T+1$, fallback to persistence model with confidence degradation warning. If missing for $>36\text{h}$, suppress automated recommendations (`NFR-REL-03`).
- **Known Scientific Limitations**: Coarse $0.5^\circ$ grid integrates regional topography; microclimatic river valleys and urban heat islands are not resolved.
- **Priority Tier**: **P0 (Essential / Foundational)**

---

### Category 2: High-Resolution Precipitation Tracking & Catchment Runoff (`DR-PCP`)

- **Requirement ID**: `DR-PCP-01`
- **Candidate Data Sources**: GPM IMERG (Integrated Multi-satellitE Retrievals for GPM) Early/Late Runs, BMD rain gauges.
- **Agricultural Purpose**: Tracking 72-hour forecast rain for irrigation postponement and monitoring upstream transboundary Meghalaya catchment rainfall for Haor flash flood warnings.
- **Decisions Supported**: Irrigation cancellation (`FR-ADV-01`), Haor emergency harvest mobilization (`FR-ADV-02`).
- **Required Geographic Coverage**: Bangladesh national territory + upstream transboundary catchments (Meghalaya, Assam, Tripura, Barak basin).
- **Required Temporal Coverage & Freshness**: Rolling 30-day historical precipitation + operational feeds refreshed within $<6\text{ hours}$ of satellite acquisition.
- **Desired Resolution**:
  - Spatial: $\le 0.1^\circ \times 0.1^\circ$ ($\approx 10\text{km} \times 10\text{km}$).
  - Temporal: 30-minute to 3-hour precipitation rates; aggregated to daily rainfall totals ($mm/day$).
- **Required Variables**:
  1. `precipitationCal` (Multi-satellite precipitation estimate with gauge calibration, $mm/hr$).
  2. `probabilityLiquidPrecipitation` (Phase discrimination).
- **Missing-Data Behavior & Tolerance**: Early Run estimates carry higher random noise; system must verify against regional BMD synoptic stations before issuing high-severity flood alerts.
- **Known Scientific Limitations**: Infrared-calibrated microwave algorithms can underestimate warm-rain orographic cloudbursts along steep Meghalaya escarpments.
- **Priority Tier**: **P0 (Essential / Foundational)**

---

### Category 3: Regional Root-Zone Soil Moisture Deficit (`DR-SMC`)

- **Requirement ID**: `DR-SMC-01`
- **Candidate Data Sources**: NASA SMAP (Soil Moisture Active Passive) L3/L4 surface and root-zone products, downscaled models.
- **Agricultural Purpose**: Benchmarking regional soil moisture storage to prevent crop wilting during dry spells and guiding AWD (Alternate Wetting and Drying) irrigation.
- **Decisions Supported**: Deep tubewell pumping initiation/postponement (`FR-ADV-01`).
- **Required Geographic Coverage**: Barind Tract pilot zone (Rajshahi, Naogaon, Chapainawabganj) and national cropland.
- **Desired Resolution**:
  - Spatial: 9km to 36km (or downscaled 1km–3km products where verified).
  - Temporal: 2–3 day revisit interval; rolling 7-day anomaly curves.
- **Required Variables**:
  1. `sm_surface` (Top 0–5 cm volumetric soil moisture, $m^3/m^3$).
  2. `sm_rootzone` (Top 0–100 cm volumetric soil moisture, $m^3/m^3$).
  3. `sm_anomaly` (Normalized difference against historical seasonal mean).
- **Missing-Data Behavior & Tolerance**: Fill gaps using continuous soil water-balance modeling ($P_{\text{eff}} - ET_c$).
- **Known Scientific Limitations**: SMAP measures surface dielectric properties; standing floodwater in rice paddies saturates the signal. Must be disaggregated from upland crops.
- **Priority Tier**: **P1 (Essential for Barind Pilot)**

---

### Category 4: Cloud-Penetrating Radar Surface Inundation (`DR-SAR`)

- **Requirement ID**: `DR-SAR-01`
- **Candidate Data Sources**: Sentinel-1 C-band SAR (Synthetic Aperture Radar) Level-1 Ground Range Detected (GRD).
- **Agricultural Purpose**: Cloud-penetrating mapping of standing floodwater and waterlogging in low-lying Haor basins and floodplains.
- **Decisions Supported**: Haor Boro emergency harvest warning (`FR-ADV-02`), waterlogging drainage alerts.
- **Required Geographic Coverage**: Haor Basin pilot zone (Sunamganj, Sylhet, Kishoreganj, Netrokona, Habiganj).
- **Desired Resolution**:
  - Spatial: $10\text{m} \times 10\text{m}$ to $20\text{m} \times 20\text{m}$.
  - Temporal: 6–12 day satellite repeat pass over Bangladesh.
- **Required Variables**:
  1. VV and VH polarization backscatter ($\sigma^\circ$ in dB).
  2. Binary surface watermask (Backscatter $<-15\text{dB}$ threshold relative to dry baseline).
- **Missing-Data Behavior & Tolerance**: 6–12 day latency is too slow for 24h flash flood arrival; must be cross-referenced with GPM upstream rainfall (`DR-PCP-01`) for predictive warnings.
- **Known Scientific Limitations**: Wind-induced surface roughening on large open water bodies increases radar backscatter, occasionally causing false non-water classifications.
- **Priority Tier**: **P1 (Essential for Haor Pilot)**

---

### Category 5: Administrative Boundaries & Crop Baselines (`DR-AGR`)

- **Requirement ID**: `DR-AGR-01`
- **Candidate Data Sources**: Bangladesh Bureau of Statistics (BBS), Survey of Bangladesh, BRRI, BARI, BARC.
- **Agricultural Purpose**: Spatial scoping of administrative units and aligning agronomic advisories with official crop calendars.
- **Required Variables**:
  1. Upazila, District, and Division GeoJSON boundary polygons (495 Upazilas).
  2. Upazila-level Agro-Ecological Zone (AEZ 1–30) mapping.
  3. Standard crop calendars: Sowing, transplanting, tillering, flowering, harvest windows for Boro, Aman, Aus, Potato, Mustard.
  4. Crop growth coefficients ($K_c$) for each phenological stage.
- **Priority Tier**: **P0 (Essential / Foundational)**

---

## 3. Data Requirements Summary for Phase 3 Investigation

| ID | Category | Primary Sensor / Source | Geographic Scope | Desired Latency | Priority Tier | Phase 3 Audit Mandate |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **`DR-MET-01`** | Agrometeorology | NASA POWER / BMD | National (64 Districts) | $<12\text{h}$ | **P0** | Verify API rate limits, daily updates, $T$, $RH$, $WS$, $SW$ availability. |
| **`DR-PCP-01`** | Precipitation | GPM IMERG / BMD | National + Transboundary Meghalaya | $<6\text{h}$ | **P0** | Audit IMERG Early run latency and upstream catchment boundaries. |
| **`DR-SMC-01`** | Soil Moisture | SMAP L3/L4 | Barind Pilot + National | $<48\text{h}$ | **P1** | Audit spatial resolution fit and correlation in Barind clay soils. |
| **`DR-SAR-01`** | Radar Inundation | Sentinel-1 C-band SAR | Haor Basin (Sylhet) | $<12\text{h}$ | **P1** | Audit ESA Copernicus Data Space API access, pass frequency over Haors. |
| **`DR-AGR-01`** | Boundaries & Calendars | BBS / BRRI / BARI | National (495 Upazilas) | Static | **P0** | Obtain verified GeoJSON boundaries and stage-specific $K_c$ tables. |
