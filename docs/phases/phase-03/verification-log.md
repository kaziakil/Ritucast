# Phase 3: Data Access Verification Log

## 1. Verification Protocol & Execution Context

- **Execution Date**: 2026-10-10
- **Environment**: Google Antigravity Terminal Environment (macOS, curl, network active)
- **Principle**: Zero fabrication. Every entry records an actual HTTP/API call executed, the exact request URL, HTTP response status, returned payload structure, and verified variables.

---

## 2. Empirical Verification Records

---

### Test 1: NASA POWER Daily Point API — Rajshahi Pilot Zone (Godagari)
- **Target Dataset**: `DATA-MET-01` (NASA POWER Agrometeorology)
- **Coordinates Tested**: Longitude: `88.33`, Latitude: `24.47` (Godagari Upazila, Rajshahi Division)
- **Target Date Range**: `20240401` to `20240403` (Peak dry-season Boro flowering / heatwave period)
- **Exact Command Executed**:
  ```bash
  curl -s "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,WS2M,ALLSKY_SFC_SW_DWN&community=AG&longitude=88.33&latitude=24.47&start=20240401&end=20240403&format=JSON"
  ```
- **HTTP Response Status**: `200 OK`
- **Execution Latency**: `0.534 seconds`
- **Response Structure Verified**:
  - `geometry.coordinates`: `[88.33, 24.47, 27.43]` (Point coordinate + elevation in meters).
  - `header.api.name`: `"POWER Daily API"`, `version: "v2.10.0"`.
  - `header.sources`: `["SYN1DEG", "MERRA2", "POWER"]`.
  - `header.fill_value`: `-999.0`.
- **Sample Verified Values (2024-04-01)**:
  - `T2M_MAX`: `39.18°C` (Captured actual severe pre-monsoon heatwave).
  - `T2M_MIN`: `22.59°C`.
  - `ALLSKY_SFC_SW_DWN`: `24.49 MJ/m²/day` (Solar insolation for Penman-Monteith).
  - `PRECTOTCORR`: `0.37 mm/day`.
  - `RH2M`: `36.9%`.
  - `WS2M`: `4.28 m/s`.
- **Conclusion**: **VERIFIED**. Endpoint is operational, zero authentication required, returns all 7 target agrometeorological parameters with clean units and physical plausibility.

---

### Test 2: NASA POWER Daily Point API — Haor Pilot Zone (Tahirpur, Sunamganj)
- **Target Dataset**: `DATA-MET-01` (NASA POWER Agrometeorology)
- **Coordinates Tested**: Longitude: `91.17`, Latitude: `25.09` (Tahirpur Upazila, Sunamganj, Haor Basin)
- **Target Date Range**: `20240415` to `20240417` (Pre-monsoon flash flood window)
- **Exact Command Executed**:
  ```bash
  curl -s "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN&community=AG&longitude=91.17&latitude=25.09&start=20240415&end=20240417&format=JSON"
  ```
- **HTTP Response Status**: `200 OK`
- **Execution Latency**: `0.425 seconds`
- **Response Structure Verified**:
  - `geometry.coordinates`: `[91.17, 25.09, 72.07]` (Elevation 72m at Meghalaya piedmont).
  - `PRECTOTCORR` (2024-04-15): `2.13 mm/day`; `RH2M` reached `73.95%`.
- **Conclusion**: **VERIFIED**. Accurately differentiates eastern humid wetland climates from western dry Barind climates.

---

### Test 3: NASA CMR Granule Search — GPM IMERG Daily Precipitation (`DATA-PCP-01`)
- **Target Dataset**: GPM IMERG Final Daily V07 (`GPM_3IMERGDF`)
- **Target Bounding Box**: `88.0, 20.5, 92.8, 26.7` (Bangladesh national domain)
- **Exact Command Executed**:
  ```bash
  curl -s "https://cmr.earthdata.nasa.gov/search/granules.json?short_name=GPM_3IMERGDF&version=07&bounding_box=88.0,20.5,92.8,26.7&temporal=2024-04-01T00:00:00Z,2024-04-03T23:59:59Z&page_size=2"
  ```
- **HTTP Response Status**: `200 OK`
- **Returned Granule Metadata**:
  - `producer_granule_id`: `3B-DAY.MS.MRG.3IMERG.20240401-S000000-E235959.V07B.nc4`
  - `dataset_id`: `"GPM IMERG Final Precipitation L3 1 day 0.1 degree x 0.1 degree V07"`
  - `boxes`: `["-90 -180 90 180"]` (Global grid).
- **Conclusion**: **VERIFIED**. Daily global NetCDF4 granules exist in the catalog covering Bangladesh without spatial gaps.

---

### Test 4: NASA CMR Granule Search — SMAP Enhanced L3 9km Soil Moisture (`DATA-SMC-01`)
- **Target Dataset**: SMAP Enhanced L3 Radiometer Global Daily 9 km (`SPL3SMP_E.006`)
- **Target Bounding Box**: `88.0, 20.5, 92.8, 26.7`
- **Exact Command Executed**:
  ```bash
  curl -s "https://cmr.earthdata.nasa.gov/search/granules.json?short_name=SPL3SMP_E&version=006&bounding_box=88.0,20.5,92.8,26.7&temporal=2024-04-01T00:00:00Z,2024-04-03T23:59:59Z&page_size=2"
  ```
- **HTTP Response Status**: `200 OK`
- **Returned Granule Metadata**:
  - `producer_granule_id`: `SMAP_L3_SM_P_E_20240401_R19240_001.h5`
  - `dataset_id`: `"SMAP Enhanced L3 Radiometer Global Daily 9 km EASE-Grid Soil Moisture V006"`
  - `boxes`: `["-85.0445 -180 85.0445 180"]`
- **Conclusion**: **VERIFIED**. Version 6 enhanced 9km HDF5 granules exist and cover the target spatial domain.

---

### Test 5: NASA CMR Granule Search — MODIS Terra 250m 16-Day Vegetation Indices (`DATA-VEG-01`)
- **Target Dataset**: MODIS/Terra Vegetation Indices 16-Day L3 Global 250m SIN Grid V061 (`MOD13Q1`)
- **Target Bounding Box**: `88.0, 20.5, 92.8, 26.7`
- **Exact Command Executed**:
  ```bash
  curl -s "https://cmr.earthdata.nasa.gov/search/granules.json?short_name=MOD13Q1&version=061&bounding_box=88.0,20.5,92.8,26.7&temporal=2024-04-01T00:00:00Z,2024-04-20T23:59:59Z&page_size=2"
  ```
- **HTTP Response Status**: `200 OK`
- **Returned Granule Metadata**:
  - `producer_granule_id`: `MOD13Q1.A2024081.h26v06.061.2024099104414`
  - `dataset_id`: `"MODIS/Terra Vegetation Indices 16-Day L3 Global 250m SIN Grid V061"`
  - `tile`: `h26v06` (Sinusoidal tile covering Bangladesh).
- **Conclusion**: **VERIFIED**. Confirmed tile `h26v06` provides 250m NDVI/EVI coverage over Bangladesh.

---

### Test 6: ESA Copernicus Data Space Ecosystem (CDSE) OData Search — Sentinel-1 SAR GRD (`DATA-SAR-01`)
- **Target Dataset**: Sentinel-1 C-Band SAR Level-1 GRD IW Dual-Pol over Bangladesh
- **Spatial Polygon Intersect**: `POLYGON((88.0 24.0, 92.0 24.0, 92.0 26.0, 88.0 26.0, 88.0 24.0))`
- **Target Date Range**: `2024-04-01` to `2024-04-05`
- **Exact Command Executed**:
  ```bash
  curl -s "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?\$filter=Collection/Name%20eq%20'SENTINEL-1'%20and%20contains(Name,'GRD')%20and%20OData.CSC.Intersects(area=geography'SRID=4326;POLYGON((88.0%2024.0,92.0%2024.0,92.0%2026.0,88.0%2026.0,88.0%2024.0))')%20and%20ContentDate/Start%20ge%202024-04-01T00:00:00.000Z%20and%20ContentDate/Start%20le%202024-04-05T23:59:59.000Z&\$top=2"
  ```
- **HTTP Response Status**: `200 OK`
- **Returned Granule Metadata**:
  - `Id`: `"35eb54b5-b7d8-41a8-a081-75b16a7fbf77"`
  - `Name`: `"S1A_IW_GRDH_1SDV_20240401T235542_20240401T235607_053247_067408_F90B_COG.SAFE"`
  - `ContentLength`: `1,254,817,882 bytes` (~1.25 GB)
  - `OriginDate` (Sensing Time): `2024-04-02T00:17:48.698516Z`
  - `PublicationDate` (Available on CDSE): `2024-04-02T02:22:10.335998Z`
  - `Online`: `true`
- **Latency Finding**: Time delta between sensing and publication was **2 hours and 5 minutes**.
- **Conclusion**: **VERIFIED**. Sentinel-1 SAR Level-1 GRD imagery is indexed, fully available, and published with near-real-time latency ($<3\text{h}$) over Bangladesh via the CDSE OData API.
