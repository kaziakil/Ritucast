# Phase 9 to Phase 10 Technical Handoff: Backend and API Development

## 1. Executive Summary & Purpose

This handoff document transitions the **Ritucast** project from **Phase 9: Agricultural Analytics and Recommendation Engine** to **Phase 10: Backend and API Development**.

It provides incoming backend engineers with a complete integration blueprint, Python interfaces, Pydantic data contracts, and operational guidelines necessary to expose Ritucast's analytical capabilities through REST and WebSocket APIs without re-implementing scientific logic or inventing ad-hoc schemas.

---

## 2. Inventory of Implemented Analytics Interfaces

Phase 10 services should import directly from the tested `analytics` package:

```mermaid
flowchart LR
    subgraph Phase10_API [Phase 10 FastAPI Layer]
        EP1[GET /api/v1/climatology/{upazila_id}]
        EP2[GET /api/v1/indicators/et0/{upazila_id}]
        EP3[GET /api/v1/indicators/water-balance/{upazila_id}]
        EP4[GET /api/v1/indicators/flood-index/{catchment_id}]
        EP5[POST /api/v1/advisories/evaluate]
    end

    subgraph Phase9_Modules [Phase 9 Analytics Core]
        M1[analytics.descriptive.ClimatologyAggregator]
        M2[analytics.indicators.PenmanMonteithCalculator]
        M3[analytics.indicators.SoilWaterDeficitCalculator]
        M4[analytics.indicators.HaorFloodIndexCalculator]
        M5[analytics.engine.AgriculturalRecommendationEngine]
    end

    EP1 --> M1
    EP2 --> M2
    EP3 --> M3
    EP4 --> M4
    EP5 --> M5
```

### 2.1 Invoking the Climatology Aggregator
```python
from analytics.descriptive import ClimatologyAggregator
import pandas as pd

df_met = pd.read_parquet("data/processed/meteorology_daily_upazila.parquet")
summary = ClimatologyAggregator.summarize_period(
    df_met=df_met,
    upazila_id="BD-50-20-30",
    start_date="2026-03-01",
    end_date="2026-03-31",
)
# Returns: DescriptiveAgroclimaticSummary instance
```

### 2.2 Invoking Physical Indicator Calculators
```python
from analytics.indicators import (
    PenmanMonteithCalculator,
    CropWaterDemandCalculator,
    SoilWaterDeficitCalculator,
    HaorFloodIndexCalculator,
)

# 1. FAO-56 ET0
et0_res = PenmanMonteithCalculator.calculate_et0(
    upazila_id="BD-50-20-30",
    date_str="2026-03-15",
    t_max_c=32.0,
    t_min_c=20.0,
    rh_mean_pct=60.0,
    wind_speed_2m_ms=2.2,
    solar_rad_mj_m2=21.5,
)

# 2. Crop Water Demand ETc
etc_res = CropWaterDemandCalculator.calculate_etc(
    upazila_id="BD-50-20-30",
    date_str="2026-03-15",
    et0_mm_day=et0_res.et0_mm_day,
    growth_stage="Tillering",
)

# 3. Daily Soil Water Balance Dt
swd_res = SoilWaterDeficitCalculator.step_daily_water_balance(
    upazila_id="BD-50-20-30",
    date_str="2026-03-15",
    d_prev_mm=10.0,
    etc_mm=etc_res.etc_mm_day,
    precip_mm=0.0,
    growth_stage="Tillering",
)

# 4. Haor Flash Flood Hazard Index Iflood
flood_res = HaorFloodIndexCalculator.calculate_index(
    catchment_id="BWDB-177",
    date_str="2026-04-18",
    p_cat_48h_mm=125.0,
    water_level_m=8.10,
    rate_of_rise_24h_m=0.65,
)
```

### 2.3 Invoking the Master Recommendation Engine
```python
from analytics.engine import AgriculturalRecommendationEngine, ContextGatingError

engine = AgriculturalRecommendationEngine()

try:
    advisories = engine.evaluate_all_rules(
        upazila_id="BD-50-20-30",
        crop_name="Boro Rice",
        growth_stage="Tillering",
        inputs={
            "qpf_48h_mm": 28.0,
            "rain_prob_pct": 75.0,
            "depletion_mm": 12.0,
            "taw_mm": 56.0,
            "ensemble_spread_pct": 20.0,
        },
        data_timestamp_utc="2026-03-15T00:00:00Z",
    )
    # Returns List[AdvisoryCard]
except ContextGatingError as e:
    # Phase 10 API should return HTTP 422 Unprocessable Entity with error detail
    pass
```

---

## 3. Strict Backend Integration Boundaries

1. **Mandatory Contextual Gating (`DEC-17`)**:
   - Phase 10 API endpoints must require `upazila_id`, `crop_name`, and `growth_stage` in query/body parameters for advisory endpoints. If any is missing, return HTTP 422 without calling rules.
2. **Preserve Card Anatomy Invariants (`DEC-30`)**:
   - The serialized JSON response for an advisory must include all 5 sections: headline, plain language Bengali text, action items, mandatory field verification copy, and uncertainty statement.
3. **What Phase 10 Must NOT Claim**:
   - Phase 10 API documentation and response schemas must **never** claim:
     - Sub-acre parcel yield predictions.
     - Disease classification from satellite bands.
     - 100% certainty or unconditional rain forecasts.
4. **Caching & Payload Budgets (`DEC-09`)**:
   - Computed indicator responses should be cached in Redis with a 1-hour TTL for static dates, and 15-minute TTL for real-time advisory evaluations.
