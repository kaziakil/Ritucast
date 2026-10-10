# Ritucast: Phase 9 Analytics Integration Contract

## 1. Integration Scope & Mission

The Backend API does not reimplement agricultural equations, physical threshold rules, or suppression logic. Instead, it integrates directly with the verified classes and modules authored in [Phase 9](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-09/validation-report.md).

---

## 2. Integrated Modules & Functional Contracts

### 2.1 Context Gating (`analytics/engine/context_gate.py`)
- **Class**: `ContextGator`
- **Method**: `validate_context(upazila_id, crop_name, growth_stage)`
- **Contract**: Ensures Upazila is in `VALID_PILOT_UPAZILAS` (`BD-50-20-30`, `BD-50-20-90`, `BD-60-90-86`, `BD-60-90-89`), crop is in `VALID_CROPS` (`BORO RICE`, `BORO`), and stage is non-empty. Raises `ContextGatingError` on failure.

### 2.2 Evapotranspiration & Water Balance (`analytics/indicators/`)
- **`PenmanMonteithCalculator`**: Evaluates FAO-56 equation (`EQN-ET0-01`) using temperature, relative humidity, wind speed, and solar radiation.
- **`CropWaterDemandCalculator`**: Maps crop stage to BRRI-calibrated $K_c$ (`EQN-ETC-01`).
- **`SoilWaterDeficitCalculator`**: Computes daily root-zone water balance $D_t$ (`EQN-SWD-01`) with TAW and RAW thresholds.

### 2.3 Haor Flash Flood Hazard Index (`analytics/indicators/haor_flood_index.py`)
- **Class**: `HaorFloodIndexCalculator`
- **Method**: `calculate_index(catchment_id, date_str, p_cat_48h_mm, water_level_m, rate_of_rise_24h_m, inundation_fraction)`
- **Contract**: Evaluates composite index $I_{\text{flood}}$ (`IDX-FLD-01`) based on Meghalaya rainfall and Surma river gauge elevation.

### 2.4 Master Recommendation Engine (`analytics/engine/advisory_engine.py`)
- **Class**: `AgriculturalRecommendationEngine`
- **Method**: `evaluate_all_rules(upazila_id, crop_name, growth_stage, inputs, ...)`
- **Contract**: Executes all active rules:
  - `RuleIrrigationPostponement` (`RULE-IRR-01`)
  - `RuleMoistureDeficitAlert` (`RULE-IRR-02`)
  - `RuleHaorEmergencyHarvest` (`RULE-FLD-01`)
  - `RuleBootingColdInjury` (`RULE-TMP-01`)
  - `RuleAnthesisHeatStress` (`RULE-TMP-02`)
  Applies automated suppression middleware (`AdvisorySuppressionEngine`) per `DEC-10`.

---

## 3. Data Transformation & Output Serialization

The repository transforms Phase 9 `AdvisoryCard` domain objects into API response payloads (`AdvisoryResponse`), appending:
- Bengali localized category and stage labels.
- Standardized rationale breakdowns.
- Mandatory field verification warnings.
- Immutable data provenance metadata.

---

## 4. Related Documentation

- Architecture: [phase-10-backend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md)
- Phase 9 Completion: [validation-report.md](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-09/validation-report.md)
