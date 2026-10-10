# Phase 8: Data Licensing, Attribution & Scientific Safeguards

## 1. Executive Summary & Open Data Policy

Ritucast operates strictly within open-data and open-science frameworks. No proprietary, commercial, or confidential datasets are used. All public datasets are ingested under clear license agreements with appropriate institutional attributions.

---

## 2. Dataset Licensing & Attribution Register

| Source ID | Dataset Name | Custodian / Provider | License | Attribution Requirement |
| :--- | :--- | :--- | :---: | :--- |
| **`DATA-MET-01`** | **NASA POWER Agrometeorology** | NASA Langley Research Center | **Public Domain** (US Govt Work) | *"NASA Prediction Of Worldwide Energy Resources (POWER) Project, NASA Langley Research Center."* |
| **`DATA-FCST-01`** | **Open-Meteo Operational NWP** | Open-Meteo / ECMWF / NOAA | **CC BY 4.0** | *"Weather data provided by Open-Meteo under CC BY 4.0 (incorporating ECMWF IFS and NOAA GFS)."* |
| **`DATA-PCP-01`** | **GPM IMERG Precipitation** | NASA GSFC / JAXA | **Open Access** (Earthdata) | *"Global Precipitation Measurement (GPM) IMERG V07, NASA GES DISC."* |
| **`DATA-SAR-01`** | **Sentinel-1 C-Band SAR GRD** | European Space Agency (ESA) | **Copernicus Open Access** | *"Contains modified Copernicus Sentinel data [year], processed by Ritucast."* |
| **`DATA-SMC-01`** | **SMAP Enhanced L3 Soil Moisture**| NASA JPL / NSIDC | **Open Access** (Earthdata) | *"Soil Moisture Active Passive (SMAP) L3 Radiometer Soil Moisture, NSIDC DAAC."* |
| **`DATA-BND-01`** | **Bangladesh Administrative GeoJSON**| BBS / Survey of Bangladesh / HDX | **CC BY-IGO 3.0** | *"Administrative boundaries provided by Bangladesh Bureau of Statistics via UN OCHA HDX."* |
| **`DATA-AGR-01`** | **BRRI/BARI Phenology & $K_c$ Tables**| BRRI / BARI / DAE | **Public Domain / DAE Extension**| *"Phenological parameters adapted from BRRI (Bangladesh Rice Research Institute) publications."* |
| **`DATA-HYD-01`** | **BWDB FFWC River Stage Gauge Logs** | BWDB FFWC | **Public Hydrology Bulletins** | *"River water level records courtesy of Flood Forecasting and Warning Centre (FFWC), BWDB."* |

---

## 3. Mandatory Scientific Safeguards & Data Limitations

The data pipeline enforces strict scientific safeguards to prevent overconfident or erroneous downstream farming advice:

### Safeguard 1: Coarse Satellite Resolution Limitation (`RSK-03`)
- **Principle**: Spaceborne sensors like SMAP (9km) and GPM IMERG (10km) capture macro-regional moisture trends across dozens of square kilometers. They cannot resolve sub-acre plot boundaries or individual paddy bund heights.
- **Enforcement**: Ingestion outputs are explicitly tagged with `spatial_resolution_km`. Pipeline metadata prohibits presenting zonal averages as parcel-specific truths.

### Safeguard 2: Optical Sensor Cloud Blindness in Monsoon (`RSK-02`)
- **Principle**: Optical sensors (Sentinel-2, MODIS) are occluded by monsoon clouds 80–90% of the time during June–October.
- **Enforcement**: Optical sensors are excluded from the core hazard and waterlogging pipelines. Cloud-penetrating Sentinel-1 C-band SAR and microwave precipitation are mandatory.

### Safeguard 3: Ground-Truth Verification Mandate (`DEC-10`, `DEC-17`)
- **Principle**: No numerical algorithm can substitute for direct physical inspection of the paddy bund (আইল).
- **Enforcement**: Provenance manifests enforce that all downstream advisory payloads carry the mandatory field check text:
  > *"সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*
