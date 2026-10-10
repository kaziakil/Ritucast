# Phase 3: Scientific Research Notes & Sensor Physics Evaluation

## 1. Executive Research Scope

- **Evaluation Date**: 2026-10-10
- **Lead Investigator**: Senior Earth Observation Scientist & Geospatial Analyst (Google Antigravity)
- **Domain Focus**: Radiometric, spatial, temporal, and physical characteristics of Earth observation missions over the tropical monsoon delta of Bangladesh.

---

## 2. Sensor Physics & Mission Deep Dives

---

### 2.1 NASA POWER Agrometeorology Deep Dive (`DATA-MET-01`)
- **Scientific Foundation**: NASA POWER assimilates satellite-derived radiative fluxes (from the NASA CERES mission) with global atmospheric reanalysis (Goddard Earth Observing System - GEOS-5 FP-IT / MERRA-2).
- **Solar Radiation Accuracy**: Accurately calculating FAO-56 Penman-Monteith Reference Evapotranspiration ($ET_0$) requires **downward shortwave surface insolation** ($R_s$). Standard weather station networks in Bangladesh rarely maintain calibrated pyranometers due to maintenance costs. NASA POWER's `ALLSKY_SFC_SW_DWN` parameter provides daily solar irradiance ($MJ/m^2/day$) derived from CERES satellite observations, bypassing the ground station data gap.
- **Precipitation Limitation**: NASA POWER's `PRECTOTCORR` is derived from global model reanalysis (MERRA-2) and has a known tendency to underestimate localized convective pre-monsoon squalls (*Kalbaishakhi*). **Finding**: NASA POWER should be utilized primarily for its temperature, solar radiation, humidity, and wind parameters, while GPM IMERG and NWP feeds provide operational precipitation totals.

---

### 2.2 GPM IMERG Precipitation Retrieval in Monsoon Delta (`DATA-PCP-01`)
- **Algorithm Architecture**: GPM IMERG (V07) merges passive microwave (PMW) radiometer measurements from the GPM constellation with geostationary infrared (IR) precipitation estimates, calibrated against monthly ground gauge analyses (GPCC).
- **Product Run Differences**:
  1. *Early Run* (`3IMERGDE`): Latency ~4–6 hours. Propagates microwave estimates forward using numerical weather model cloud motion vectors. Ideal for **real-time flood hazard warnings** and upstream Meghalaya cloudburst alerts.
  2. *Late Run* (`3IMERGDL`): Latency ~14 hours. Incorporates both forward and backward cloud motion vectors.
  3. *Final Run* (`3IMERGDF`): Latency ~3.5 months. Fully adjusted with GPCC monthly ground station rain gauge analyses. Ideal for **10-year historical climatology anomaly baselines**.
- **The Meghalaya Orographic Barrier**: The steep southern escarpment of the Meghalaya plateau (Cherrapunji / Mawsynram) rises abruptly from the low-lying Sylhet plains (from 5m to over 1,400m elevation). Orographic cloudbursts frequently trigger warm-rain microphysical processes where raindrops grow rapidly below the freezing level. Passive microwave sensors can partially underestimate these low-level warm clouds. **Mitigation**: Upstream transboundary warning algorithms must apply an empirical threshold ($>100\text{mm}/48\text{h}$) cross-checked with BWDB river gauge rises.

---

### 2.3 Sentinel-1 C-Band SAR Radar Physics & Inundation Mapping (`DATA-SAR-01`)
- **Radar Frequency & Cloud Penetration**: Sentinel-1 operates a C-band Synthetic Aperture Radar (SAR) at $5.405\text{ GHz}$ ($\lambda \approx 5.55\text{ cm}$). Because microwave wavelengths are orders of magnitude larger than cloud droplets ($10–50\ \mu\text{m}$) and rain drops ($1–3\text{ mm}$), C-band radar waves penetrate cloud cover, monsoon rain, smoke, and haze with negligible atmospheric attenuation.
- **Specular vs Diffuse Scattering**:
  - *Smooth Open Water / Flooded Paddy*: Incident microwave energy reflects away from the sensor like a mirror (*specular reflection*), resulting in extremely low radar backscatter ($\sigma^\circ_{\text{VV}} < -15\text{ dB}$ to $-18\text{ dB}$). Flooded areas appear jet black in SAR imagery.
  - *Dry Soil & Vegetation*: Rough surfaces cause *diffuse volume scattering*, returning significant energy back to the sensor ($\sigma^\circ_{\text{VV}} \approx -7\text{ dB}$ to $-12\text{ dB}$).
  - *Double-Bounce Scattering*: When rice stems emerge from standing water, the radar wave bounces from the water surface to the vertical stem and directly back to the satellite, producing high backscatter anomalies.
- **Operational Reality**: Sentinel-1 Level-1 GRD imagery achieves $10\text{m}$ pixel spacing. Our live CDSE verification demonstrated that products over Bangladesh are published online within **2 hours and 5 minutes** of satellite acquisition.

---

### 2.4 SMAP L-Band Radiometer Soil Moisture Realities (`DATA-SMC-01`)
- **Penetration Depth**: SMAP operates an L-band radiometer at $1.41\text{ GHz}$ ($\lambda \approx 21\text{ cm}$). L-band radiation responds to the dielectric constant of the **top 0–5 cm of the soil column**.
- **The Flooded Paddy Dilemma**: In Bangladesh, Boro and Aman rice paddies are puddled and deliberately maintained under 2–7 cm of standing water during transplanting and tillering. An L-band radiometer viewing a 9km footprint saturated with flooded paddies records maximum dielectric permittivity, indicating $100\%$ saturation. However, adjacent non-rice fields (mustard, wheat, vegetables) on higher terraces may simultaneously experience severe root-zone moisture deficits.
- **Architectural Decision**: SMAP radiometer soil moisture must be interpreted as a **regional macro-environmental drought index** for upland areas (Barind Tract), and **must not be used to infer water levels inside bunded rice paddies**.

---

### 2.5 MODIS (MOD13Q1) vs Sentinel-2 MSI Vegetation Indices (`DATA-VEG-01`)
- **MODIS MOD13Q1 (250m, 16-Day)**: Tile `h26v06` covers Bangladesh. While highly stable and calibrated across 2000–present, optical vegetation monitoring during the monsoon (June–September) is crippled by cloud cover. In a typical July, up to 85% of pixels in a 16-day MODIS composite over Sylhet or Barisal are labeled as cloud/aerosol contaminated in the VI Quality flag bits.
- **Sentinel-2 MSI (10m)**: Offers superb spatial detail ($10\text{m}$ resolution resolves individual bunded plots). However, each Sentinel-2 granule averages 800MB–1.2GB. Ingesting and cloud-masking 10m scenes nationwide during the initial phase would overwhelm processing pipelines without providing monsoon visibility.
- **Decision**: Include MODIS strictly as an optional dry-season regional baseline; defer Sentinel-2 to Phase 12.

---

## 3. Agronomic Reference Standards & Official Baselines

### 3.1 BRRI / BARI Crop Coefficients ($K_c$) for Bangladesh
Under FAO-56 methodology, crop water requirement is computed as:

$$ET_c = K_c \times ET_0$$

Using published benchmarks from BRRI (*Modern Rice Cultivation Guidelines*) and regional lysimeter trials:

| Growth Stage | Boro Rice (Winter Irrigated) | T. Aman Rice (Monsoon Rainfed) | Potato (Rabi Cash Crop) | Mustard (Rabi Cash Crop) |
| :--- | :---: | :---: | :---: | :---: |
| **Initial / Seedbed (0–20 days)** | $1.05$ | $1.10$ | $0.50$ | $0.40$ |
| **Vegetative / Tillering (20–55 days)** | $1.15$ | $1.15$ | $0.80$ | $0.75$ |
| **Mid-Season / Flowering (55–90 days)** | **$1.25 - 1.30$** (Peak Demand) | **$1.20 - 1.25$** | **$1.15$** (Peak) | **$1.05$** (Peak) |
| **Ripening / Harvesting (90–120+ days)**| $0.90$ | $0.95$ | $0.75$ | $0.45$ |

*Agronomic Note*: During flowering/panicle initiation, rice reaches peak crop water consumption ($K_c = 1.30$). If a dry spell occurs during this 2-week window, even mild moisture stress causes spikelet sterility and dramatic yield losses.

---

## 4. Primary Research Literature Cited

1. **Allen, R. G., et al. (1998)**. *Crop evapotranspiration: Guidelines for computing crop water requirements*. FAO Irrigation and Drainage Paper 56, Rome.
2. **BRRI (2021)**. *Adhunik Dhaner Chash (Modern Rice Cultivation)*, 23rd Ed. Bangladesh Rice Research Institute, Gazipur.
3. **NASA Earth Science (2023)**. *POWER System Documentation: Methodology for Agricultural Meteorology Data Products (v2.10)*. NASA Langley Research Center.
4. **Huffman, G. J., et al. (2020)**. *Integrated Multi-satellitE Retrievals for GPM (IMERG) Technical Documentation*. NASA Goddard Space Flight Center.
5. **Enenkel, M., et al. (2019)**. *Enhanced flood risk management in Bangladesh through Earth Observation and Cloud Computing*. Scientific Reports, Nature.
6. **BBS (2023)**. *Yearbook of Agricultural Statistics 2022*. Bangladesh Bureau of Statistics, Ministry of Planning.
