# Ritucast: Master Candidate Dataset Inventory

## 1. Inventory Classification Framework

To systematically evaluate Earth observations and agricultural data sources for Bangladesh, every candidate is categorized by product nature:
- **Individual Dataset**: A discrete, versioned data stream with standardized parameters (e.g., GPM IMERG Final Daily).
- **Product Family**: A collection of satellite products spanning multiple processing levels or sensors (e.g., SMAP L1–L4).
- **Data-Access Platform**: A portal or API broker distributing underlying primary datasets (e.g., CROP-CASMA, NASA Earthdata CMR).
- **Derived Analytical Product**: A modeled or value-added output combining multiple observations (e.g., FAO-56 Penman-Monteith $ET_0$).
- **Institutional / Statistical Source**: Ground-based censuses, surveys, or agency records (e.g., BBS Yearbook of Agricultural Statistics).

---

## 2. Evaluation of 16 Candidate Data Categories

---

### 1. NASA POWER (Prediction Of Worldwide Energy Resources)
- **Product Nature**: Product Family / Dissemination Platform.
- **Specific Products Evaluated**: NASA POWER Daily Point & Regional APIs (Community: AG - Sustainable Agriculture).
- **Provider**: NASA Langley Research Center / NASA Earth Science Applied Sciences Program.
- **Official Documentation**: [power.larc.nasa.gov](https://power.larc.nasa.gov/) | [API Docs](https://power.larc.nasa.gov/docs/services/api/)
- **Core Parameters**: Daily $T_{\text{2M\_MAX}}$, $T_{\text{2M\_MIN}}$, $T_{\text{2M}}$, $ALLSKY\_SFC\_SW\_DWN$ (Insolation, $MJ/m^2/day$), $PRECTOTCORR$ ($mm/day$), $RH2M$ (%), $WS2M$ ($m/s$).
- **Spatial Resolution & Grid**: $0.5^\circ \times 0.5^\circ$ ($\approx 55\text{km}$ grid).
- **Temporal Properties**: Daily aggregates; 1981–present; updated daily with ~2–3 day latency for final MERRA-2/GEOS assimilation.
- **Bangladesh Coverage Status**: **Verified**. Global coverage includes all coordinates in Bangladesh without spatial masking.
- **Access & Licensing**: Free REST API, JSON/CSV output, no API key required, public domain (NASA Open Data Policy).
- **Suitability for Ritucast**: **High**. Provides the exact physical parameters required for FAO-56 Penman-Monteith Reference Evapotranspiration ($ET_0$) calculation (`DR-MET-01`, `FR-ADV-01`).
- **Initial Recommendation**: **SELECT (Initial Release Core - P0)**.

---

### 2. MODIS Vegetation Indices (NDVI / EVI)
- **Product Nature**: Individual Satellite Dataset Family.
- **Specific Products Evaluated**: `MOD13Q1` (Terra) and `MYD13Q1` (Aqua) Collection 6.1.
- **Provider**: NASA LP DAAC / USGS EROS Center.
- **Official Documentation**: [modis.gsfc.nasa.gov](https://modis.gsfc.nasa.gov/) | [LP DAAC MOD13Q1](https://lpdaac.usgs.gov/products/mod13q1v061/)
- **Core Parameters**: 250m 16-day composited Normalized Difference Vegetation Index (NDVI), Enhanced Vegetation Index (EVI), VI Quality flags, pixel reliability.
- **Spatial Resolution**: 250m nominal sinusoidal grid (Tiles `h26v06` and `h25v06` cover Bangladesh).
- **Temporal Properties**: 16-day composite; February 2000–present.
- **Bangladesh Coverage Status**: **Verified**. Tile `h26v06` fully captures central/eastern Bangladesh; `h25v06` captures western Rajshahi/Khulna.
- **Scientific Limitation in Bangladesh**: 16-day optical composites suffer from persistent cloud corruption during the monsoon (June–September T. Aman season). A 250m pixel encompasses 15–30 smallholder plots (*mixed pixel problem*).
- **Suitability for Ritucast**: Valuable as a secondary dry-season (Rabi / Boro) regional vigor benchmark, but cannot serve as a real-time operational trigger during the cloudy monsoon.
- **Initial Recommendation**: **OPTIONAL / SECONDARY (Dry Season Baseline - P2)**.

---

### 3. SMAP Soil Moisture Active Passive Products
- **Product Nature**: Product Family.
- **Specific Products Evaluated**:
  1. `SPL3SMP_E.006`: SMAP Enhanced L3 Radiometer Global Daily 9 km EASE-Grid Soil Moisture.
  2. `SPL4SMA.007`: SMAP L4 Global 3-hourly 9 km Surface and Root-Zone Soil Moisture.
- **Provider**: NASA JPL / NSIDC DAAC.
- **Official Documentation**: [smap.jpl.nasa.gov](https://smap.jpl.nasa.gov/) | [NSIDC SPL3SMP_E](https://nsidc.org/data/spl3smp_e/versions/6)
- **Core Parameters**: Surface volumetric soil moisture (0–5 cm, $m^3/m^3$), root-zone soil moisture (0–100 cm, modeled in L4), soil temperature, retrieval quality flags.
- **Spatial Resolution**: 9 km and 33 km effective radiometer resolution; EASE-Grid 2.0.
- **Temporal Properties**: 2–3 day revisit; March 2015–present; latency ~24–48 hours.
- **Bangladesh Coverage Status**: **Verified**. Granules verified via NASA CMR covering bounding box $88^\circ - 93^\circ\text{E}$, $20.5^\circ - 26.7^\circ\text{N}$.
- **Scientific Limitation in Bangladesh**: Radiometer L-band signals saturate over open water and standing flooded paddy fields (puddled Boro/Aman rice). Coarse 9km resolution averages ponds, settlements, and fields.
- **Suitability for Ritucast**: Excellent for capturing regional dry-spell soil drying curves across the upland Barind Tract, but must be paired with water-balance models for individual paddy plots.
- **Initial Recommendation**: **SELECT (Initial Release Core - P1 for Barind Pilot)**.

---

### 4. GPM IMERG Precipitation Estimates
- **Product Nature**: Individual Satellite Dataset Family.
- **Specific Products Evaluated**:
  1. `GPM_3IMERGDF.07`: IMERG Final Daily 0.1° $\times$ 0.1° (Research/climatology grade, ~3.5 month latency).
  2. `GPM_3IMERGDE.07`: IMERG Early Daily 0.1° $\times$ 0.1° (Operational near-real-time, ~4–6 hour latency).
- **Provider**: NASA Goddard Space Flight Center / NASA GES DISC.
- **Official Documentation**: [gpm.nasa.gov](https://gpm.nasa.gov/) | [GES DISC IMERG Guide](https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGDF_07/summary)
- **Core Parameters**: Calibrated daily precipitation ($mm/day$), probability of liquid precipitation, quality index.
- **Spatial Resolution**: $0.1^\circ \times 0.1^\circ$ ($\approx 10\text{km} \times 10\text{km}$).
- **Temporal Properties**: Daily and 30-minute intervals; June 2000–present.
- **Bangladesh Coverage Status**: **Verified**. Covers national territory and critical transboundary upstream catchments in Meghalaya, Assam, and Tripura.
- **Suitability for Ritucast**: Essential for 7-day cumulative rainfall anomaly tracking (`FR-ENV-02`) and upstream transboundary rainfall monitoring for Haor flash flood warnings (`FR-ADV-02`).
- **Initial Recommendation**: **SELECT (Initial Release Core - P0)**.

---

### 5. Sentinel-1 C-Band Synthetic Aperture Radar (SAR)
- **Product Nature**: Operational Satellite Mission / Level-1 GRD Products.
- **Specific Product Evaluated**: Sentinel-1 Level-1 Ground Range Detected (GRD), Interferometric Wide (IW) swath mode, dual polarization (VV + VH).
- **Provider**: European Space Agency (ESA) Copernicus Programme / Copernicus Data Space Ecosystem (CDSE).
- **Official Documentation**: [dataspace.copernicus.eu](https://dataspace.copernicus.eu/) | [Sentinel-1 User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-1-sar)
- **Core Parameters**: Calibrated radar backscatter intensity ($\sigma^\circ$ in dB); VV and VH polarization.
- **Spatial Resolution**: 10m $\times$ 10m pixel spacing (20m spatial resolution).
- **Temporal Properties**: 6–12 day repeat pass over Bangladesh; October 2014–present; operational latency ~2–3 hours from sensing on CDSE.
- **Bangladesh Coverage Status**: **Verified**. Regular descending and ascending passes cover Bangladesh. OData query verified immediate availability.
- **Cloud Penetration**: 100% cloud-penetrating. Crucial for mapping monsoon flood extent and Haor waterlogging when optical sensors fail completely.
- **Initial Recommendation**: **SELECT (Initial Release Core - P1 for Haor Flood Mapping)**.

---

### 6. Sentinel-2 Multi-Spectral Instrument (MSI)
- **Product Nature**: Operational Satellite Mission / Level-2A Surface Reflectance.
- **Provider**: European Space Agency (ESA) Copernicus Programme / CDSE.
- **Official Documentation**: [dataspace.copernicus.eu](https://dataspace.copernicus.eu/)
- **Core Parameters**: 13 spectral bands (10m VNIR, 20m Red-Edge / SWIR); Bottom-Of-Atmosphere (BOA) reflectance; Scene Classification Layer (SCL).
- **Spatial Resolution**: 10m to 20m.
- **Temporal Properties**: 5-day combined constellation revisit.
- **Evaluation & Constraint**: Heavy data volume (approx. 600MB–1GB per tile); optical bands suffer from 80–90% cloud occlusion during the crucial monsoon (Aman) season. Processing 10m imagery nationwide exceeds the $<1.5\text{MB}$ bandwidth budget of the MCP.
- **Initial Recommendation**: **DEFER (Scheduled for Phase 12/15 High-Resolution Expansion)**.

---

### 7. Crop-Yield and Crop-Production Statistics
- **Product Nature**: Official Institutional Agricultural Statistics.
- **Specific Source Evaluated**: Bangladesh Bureau of Statistics (BBS) *Yearbook of Agricultural Statistics* (published annually).
- **Provider**: BBS, Statistics and Informatics Division, Ministry of Planning, Government of Bangladesh.
- **Official Documentation**: [bbs.gov.bd](http://bbs.gov.bd/)
- **Parameters**: Net cultivated area (acres), total production (metric tons), and yield rate (maunds/acre, MT/ha) by district and division for major crops (Boro, Aman, Aus, Wheat, Potato, Jute, Mustard, Maize).
- **Granularity**: Disaggregated to the District level (64 districts); historical series spans 45+ years. Sub-district (Upazila) statistics are compiled during decennial Agricultural Censuses (2008, 2019), but not published annually in tabular digital formats.
- **Limitation**: District aggregates cannot serve as field-level ground truth labels for parcel-scale yield prediction.
- **Initial Recommendation**: **SELECT AS REGIONAL CONTEXT / BENCHMARK (P0 Contextual)**.

---

### 8. Crop Calendars and Phenological Guidelines
- **Product Nature**: Authoritative Agronomic Publications & Institutional Guidelines.
- **Specific Sources Evaluated**:
  1. Bangladesh Rice Research Institute (BRRI): *Adhunik Dhaner Chash* (Modern Rice Cultivation Guidelines, 23rd Edition).
  2. Bangladesh Agricultural Research Institute (BARI): *Krishi Projukti Hatboi* (Handbook of Agro-Technologies).
  3. DAE Agro-Meteorological Information Systems Development Project (AMISDP) Crop Weather Calendars.
- **Parameters**: Recommended sowing, transplanting, vegetative, flowering, and harvesting date ranges by variety (e.g., BRRI dhan28, BRRI dhan29, BRRI dhan89) across Agro-Ecological Zones; stage-specific crop coefficients ($K_c$).
- **Suitability for Ritucast**: Fundamental prerequisite for configuring stage-aware crop water requirement ($ET_c$) models (`FR-LOC-02`, `FR-ADV-01`).
- **Initial Recommendation**: **SELECT (Initial Release Core - P0)**.

---

### 9. Administrative Boundaries (GeoJSON / Spatial Polygons)
- **Product Nature**: Official Geospatial Vector Boundaries.
- **Specific Sources Evaluated**: Bangladesh Bureau of Statistics (BBS) GIS Unit / Survey of Bangladesh / UN OCHA HDX Bangladesh Administrative Boundaries (Level 0: Country, Level 1: Division, Level 2: District, Level 3: Upazila).
- **Official Source**: [data.humdata.org (HDX Bangladesh)](https://data.humdata.org/dataset/cod-ab-bgd) (verified source aligned with BBS codes).
- **Parameters**: 8 Divisions, 64 Districts, 495 Upazilas with standard P-codes (`BGD_ADM3_PCODE`) and English/Bangla names.
- **Coordinate Reference System**: EPSG:4326 (WGS 84).
- **Suitability for Ritucast**: Essential for spatial geocoding, boundary clipping, and administrative query routing (`FR-LOC-01`).
- **Initial Recommendation**: **SELECT (Initial Release Core - P0)**.

---

### 10. Soil Properties & Hydraulic Characteristics
- **Product Nature**: Spatial Soil Inventories & Global Digital Soil Maps.
- **Specific Sources Evaluated**:
  1. Soil Resource Development Institute (SRDI) Upazila Land and Soil Resource Utilization Guides (*Upazila Nirdeshika*).
  2. ISRIC SoilGrids 250m global digital soil mapping.
- **Parameters**: Soil texture classes (clay, silt loam, sandy clay), bulk density, cation exchange capacity (CEC), pH, available water capacity (AWC).
- **Evaluation**: SRDI guides exist in physical Bengali book formats for most upazilas but lack a centralized open API; SoilGrids provides gridded estimates globally but carries calibration uncertainties in alluvial delta soils.
- **Suitability for Ritucast**: Secondary reference for calibrating local soil water-holding capacities in Barind red clay vs Haor peat/silt soils.
- **Initial Recommendation**: **OPTIONAL / BACKGROUND CALIBRATION (Phase 4 Task)**.

---

### 11. Flood and Hydrological Monitoring Data
- **Product Nature**: Ground Hydrological Station Network & Operational Flood Bulletins.
- **Specific Source Evaluated**: Bangladesh Water Development Board (BWDB) Flood Forecasting and Warning Centre (FFWC).
- **Official Source**: [ffwc.gov.bd](http://www.ffwc.gov.bd/)
- **Parameters**: Daily observed river water levels (m PWD), danger levels, 24h/48h/72h deterministic and probabilistic river flood forecasts at 100+ river gauge stations.
- **Suitability for Ritucast**: Crucial ground reference for validating upstream transboundary river stage in the Surma-Kushiyara-Meghna system feeding Sunamganj haors.
- **Initial Recommendation**: **SELECT AS GROUND REFERENCE & VALIDATION TARGET (P1)**.

---

### 12. Historical Insurance Claims Data
- **Product Nature**: Institutional / Financial Proprietary Data.
- **Evaluation**: Green Delta Insurance, Sadharan Bima Corporation, and microfinance institutions pilot index-based crop insurance on small scales, but claim histories are proprietary, commercially sensitive, and completely unavailable via open APIs.
- **Initial Recommendation**: **REJECT / EXCLUDE (Irrelevant to Farmer Decision Support)**.

---

### 13. Agricultural Loan-Performance Data
- **Product Nature**: Proprietary Financial Records (Bangladesh Krishi Bank, BRAC, Grameen).
- **Evaluation**: Farmer credit default and loan repayment data is confidential personal financial data. Violates Ritucast’s privacy-by-design policy (`NFR-SEC-01`).
- **Initial Recommendation**: **REJECT / EXCLUDE (Violates Privacy Architecture)**.

---

### 14. Crop Market Prices
- **Product Nature**: Daily Agricultural Market Wholesale/Retail Feeds.
- **Specific Source Evaluated**: Department of Agricultural Marketing (DAM), Ministry of Agriculture ([dam.gov.bd](http://www.dam.gov.bd/)).
- **Parameters**: Daily wholesale and retail prices of rice, potato, vegetables across major markets.
- **Evaluation**: Valuable for economic harvest decisions in later phases, but out of scope for the Minimum Complete Product focusing on agro-climatic physical risk.
- **Initial Recommendation**: **DEFER (Scheduled for Horizon 2 / Phase 18)**.

---

### 15. Operational Climate & Weather Forecasts (NWP)
- **Product Nature**: Numerical Weather Prediction (NWP) Model Feeds.
- **Specific Sources Evaluated**:
  1. Open-Meteo Weather API (aggregates ECMWF IFS 9km, GFS 13km, and DWD ICON 11km).
  2. NOAA Global Forecast System (GFS) 0.25°.
  3. Bangladesh Meteorological Department (BMD) synoptic forecasts.
- **Parameters**: 7-day hourly and daily forecasted air temperature, precipitation probability, precipitation amount ($mm$), wind speed, relative humidity.
- **Suitability for Ritucast**: Essential for driving the 7-day forecast views (`FR-ENV-01`) and the 72-hour irrigation postponement engine (`FR-ADV-01`). Open-Meteo provides an open-license, non-commercial API without key restrictions that aggregates ECMWF and GFS.
- **Initial Recommendation**: **SELECT (Initial Release Core - P0)**.

---

### 16. CROP-CASMA (Crop Condition and Soil Moisture Analytics)
- **Product Nature**: Web GIS Platform & Decision Tool (USDA NASS / George Mason University).
- **Official Documentation**: [cloud.csiss.gmu.edu/crop-casma](https://cloud.csiss.gmu.edu/crop-casma/)
- **Evaluation**: CROP-CASMA is a specialized USDA portal serving SMAP-derived and MODIS-derived crop moisture indices **strictly for the Contiguous United States (CONUS)**. It does not provide global coverage or ingest Bangladesh datasets.
- **Initial Recommendation**: **REJECT AS A DIRECT DATASET (CONUS Only; Architecture Pattern Reference Only)**.

---

## 3. Summary of Inventory Decisions

| Candidate Category | Core Product Selected | Provider | Role in Ritucast | Initial Status |
| :--- | :--- | :--- | :--- | :---: |
| **1. Weather & Solar** | NASA POWER Daily Point/Regional API | NASA Langley | Atmospheric forcing & $ET_0$ calculation | **SELECT (P0)** |
| **2. Weather Forecast** | ECMWF / GFS via Open-Meteo NWP Feed | ECMWF / NOAA | 7-day operational weather forecasts | **SELECT (P0)** |
| **3. Precipitation** | GPM IMERG V07 (Early Daily & Final) | NASA GES DISC | 7-day anomaly & upstream catchment rain | **SELECT (P0)** |
| **4. Radar Flood** | Sentinel-1 C-Band SAR GRD | ESA Copernicus CDSE | Cloud-penetrating Haor inundation mapping | **SELECT (P1)** |
| **5. Soil Moisture** | SMAP Enhanced L3 9km (`SPL3SMP_E`) | NASA JPL / NSIDC | Barind root-zone moisture trend indicator | **SELECT (P1)** |
| **6. Crop Calendars** | BRRI & BARI Modern Cultivation Guides | BRRI / BARI / DAE | Stage-aware phenology & $K_c$ tables | **SELECT (P0)** |
| **7. Boundaries** | Bangladesh Admin GeoJSON (Level 3) | BBS / UN OCHA HDX | Upazila spatial scoping (495 Upazilas) | **SELECT (P0)** |
| **8. Ground Hydrology** | BWDB FFWC Water Level Records | BWDB FFWC | Ground reference for Haor flood crests | **SELECT (P1)** |
| **9. Vegetation VI** | MODIS 250m 16-day (`MOD13Q1.061`) | NASA LP DAAC | Dry-season regional vigor baseline | **OPTIONAL (P2)** |
| **10. Yield Statistics** | BBS Yearbook of Agricultural Statistics | BBS | Regional crop acreage and yield context | **OPTIONAL (P2)** |
| **11. High-Res Optical**| Sentinel-2 MSI Level-2A | ESA Copernicus | High-resolution field delineation | **DEFER** |
| **12. Soil Properties** | SRDI Upazila Guides / SoilGrids 250m | SRDI / ISRIC | Baseline hydraulic parameters | **DEFER** |
| **13. Market Prices** | DAM Daily Agricultural Market Prices | DAM | Economic harvesting optimization | **DEFER** |
| **14. Insurance Claims** | Private Crop Micro-Insurance Logs | Commercial Insurers | Financial risk modeling | **REJECT** |
| **15. Farmer Loans** | Bank Credit Repayment Records | Krishi Bank / MFIs | Credit scoring | **REJECT** |
| **16. CROP-CASMA** | USDA NASS CASMA System | USDA / GMU | Regional web tool (CONUS only) | **REJECT** |
