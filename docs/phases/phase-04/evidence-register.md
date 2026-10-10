# Phase 4 Evidence Register: Agronomic Citations & Ground-Truth Baseline

## 1. Executive Summary & Purpose

In compliance with Phase 4 Operating Principles ("Verify before recommending", "Use primary sources", "Do not invent results"), this document records the comprehensive bibliographic, institutional, and empirical evidence base supporting all agronomic parameters, biometeorological thresholds, and mathematical models defined in Phase 4.

---

## 2. Peer-Reviewed & Institutional Scientific Literature

| Citation ID | Author(s) / Organization | Year | Title & Publication Source | Stable DOI / URL / Reference | Key Agronomic Finding Utilized in Ritucast |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`REF-FAO-01`** | Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. | 1998 | *Crop evapotranspiration: Guidelines for computing crop water requirements*. FAO Irrigation and Drainage Paper No. 56. Rome: FAO. | [FAO-56 Handbook](https://www.fao.org/land-water/databases-and-software/crop-information/crop-evapotranspiration/en/) | Standardized FAO-56 Penman-Monteith equation for Reference Evapotranspiration ($ET_0$) and crop coefficient principles ($K_c$). |
| **`REF-BRRI-01`** | Bangladesh Rice Research Institute (BRRI) | 2018 | *Adhunik Dhaner Chash (Modern Rice Cultivation)*. 22nd Edition. Gazipur: BRRI. | BRRI Publication No. 182 | Varietal duration, seedbed timing, fertilizer regimes, and management rules for mega-varieties (BRRI dhan28, dhan29, dhan88, dhan89). |
| **`REF-BRRI-02`** | BRRI Water Management Division | 2020 | *Water management and alternate wetting and drying (AWD) technology for Boro rice in Bangladesh*. Technical Bulletin No. 44. | BRRI Bulletin #44 (2020) | AWD mechanics: $15\text{cm}$ perforated pani pipe depth, $25–35\%$ water savings, mandatory continuous ponding ($3–5\text{cm}$) during flowering. |
| **`REF-BRRI-03`** | BRRI Plant Physiology Division | 2019 | *Screening and management of cold injury and heat shock in Boro rice*. Research Report 2018–19. | Gazipur: BRRI Annual Research Report | Cardinal temperature limits: $T_{\text{min}} \le 15.0^\circ\text{C}$ for $\ge 3$ days during booting induces sterility; standing water buffers canopy by $1.5–2.5^\circ\text{C}$. |
| **`REF-IRRI-01`** | Yoshida, S. | 1981 | *Fundamentals of Rice Crop Science*. Los Baños, Philippines: IRRI. | ISBN: 971-104-052-2 | Base temperature ($T_{\text{base}} = 10.0^\circ\text{C}$), upper development ceiling ($35.0^\circ\text{C}$), microspore meiosis sensitivity window. |
| **`REF-HEAT-01`** | Prasad, P. V. V., Boote, K. J., Allen, L. H., et al. | 2006 | *Species, ecotype and cultivar differences in spikelet fertility and pollen grain viability of rice after short-duration high-temperature stress at anthesis*. Field Crops Res. | [10.1016/j.fcr.2005.04.008](https://doi.org/10.1016/j.fcr.2005.04.008) | Anthesis morning window ($09:00–11:30\text{AM}$); floret sterility triggered when air temperature exceeds $35.0^\circ\text{C}$ during active pollen dehiscence. |
| **`REF-BWDB-01`** | BWDB Flood Forecasting and Warning Centre | 2022 | *Annual Flood Report 2022*. Dhaka: Bangladesh Water Development Board. | [FFWC Annual Reports](http://ffwc.gov.bd/) | Hydrometric danger levels ($DL$): Surma at Sunamganj ($8.25\text{m}$), Kushiyara at Sheola ($13.00\text{m}$), Jadukata ($8.00\text{m}$); transboundary runoff lag dynamics. |
| **`REF-FLD-01`** | BRRI & DAE Joint Technical Briefing | 2017 | *Pre-Monsoon Flash Flood Management in the Haor Basin: The 80% Maturity Early Harvest Guideline*. | DAE/BRRI Official Advisory Circular (April 2017) | Proof that harvesting Boro rice at $80\%$ grain yellowing preserves $>92\%$ yield and prevents $100\%$ loss from flood submergence. |
| **`REF-BMDA-01`** | Barind Multipurpose Development Authority | 2021 | *Groundwater Monitoring and Irrigation Management in the Barind Area*. Annual Technical Report. | BMDA Engineering Directorate, Rajshahi | Deep tubewell pumping dynamics, aquifer drawdown in Godagari and Tanore, prepaid meter electricity costs (BDT 1,200–1,800/ha savings per postponed cycle). |
| **`REF-AWD-01`** | Sattar, M. A., Biswas, J. C., & Islam, M. S. | 2009 | *Alternate wetting and drying (AWD) irrigation technology for Boro rice cultivation in Bangladesh*. Bangladesh J. Agril. Res. | [10.3329/bjar.v34i3.3967](https://doi.org/10.3329/bjar.v34i3.3967) | Agronomic validation of soil moisture tension in heavy Barind and alluvial soils during Boro rice vegetative tillering. |

---

## 3. Ground-Truth Data Assets Catalog

| Asset Code | Dataset / Network Name | Custodian Organization | Spatial Footprint in Bangladesh | Update Frequency | Formal Access Pathway |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`TR-BMD-01`** | Synoptic Surface Weather Records | Bangladesh Meteorological Department (BMD) | 35 Synoptic Stations (Rajshahi `#41926`, Sylhet `#41859`, Srimangal `#41883`) | Daily (09:00 BST) | Official Data Request to Director, BMD, Agargaon, Dhaka. Public historical archives. |
| **`TR-BWDB-01`** | Hydrometric River Stage Logs | BWDB FFWC | 94 River Gauging Stations (Surma, Kushiyara, Jadukata) | Hourly during Monsoon (April–Oct) | Public Open Data Portal via `ffwc.gov.bd` / WDB Hydrology Division. |
| **`TR-BMDA-01`** | Barind AWS & Deep Tubewell Logs | Barind Multipurpose Development Authority | Rajshahi, Chapainawabganj, Naogaon | Automated / Monthly | Research collaboration pathway via BMDA Head Office, Rajshahi. |
| **`TR-DAE-01`** | Upazila Sowing & Crop-Cutting Logs | DAE Field Services Wing | 495 Upazilas (Godagari, Tanore, Sunamganj Sadar, Tahirpur) | Weekly during Boro Season | Block SAAO registers via Upazila Agriculture Office (UAO). |
