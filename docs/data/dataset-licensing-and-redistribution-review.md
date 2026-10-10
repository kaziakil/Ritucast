# Dataset Licensing, Provenance, and Redistribution Review — Ritucast

## 1. Executive Summary

This review evaluates the intellectual property, copyright, and redistribution terms governing all Earth-observation datasets, meteorological feeds, and agricultural calibration parameters utilized by **Ritucast**.

All data utilized in Ritucast's production release is licensed under open access, public domain, or government open data terms, permitting offline pre-processing, derivative indicator generation, and public advisory distribution.

---

## 2. Dataset Licensing Matrix

| Dataset ID | Source Organization | Data Type | Official License / Terms | Commercial Use Permitted? | Redistribution & Caching Rights | Attribution Requirement |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `DATA-MET-01` | **NASA POWER Project** | Solar Radiation, Temperature, Humidity | Public Domain (US Government Work / Open Data) | Yes | Yes (Unlimited caching and derived feature distribution) | Required citation: *"NASA Prediction of Worldwide Energy Resources (POWER) Project"* |
| `DATA-FCST-01` | **Open-Meteo API** | Numerical Weather Forecasts (GFS, ECMWF, ICON) | Open Database License (ODbL) / CC-BY 4.0 | Yes (Attribution required) | Yes (Permits caching and derivative indicators) | Required attribution: *"Weather data by Open-Meteo.com"* |
| `DATA-SAR-01` | **European Space Agency (ESA) / Copernicus** | Sentinel-1 SAR C-band Backscatter | Open Access under EU Regulation No 1159/2013 | Yes | Yes (Full redistribution of processed water extent masks) | Required citation: *"Contains modified Copernicus Sentinel data [year]"* |
| `DATA-AGR-01` | **Bangladesh Rice Research Institute (BRRI)** | Boro Rice Phenology, Crop Coefficients ($K_c$) | Public Agricultural Research Extension Publications | N/A (Scientific Reference) | Yes (Used for physical equation calibration) | BRRI Boro Rice Production Guidelines (BRRI Gazette) |
| `DATA-HYD-01` | **Bangladesh Water Development Board (BWDB)** | River Stage Gauges, Danger Levels ($8.25\text{m}$) | Public Hydrological Bulletin / FFWC Open Portal | Yes (Public Decision Support) | Permitted (Official government flood monitoring levels) | BWDB Flood Forecasting and Warning Centre (FFWC) |
| `DATA-BND-01` | **Bangladesh Bureau of Statistics (BBS) / GADM** | Administrative Upazila Boundaries (Level 3) | GADM Open License / BBS Open Geo Portal | Non-Commercial / Government Open Data | Permitted (Simplified polygon packaging for pilot zones) | GADM / BBS Administrative Boundary Database |

---

## 3. Derivative Product Creation & Redistribution Rights

### 3.1 Pre-Packaged Local Parquet Tables (`DEC-52`)
- **Architecture**: As established in Phase 13, Ritucast packages pre-computed Upazila summaries inside the backend container image ([`deploy/docker/Dockerfile.backend`](file:///Users/kazi/Projects/RITUCAST/deploy/docker/Dockerfile.backend)) at `/app/data/processed/`. Total dataset size is $<110\text{KB}$.
- **Legal Compliance**:
  - NASA POWER and Open-Meteo allow caching, transformation, and redistribution of derived agro-meteorological metrics.
  - The pre-packaged files represent derived analytical aggregates (daily means, water deficit calculations), not raw redistributions of copyrighted proprietary models.

### 3.2 Provenance Preservation
- Every API advisory response preserves data provenance metadata:
  ```json
  "provenance": {
    "weather_source": "NASA POWER / Open-Meteo GFS",
    "science_basis": "FAO-56 Penman-Monteith (1998)",
    "flood_index": "BWDB River Stage + Sentinel-1 SAR",
    "crop_calendar": "BRRI Boro Rice Agro-ecological Guidelines",
    "evaluated_at_utc": "2026-10-10T11:50:00Z"
  }
  ```
- Transparent provenance allows agricultural extension workers to audit the physical sensors driving recommendations.

---

## 4. Attribution Notices in User Interface

In compliance with the attribution terms of Copernicus and Open-Meteo:
1. **Application Footer**: Displays clear attribution links:
   - *"আবহাওয়া তথ্য: Open-Meteo ও NASA POWER"*
   - *"কৃষি মানদণ্ড: বাংলাদেশ ধান গবেষণা ইনস্টিটিউট (BRRI) ও FAO-56"*
2. **Metadata Endpoint**: Exposes [`/api/v1/provenance`](file:///Users/kazi/Projects/RITUCAST/api/routers/provenance.py) providing machine-readable dataset versions and licensing terms.

Related documentation:
- [`docs/privacy/data-inventory.md`](file:///Users/kazi/Projects/RITUCAST/docs/privacy/data-inventory.md)
- [`docs/data/data-access-and-licensing.md`](file:///Users/kazi/Projects/RITUCAST/docs/data/data-access-and-licensing.md)
- [`docs/responsible-ai/agricultural-recommendation-safeguards.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/agricultural-recommendation-safeguards.md)
