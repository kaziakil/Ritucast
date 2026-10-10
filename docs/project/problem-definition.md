# Ritucast: Agricultural Problem Definition & Ranked Inventory

## 1. Overview & Evaluation Framework

Agricultural decision-making in Bangladesh operates under intense agro-ecological pressures, high seasonal variability, and pronounced climate vulnerability. To ensure Ritucast builds high-utility solutions rather than speculative features, this document conducts an evidence-based assessment of candidate agricultural challenges.

### Evidence Classification Standard
- **Documented Fact (DF)**: Backed by published peer-reviewed literature, official statistics (BBS, DAE, BMD, BWDB), or multilateral agency reports (FAO, IRRI, World Bank).
- **Reasonable Interpretation (RI)**: Logically derived from validated agro-climatic trends and field practices, supported by domain consensus, but subject to local micro-variations.
- **Unverified Hypothesis (UH)**: Plausible assumption or user need that requires empirical field validation or direct user research during subsequent phases.

---

## 2. Ranked Problem Inventory

| Rank | Problem Area | Primary Affected Zones / Crops | Severity | Actionability via EO / Weather | Evidence Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Excess Soil Moisture, Waterlogging & Flash-Flood Inundation** | Haor Basin (Northeast: Sunamganj, Sylhet), Lowlands / Boro Rice & Kharif-1 Crops | Critical | High (SAR, GPM, IMERG, Hydrology) | **DF** (Strong) |
| **2** | **Irrigation Timing & Dry-Spell / Moisture-Deficit Stress** | Barind Tract (Northwest: Rajshahi, Rangpur) / Boro Rice, Wheat, Maize | High | High (SMAP, POWER, ET Models) | **DF** (Strong) |
| **3** | **Uncertainty in Sowing / Transplanting & Harvest Timing** | National (Aman, Boro, Aus) / Rice, Mustard, Potato | High | Moderate-High (Phenology, Rainfall windows) | **DF** (Strong) |
| **4** | **Pre-Visual Crop Condition & Vegetative Stress Detection** | Intensive cropping clusters / Commercial Vegetables, Rice, Potato | Moderate | Moderate (NDVI/EVI anomaly; cloud limited) | **RI** (Moderate) |
| **5** | **Field-Level Micro-Pest / Disease Outbreak Prediction** | National / Potato Late Blight, Rice Blast, BPH | High | Low (Requires micro-climate + field scouting) | **UH** (Weak for EO alone) |

---

## 3. Detailed Problem Investigation

---

### Problem 1: Excess Soil Moisture, Waterlogging & Flash-Flood Inundation (Rank 1)

#### 1. Problem and Agricultural Context
Early pre-monsoon flash floods (April–May) frequently inundate the northeastern Haor wetlands of Bangladesh (Sunamganj, Kishoreganj, Habiganj, Netrokona, Sylhet), threatening the mature Boro rice crop right before or during harvest. Boro rice represents ~54% of national rice production (BBS, 2022/2023). A single flood event can devastate hundreds of thousands of hectares within 48 to 72 hours. Concurrently, unseasonal monsoon depressions cause prolonged waterlogging in southern delta districts, rotting Kharif vegetables and newly transplanted Aman seedlings.

#### 2. Stakeholders Affected
- Smallholder Haor Boro rice farmers (loss of entire annual household grain income).
- Department of Agricultural Extension (DAE) Sub-Assistant Agriculture Officers (SAAOs).
- Bangladesh Water Development Board (BWDB) and local disaster management committees.

#### 3. Key Decisions Farmers Must Make
- **Emergency Early Harvest**: Should the farmer harvest Boro rice at 80% grain maturity (accepting slight yield/moisture penalties) before flood arrival, or wait for 100% maturity?
- **Labor & Machinery Mobilization**: When should expensive combine harvesters or labor gangs be hired before transport becomes impossible due to rising waters?
- **Drainage & Sluice Gate Operations**: When to dig perimeter trenches or open community drainage channels.

#### 4. Consequences of Poor or Delayed Decisions
- Total loss of submerged unharvested standing crop (100% economic loss).
- Grain germination and rot on panicles submerged under warm muddy water.
- Prolonged debt cycles for vulnerable smallholder households.

#### 5. Current Methods & Alternatives
- Visual water gauge watching at upstream rivers (Surma, Kushiyara).
- Informal phone calls to upstream relatives near the Indian Meghalaya border.
- DAE/BWDB flood bulletin broadcasts (often issued at river-basin scale, lacking localized field-inundation projections).

#### 6. Limitations of Existing Approaches
- River gauge data indicates river levels, not overland field waterlogging or depression retention.
- Lack of field-accessible mobile notifications tailored to specific upazilas and haors.

#### 7. How Ritucast Can Help
- Integrate GPM IMERG upstream catchment precipitation tracking + Sentinel-1 SAR radar water-inundation mapping (cloud-penetrating).
- Generate a "Harvest Urgency Window" score for haor upazilas indicating upstream runoff accumulation risks 3–5 days ahead.

#### 8. Required Data and Scientific Capabilities
- GPM IMERG real-time precipitation estimates (upstream Meghalaya/Assam catchments + national).
- Sentinel-1 C-band SAR GRD data (flood extent mapping).
- BWDB water level observation tie-ins (where open).
- Digital Elevation Models (DEM: SRTM 30m / Copernicus DEM 30m) for hydrological flow accumulation.

#### 9. Potential Limitations & Failure Modes
- Flash floods can arrive within 12–24 hours of extreme upstream cloudbursts; 6–12 day satellite radar revisit intervals can miss sudden peak crests without predictive hydrometeorological modeling.
- Downstream backwater effects require hydrological modeling beyond raw precipitation totals.

#### 10. Strength of Available Evidence
- **Documented Fact (DF)**: Comprehensive documentation by BWDB, CEGIS, BBS, and FAO regarding Boro losses in haor basins (e.g., 2017 haor flood catastrophe affected >200,000 hectares).

---

### Problem 2: Irrigation Timing & Dry-Spell / Moisture-Deficit Stress (Rank 2)

#### 1. Problem and Agricultural Context
The Northwestern Barind Tract (Rajshahi, Naogaon, Chapainawabganj, Dinajpur) suffers from declining groundwater tables and high irrigation costs. Boro rice in the dry rabi season (January–April) is almost 100% dependent on deep tubewell (DTW) and shallow tubewell (STW) diesel/electric pumping. Pumping represents 25–35% of total production cost. Over-irrigation wastes scarce groundwater and diesel subsidies, while intermittent dry-spell stress during flowering causes spikelet sterility and dramatic yield drops.

#### 2. Stakeholders Affected
- Smallholder Boro, wheat, and maize farmers in groundwater-stressed zones.
- Tubewell operators (Barind Multipurpose Development Authority - BMDA prepaid card systems).
- Upazila agricultural officers managing regional water efficiency.

#### 3. Key Decisions Farmers Must Make
- **Irrigation Scheduling**: Should the farmer pump today (costing 1,500–2,500 BDT/acre) or will incoming rain meet crop water demand over the next 48–72 hours?
- **Alternate Wetting and Drying (AWD) Adherence**: Is the root-zone soil moisture safe enough to let the field dry for another 2–3 days without stressing the crop?

#### 4. Consequences of Poor or Delayed Decisions
- **Over-pumping**: Excessive operational cost, accelerated groundwater depletion, and nutrient leaching.
- **Under-irrigation**: Moisture stress during panicle initiation / flowering causing up to 40–60% yield penalty.

#### 5. Current Methods & Alternatives
- Visual surface soil cracking inspection.
- Fixed calendar-based pumping (e.g., every 4 to 6 days regardless of weather).
- Occasional use of perforated PVC AWD pipes (low adoption due to manual checking requirements).

#### 6. Limitations of Existing Approaches
- Surface dryness often deceives farmers into pumping even when subsoil/root-zone moisture is sufficient.
- Weather forecasts on public media lack evapotranspiration (ET₀) and crop-stage water balance calculations.

#### 7. How Ritucast Can Help
- Provide root-zone moisture trend estimates and short-term (1–5 day) crop water deficit forecasts by combining NASA POWER (solar radiation, wind, temp, humidity for Penman-Monteith ET₀) with SMAP soil moisture anomalies.
- Deliver actionable advisories: *"Postpone irrigation: 15–25mm rain expected in 48 hours"* or *"Critical moisture deficit: irrigate within 48h to prevent flowering stress."*

#### 8. Required Data and Scientific Capabilities
- NASA POWER daily agrometeorology (solar radiation, temperature, dew point, wind speed).
- Reference Evapotranspiration ($ET_0$) calculation using FAO-56 Penman-Monteith equations.
- SMAP L3/L4 surface and root-zone soil moisture products.
- Crop coefficients ($K_c$) from BRRI/BARI for major crop growth stages.

#### 9. Potential Limitations & Failure Modes
- SMAP coarse resolution (9–36km) cannot distinguish adjacent flooded paddy from upland mustard without downscaling or hydrological water-balance disaggregation.
- Micro-topography and bund management create field-to-field variations.

#### 10. Strength of Available Evidence
- **Documented Fact (DF)**: Validated extensively by BMDA, BRRI, and IWMI publications on groundwater over-extraction and AWD economics in Northwest Bangladesh.

---

### Problem 3: Uncertainty in Sowing / Transplanting & Harvest Windows (Rank 3)

#### 1. Problem and Agricultural Context
Bangladesh’s cropping intensity exceeds 190%, with many farmers practicing double- or triple-cropping (e.g., Aman rice $\rightarrow$ Mustard/Potato $\rightarrow$ Boro rice). Sowing and transplanting windows are extremely tight (often a 10–14 day margin). Delays in monsoon onset (affecting T. Aman transplanting) or early winter cold spells (affecting Boro seedbed nursery germination) cause cascade delays throughout the year.

#### 2. Stakeholders Affected
- Smallholders and tenant farmers balancing multi-crop rotations.
- DAE extension planners issuing regional sowing advisories.

#### 3. Key Decisions Farmers Must Make
- **Transplanting Date**: When is cumulative soil wetness sufficient to transplant Aman seedlings without supplemental pumping?
- **Cold Injury Avoidance**: When to cover Boro seedbeds with polythene sheeting during December–January cold fog waves.
- **Harvesting Window**: When to reap Aman or Potato crops to avoid unseasonal pre-winter depressions or late-season storms.

#### 4. Consequences of Poor or Delayed Decisions
- Over-aged seedlings transplanted, resulting in reduced tillering and 15–25% lower yields.
- Seedling mortality from cold injury in Boro nurseries.
- Post-harvest grain spoilage from unexpected rain during field drying.

#### 5. Current Methods & Alternatives
- Traditional almanacs (*Panjika*), ancestral heuristics, local calendar dates.
- BAMIS web portal bulletins (often PDF-based or generic district-level text).

#### 6. Limitations of Existing Approaches
- Climate change has shifted traditional rainfall patterns; historic calendar dates frequently fail.
- Advisories fail to account for variety-specific phenological durations (e.g., short-duration BRRI dhan75 vs. long-duration BRRI dhan49).

#### 7. How Ritucast Can Help
- Combine localized rainfall probability, soil moisture indices, and thermal comfort thresholds into a "Farming Window Index" (Transplanting Readiness, Safe Harvest Window).

#### 8. Required Data and Scientific Capabilities
- Historical and forecasted precipitation (GPM IMERG, numerical weather predictions).
- Temperature extremes (minimum temperature <10°C cold waves, maximum >35°C heat stress).
- BBS/BRRI crop calendar data and thermal degree-day (GDD) benchmarks.

#### 9. Potential Limitations & Failure Modes
- Seasonal and sub-seasonal weather forecasts beyond 7–10 days carry substantial meteorological uncertainty.
- Ritucast must clearly convey probabilistic likelihood rather than deterministic guarantees.

#### 10. Strength of Available Evidence
- **Documented Fact (DF)**: Well-established in DAE and BRRI annual agrometeorological reports; shifting monsoon patterns documented by BMD.

---

### Problem 4: Pre-Visual Vegetative Condition & Anomaly Monitoring (Rank 4)

#### 1. Problem and Agricultural Context
Detecting vegetative lag, nutrient deficiency, or drought stress across large agricultural tracts before irreversible stunting occurs allows proactive corrective intervention (top-dressing fertilizer, supplemental watering).

#### 2. Evaluation & Priority Rationale
- **Limitation**: During the major monsoon season (T. Aman, June–October), persistent cloud cover renders optical satellites (MODIS, Sentinel-2 MSI) unusable for multi-week stretches.
- **Spatial Mismatch**: 250m MODIS pixels represent a blend of 5 to 20 smallholder plots, roads, ponds, and homestead trees (*mixed pixel problem*).
- **Assessment**: Valuable for regional benchmarking, seasonal comparisons, and dry-season monitoring (Rabi crops/Boro), but cannot be relied upon as a primary real-time operational trigger during the monsoon without SAR integration.
- **Evidence Level**: **Reasonable Interpretation (RI)** with documented optical cloud limitation.

---

### Problem 5: Field-Level Pest and Disease Outbreak Prediction (Rank 5)

#### 1. Problem and Agricultural Context
Pests such as Brown Planthopper (BPH), Rice Hispa, and fungal pathogens like *Pyricularia oryzae* (Rice Blast) and *Phytophthora infestans* (Potato Late Blight) cause massive seasonal crop damage.

#### 2. Evaluation & Priority Rationale
- **Scientific Reality**: Pathogen outbreaks depend heavily on field micro-climates (canopy humidity, leaf wetness duration, micro-spore load) and crop canopy density, which satellite sensors cannot directly observe.
- **Failure Mode**: Making automated pest-spray recommendations based purely on coarse gridded satellite weather risks either false alarms (unnecessary costly pesticide application) or missed outbreaks (crop destruction).
- **Assessment**: **Excluded from Phase 1/Phase 2 core scope**. Can only be explored in later phases (Phase 9+) as supportive climate-favorability risk indices in collaboration with DAE plant protection wings.
- **Evidence Level**: **Unverified Hypothesis (UH)** for satellite-only decision support.

---

## 4. Problem Prioritization Matrix

```mermaid
quadrantChart
    title Agricultural Problem Prioritization (Impact vs Feasibility)
    x-axis Low Feasibility via EO --> High Feasibility via EO
    y-axis Low User Value --> High User Value
    quadrant-1 Immediate Core Focus (Phase 1-2 Scope)
    quadrant-2 High Value but High Complexity (Future Research)
    quadrant-3 Low Priority / Excluded
    quadrant-4 Secondary Features (Later Phases)
    "Waterlogging & Flash-Flood Inundation": [0.85, 0.92]
    "Irrigation & Dry-Spell Deficit": [0.82, 0.88]
    "Sowing & Harvest Timing Windows": [0.75, 0.82]
    "Vegetative Condition Anomalies": [0.65, 0.60]
    "Field-Level Pest & Disease Outbreaks": [0.25, 0.70]
    "Autonomous Field Control": [0.15, 0.30]
```

---

## 5. Summary & Problem Definition Baseline

Ritucast will concentrate its initial product foundation on three high-leverage, evidence-backed problem areas:
1. **Pre-monsoon and monsoon waterlogging / flash-flood early risk indicators** (protecting haor and lowland crops).
2. **Crop water deficit and irrigation timing decision support** (conserving groundwater and optimizing input costs in water-stressed regions).
3. **Weather-synchronized planting and harvest operational windows** (improving crop establishment and harvest quality).

All claims regarding direct field-level disease diagnosis, individual-field micro-yield guarantees, and autonomous controls are explicitly rejected from the core problem scope.
