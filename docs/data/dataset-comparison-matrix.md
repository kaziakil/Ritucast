# Ritucast: Master Dataset Comparison Matrix

## 1. Specification & Identification Standard

Every candidate dataset is assigned a stable identifier (`DATA-XXX-##`) that maps directly to the functional requirements defined in Phase 2.

---

## 2. Master Comparison Matrix

| Field | `DATA-MET-01` (Agro-Meteorology) | `DATA-FCST-01` (Weather Forecast) | `DATA-PCP-01` (Precipitation) | `DATA-SAR-01` (Radar Inundation) | `DATA-SMC-01` (Soil Moisture) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dataset / Product** | NASA POWER Daily Point / Regional API (Community: AG) | ECMWF IFS 9km / NOAA GFS 13km via Open-Meteo API | GPM IMERG V07 (Early Daily & Final Daily) | Sentinel-1 Level-1 GRD IW Swath (Dual VV+VH) | SMAP Enhanced L3 Radiometer Global Daily 9km (`SPL3SMP_E.006`) |
| **Provider** | NASA Langley Research Center | Open-Meteo / ECMWF / NOAA | NASA GES DISC / GSFC | European Space Agency (ESA) Copernicus CDSE | NASA JPL / NSIDC DAAC |
| **Official Source** | [power.larc.nasa.gov](https://power.larc.nasa.gov/) | [open-meteo.com](https://open-meteo.com/en/docs) | [disc.gsfc.nasa.gov](https://disc.gsfc.nasa.gov/) | [dataspace.copernicus.eu](https://dataspace.copernicus.eu/) | [nsidc.org](https://nsidc.org/data/spl3smp_e/versions/6) |
| **Category** | Historical & Near-Real-Time Agro-Weather | Numerical Weather Prediction (NWP) | Multi-Satellite Precipitation Estimates | Synthetic Aperture Radar (SAR) Microwave | Passive Microwave Soil Moisture Radiometer |
| **Requirements Supported**| `FR-ENV-01`, `FR-ADV-01`, `DR-MET-01` | `FR-ENV-01`, `FR-ADV-01`, `FR-ADV-03` | `FR-ENV-02`, `FR-ADV-02`, `DR-PCP-01` | `FR-ENV-04`, `FR-ADV-02`, `DR-SAR-01` | `FR-ENV-03`, `FR-ADV-01`, `DR-SMC-01` |
| **Bangladesh Coverage** | **Verified (Complete)**: $0.5^\circ$ regular grid nationwide. | **Verified (Complete)**: Seamless global coverage at $9\text{km}-13\text{km}$. | **Verified (Complete)**: $0.1^\circ$ global grid including transboundary catchments. | **Verified (Complete)**: Ascending & descending passes over all divisions. | **Verified (Complete)**: Regular coverage over Bangladesh bounding box. |
| **Spatial Resolution** | $0.5^\circ \times 0.5^\circ$ ($\approx 55\text{km} \times 55\text{km}$) | $0.1^\circ \times 0.1^\circ$ ($\approx 9\text{km} - 11\text{km}$) | $0.1^\circ \times 0.1^\circ$ ($\approx 10\text{km} \times 10\text{km}$) | $10\text{m} \times 10\text{m}$ pixel spacing (20m resolution) | 9km nominal EASE-Grid 2.0 (33km native antenna footprint) |
| **Temporal Properties** | Daily aggregates; 1981–present; updated daily (~2-3 day latency). | Hourly & Daily; 7-day forecast horizon; refreshed every 1–6 hours. | Daily & 30-min; 2000–present; Early Run latency ~4–6h; Final ~3.5 mo. | 6–12 day repeat pass; 2014–present; latency ~2–3h from sensing on CDSE. | Daily composite; 2–3 day revisit; 2015–present; latency ~24–48h. |
| **Core Variables** | $T_{\text{max}}, T_{\text{min}}, SW_{\text{in}}, RH, WS, P_{\text{corr}}$ | $T_{\text{max}}, T_{\text{min}}, P_{\text{prob}}, P_{\text{sum}}, WS, RH$ | `precipitationCal` ($mm/day$, $mm/hr$), `probLiquid` | $\sigma^\circ_{\text{VV}}, \sigma^\circ_{\text{VH}}$ radar backscatter (dB) | `soil_moisture` ($m^3/m^3$), `soil_temp`, retrieval flags |
| **Units & Quality** | °C, $MJ/m^2/day$, %, $m/s$, $mm/day$. Fill: `-999.0`. | °C, %, $mm$, $km/h$. Normalized WMO codes. | $mm/hr$, $mm/day$. Quality Index flag. | Decibels (dB). Orbit state vectors & calibration LUTs. | $m^3/m^3$ volumetric. Quality flag bits (0 = recommended). |
| **Access Method** | REST API (JSON / CSV outputs). | REST API (JSON output, lightweight). | NASA CMR STAC / Earthdata OPeNDAP / HTTPS. | Copernicus OData / STAC API / S3 object store. | NASA CMR STAC / Earthdata HTTPS / OPeNDAP. |
| **Authentication** | None (Completely open public API). | None for non-commercial tier ($<10,000$ daily calls). | NASA Earthdata Login (Free OAuth2 Bearer token). | CDSE Keycloak (Free OAuth2 token). | NASA Earthdata Login (Free OAuth2 Bearer token). |
| **Licensing** | Public Domain (NASA Open Data Policy). | Open Data (CC-BY 4.0; ECMWF Open Data Terms). | Public Domain (NASA Open Data Policy). | Open Access (Copernicus Legal Notice - Full & Open). | Public Domain (NASA Open Data Policy). |
| **Data Volume & Complexity** | Very Low ($<10\text{KB}$ per Upazila request). | Very Low ($<15\text{KB}$ per Upazila request). | Low-Medium (~10MB global NetCDF daily slice). | High (~1.2GB per GRD ZIP scene); raster clipping needed. | Medium (~40MB per global HDF5 granule). |
| **Processing Complexity** | **Low**: Direct JSON ingestion into PostgreSQL/timeseries. | **Low**: Direct JSON ingestion into frontend/backend cache. | **Medium**: Subsetting bounding box, NetCDF to array extraction. | **High**: Radiometric calibration, speckle filter, dB thresholding. | **Medium**: HDF5 extraction, EASE-Grid projection, spatial downscale. |
| **Scientific Limitations** | Coarse $0.5^\circ$ cell averages topography; misses local microclimates. | Forecast skill decays beyond 72h; convective storm location error. | Underestimates orographic warm rain on steep Meghalaya faces. | Wind roughening causes false non-water; revisit gap misses peak crest. | Radiometer saturates over puddled flooded paddy fields. |
| **Initial Priority** | **P0 (Foundational Core)** | **P0 (Foundational Core)** | **P0 (Foundational Core)** | **P1 (Essential Haor Pilot)** | **P1 (Essential Barind Pilot)** |
| **Validation Status** | **VERIFIED**: Empirical live API request confirmed for Rajshahi & Haor. | **VERIFIED**: Endpoint and JSON schema confirmed. | **VERIFIED**: CMR granules identified covering Bangladesh box. | **VERIFIED**: CDSE OData query confirmed immediate product access. | **VERIFIED**: CMR granule metadata verified covering coordinates. |

---

## 3. Supplementary and Contextual Datasets Comparison

| Field | `DATA-AGR-01` (Crop Calendars) | `DATA-BND-01` (Admin Boundaries) | `DATA-HYD-01` (Ground Hydrology) | `DATA-VEG-01` (MODIS NDVI) | `DATA-YLD-01` (Crop Statistics) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dataset / Product** | BRRI & BARI Modern Rice & Crop Calendars | Bangladesh Administrative Boundaries Level 0–3 GeoJSON | BWDB FFWC River Stage & Flood Records | MODIS Terra 16-Day 250m (`MOD13Q1.061`) | BBS *Yearbook of Agricultural Statistics* |
| **Provider** | BRRI / BARI / DAE | BBS / UN OCHA HDX | Bangladesh Water Development Board (BWDB) | NASA LP DAAC / USGS | Bangladesh Bureau of Statistics (BBS) |
| **Category** | Agronomic Guidelines & Phenology Tables | Geospatial Vector Boundaries | In-Situ River Water Level Gauge Logs | Satellite Optical Vegetation Reflectance | Official National Agricultural Statistics |
| **Requirements Supported**| `FR-LOC-02`, `FR-ADV-01`, `DR-AGR-01` | `FR-LOC-01`, `DR-AGR-01` | `FR-ENV-04`, `FR-ADV-02` | `FR-ENV-02` (Auxiliary), `DR-VEG-01` | Regional benchmark / context |
| **Bangladesh Coverage** | **Verified**: National cropping systems across all 30 AEZs. | **Verified**: 8 Divisions, 64 Districts, 495 Upazilas. | **Verified**: 100+ river monitoring stations nationwide. | **Verified**: Tile `h26v06` covers Bangladesh. | **Verified**: 64 administrative districts. |
| **Spatial Resolution** | Variety / AEZ specific | Polygons with $<10\text{m}$ coordinate precision | Point coordinates (synoptic river gauges) | 250m sinusoidal grid | District-level tabular totals |
| **Temporal Properties** | Seasonal / Annual revisions | Updated periodically following upazila reorganizations | Daily observed water levels; 1990–present | 16-day composite; 2000–present | Annual publication (1–2 year lag) |
| **Core Variables** | Sowing/harvest windows, duration (days), $K_c$ per stage | `ADM3_EN`, `ADM3_PCODE`, Upazila GeoJSON geometry | River level (m PWD), Danger Level, 24h change | 250m NDVI, EVI, VI Quality flags | Harvested area (acres), Production (MT), Yield |
| **Access Method** | Official published handbooks & agronomic tables | Static GeoJSON file download / GitHub / HDX | FFWC web portal / daily PDF & web table bulletins | NASA CMR / LP DAAC Earthdata HTTPS | Official BBS reports / PDF and statistical tables |
| **Authentication** | Public domain government publications | None (Open access) | None (Public portal) | Free Earthdata OAuth2 | None (Official publications) |
| **Licensing** | Public Information (Government of Bangladesh) | CC-BY-IGO (Open humanitarian data) | Public Water Data (Government of Bangladesh) | Public Domain (NASA Open Data Policy) | Official National Statistics (Gov of BD) |
| **Initial Priority** | **P0 (Foundational Core)** | **P0 (Foundational Core)** | **P1 (Validation Ground Reference)** | **P2 (Optional Dry-Season Context)** | **P2 (Contextual Benchmark)** |
| **Validation Status** | **VERIFIED**: Phenology benchmarks and $K_c$ extracted. | **VERIFIED**: Validated 495-upazila boundaries available. | **VERIFIED**: FFWC Surma/Kushiyara station series verified. | **VERIFIED**: Tile `h26v06` identified in CMR. | **VERIFIED**: District time series verified. |
