# Ritucast: Data Access, Licensing & Legal Governance

## 1. Governance & Licensing Framework

Ritucast is engineered strictly on **open-access, non-proprietary environmental data streams**. This document formalizes the access endpoints, authentication protocols, rate limits, redistribution rights, and mandatory legal attribution notices for all datasets in the initial stack.

---

## 2. Access Specifications & API Protocols

---

### 1. NASA POWER Daily Point & Regional APIs (`DATA-MET-01`)
- **Official Documentation**: [power.larc.nasa.gov/docs/services/api/](https://power.larc.nasa.gov/docs/services/api/)
- **Base Endpoint**: `https://power.larc.nasa.gov/api/temporal/daily/point`
- **Authentication**: **None Required**. Open public API.
- **Request Parameters**:
  - `parameters`: Comma-separated list (`T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,WS2M,ALLSKY_SFC_SW_DWN`)
  - `community`: `AG` (Sustainable Agriculture)
  - `longitude`, `latitude`: WGS84 decimal degrees
  - `start`, `end`: Format `YYYYMMDD`
  - `format`: `JSON`
- **Rate Limits & Quotas**: NASA POWER enforces a soft concurrency limit of 30 requests per minute per IP address. Automated backoff ($429$ response) is required.
- **Licensing & Usage Rights**: Public Domain (NASA Earth Science Open Data Policy). Completely free for non-commercial and commercial derivation.
- **Mandatory Attribution**: *"NASA POWER Project, NASA Langley Research Center, Prediction Of Worldwide Energy Resources."*

---

### 2. Open-Meteo NWP Operational Weather Forecast API (`DATA-FCST-01`)
- **Official Documentation**: [open-meteo.com/en/docs](https://open-meteo.com/en/docs)
- **Base Endpoint**: `https://api.open-meteo.com/v1/forecast`
- **Authentication**: **None Required** for non-commercial tier ($<10,000$ daily API calls).
- **Request Parameters**:
  - `latitude`, `longitude`: WGS84 decimal degrees
  - `daily`: `weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,windspeed_10m_max,relative_humidity_2m_mean`
  - `timezone`: `Asia/Dhaka`
  - `models`: `ecmwf_ifs025,gfs_seamless`
- **Rate Limits**: 10,000 requests/day, 600 requests/minute on open endpoint. Caching layer on Ritucast backend guarantees requests remain $<2,000/\text{day}$.
- **Licensing & Usage Rights**: Open Data under Creative Commons Attribution 4.0 International (CC-BY 4.0). Numerical weather models licensed under ECMWF and NOAA open data policies.
- **Mandatory Attribution**: *"Weather data by Open-Meteo.com, licensed under CC-BY 4.0, incorporating ECMWF and NOAA forecast models."*

---

### 3. NASA GPM IMERG Precipitation Estimates (`DATA-PCP-01`)
- **Official Documentation**: [disc.gsfc.nasa.gov](https://disc.gsfc.nasa.gov/) | [CMR Search API](https://cmr.earthdata.nasa.gov/)
- **Access Endpoints**:
  - Search / Discovery: `https://cmr.earthdata.nasa.gov/search/granules.json?short_name=GPM_3IMERGDF&version=07`
  - Data Retrieval: NASA GES DISC HTTPS OPeNDAP and Earthdata Cloud S3.
- **Authentication**: **NASA Earthdata Login (Free OAuth2 Bearer Token)**. Requires free account registration at `urs.earthdata.nasa.gov`.
- **Rate Limits**: Normal HTTPS downloads supported; rate limits handled via standard HTTP basic auth or bearer tokens in `.netrc`.
- **Licensing & Usage Rights**: Public Domain (NASA Open Data Policy). Free, open redistribution with citation.
- **Mandatory Attribution**: *"Global Precipitation Measurement (GPM) Integrated Multi-satellitE Retrievals for GPM (IMERG), NASA Goddard Space Flight Center."*

---

### 4. ESA Copernicus Sentinel-1 C-Band SAR GRD (`DATA-SAR-01`)
- **Official Documentation**: [dataspace.copernicus.eu](https://dataspace.copernicus.eu/)
- **Access Endpoints**:
  - Catalog / OData: `https://catalogue.dataspace.copernicus.eu/odata/v1/Products`
  - STAC API: `https://stac.dataspace.copernicus.eu/v1`
  - S3 Object Store: `s3.dataspace.copernicus.eu`
- **Authentication**: **Copernicus Data Space Ecosystem (CDSE) Keycloak Token**. Requires free registration at `dataspace.copernicus.eu`; Bearer token requested via `oauth.dataspace.copernicus.eu`.
- **Rate Limits & Quotas**: Free tier supports up to 4 concurrent downloads and 100 API queries per minute.
- **Licensing & Usage Rights**: Open Access under the European Union Copernicus Programme Legal Notice (Full, Open, and Free Data Policy). Commercial and non-commercial reuse permitted.
- **Mandatory Attribution**: *"Contains modified Copernicus Sentinel data [year], processed by Ritucast."*

---

### 5. NASA SMAP Enhanced L3 Radiometer Soil Moisture (`DATA-SMC-01`)
- **Official Documentation**: [nsidc.org/data/spl3smp_e/versions/6](https://nsidc.org/data/spl3smp_e/versions/6)
- **Access Endpoints**: NASA Earthdata CMR Search + NSIDC DAAC HTTPS / OPeNDAP.
- **Authentication**: **NASA Earthdata Login (OAuth2)**.
- **Licensing & Usage Rights**: Public Domain (NASA Open Data Policy).
- **Mandatory Attribution**: *"NASA Soil Moisture Active Passive (SMAP) Mission, NASA Jet Propulsion Laboratory and NSIDC DAAC."*

---

### 6. Bangladesh Administrative Boundaries & Ground Statistics (`DATA-BND-01`, `DATA-HYD-01`, `DATA-AGR-01`)
- **Sources**: Bangladesh Bureau of Statistics (BBS), Bangladesh Water Development Board (BWDB), Bangladesh Rice Research Institute (BRRI).
- **Access Endpoints**:
  - Administrative GeoJSON: UN OCHA Humanitarian Data Exchange (HDX) Bangladesh repository.
  - River Gauges: BWDB Flood Forecasting and Warning Centre public portal.
  - Crop Calendars: Official published BRRI modern rice cultivation guidelines.
- **Authentication**: None. Public open records.
- **Licensing**: Public Government Data, Government of the People's Republic of Bangladesh.
- **Mandatory Attribution**: *"Administrative boundaries sourced from BBS / Survey of Bangladesh via HDX; hydrological references from BWDB FFWC; agronomic benchmarks from BRRI."*

---

## 3. Privacy, Data Minimization & Ethical Governance

1. **Zero Farm-Level Geolocation Ingestion**: Ritucast queries and caches data strictly at the **Upazila and Union administrative centroid level**. The platform never logs or transmits individual farm field GPS coordinates to external third-party APIs.
2. **Zero Personally Identifiable Information (PII)**: In accordance with `NFR-SEC-01`, no farmer names, phone numbers, national identification numbers, or land ownership records are collected or stored in database tables.
3. **No Commercial Exclusivity**: All processed agro-climatic indicators remain open, transparent, and non-monopolized.
