# Analytics Output Contracts & Data Schemas — Ritucast

## 1. Executive Summary & Purpose

This document specifies the formal data contracts, Pydantic v2 models, and JSON schemas produced by Phase 9 for consumption by [Phase 10: Backend and API Development](file:///Users/kazi/Projects/RITUCAST/docs/planning/roadmap.md).

All contracts are implemented in [indicator_schemas.py](file:///Users/kazi/Projects/RITUCAST/analytics/contracts/indicator_schemas.py) and [advisory_schemas.py](file:///Users/kazi/Projects/RITUCAST/analytics/contracts/advisory_schemas.py).

---

## 2. Descriptive Climatology Schema (`DescriptiveAgroclimaticSummary`)

```json
{
  "upazila_id": "BD-50-20-30",
  "start_date": "2026-03-01",
  "end_date": "2026-03-31",
  "days_count": 31,
  "mean_t2m_c": 26.4,
  "max_t2m_c": 36.2,
  "min_t2m_c": 18.5,
  "cumulative_precipitation_mm": 18.4,
  "mean_solar_rad_mj_m2": 21.8,
  "mean_rh2m_pct": 58.2,
  "completeness_pct": 100.0
}
```

---

## 3. Physical Indicator Schemas

### 3.1 Reference Evapotranspiration (`ReferenceET0Result`)
```json
{
  "upazila_id": "BD-50-20-30",
  "date": "2026-03-15",
  "et0_mm_day": 5.12,
  "elevation_m": 20.0,
  "net_radiation_mj_m2": 12.87,
  "vapor_pressure_deficit_kpa": 0.98,
  "method": "FAO-56 Penman-Monteith",
  "quality_flag": "VALID"
}
```

### 3.2 Crop Water Demand (`CropWaterDemandResult`)
```json
{
  "upazila_id": "BD-50-20-30",
  "date": "2026-03-15",
  "crop_name": "Boro Rice",
  "growth_stage": "Tillering",
  "kc_current": 1.15,
  "et0_mm_day": 5.12,
  "etc_mm_day": 5.89
}
```

### 3.3 Root-Zone Soil Water Deficit (`SoilWaterDeficitResult`)
```json
{
  "upazila_id": "BD-50-20-30",
  "date": "2026-03-15",
  "crop_name": "Boro Rice",
  "growth_stage": "Tillering",
  "depletion_mm": 14.5,
  "taw_mm": 56.0,
  "raw_mm": 19.6,
  "effective_rain_mm": 0.0,
  "irrigation_applied_mm": 0.0,
  "is_stress_critical": false,
  "storage_capacity_remaining_mm": 41.5
}
```

### 3.4 Haor Flash Flood Hazard Score (`HaorFloodIndexResult`)
```json
{
  "catchment_id": "BWDB-177",
  "date": "2026-04-18",
  "i_flood": 0.88,
  "hazard_tier": "EMERGENCY",
  "p_cat_48h_mm": 140.0,
  "water_level_m_pwd": 8.50,
  "rate_of_rise_24h_m": 0.90,
  "inundation_fraction": 0.30,
  "sub_indices": {
    "f_P": 0.917,
    "f_S": 1.0,
    "f_R": 0.875,
    "f_I": 0.75
  }
}
```

---

## 4. Master Advisory Recommendation Card Schema (`AdvisoryCard`)

Conforms strictly to the 5-section recommendation card anatomy (`DEC-30`):

```json
{
  "advisory_id": "ADV-IRR01-BD-50-20-30-2026-03-15",
  "rule_id": "RULE-IRR-01",
  "upazila_id": "BD-50-20-30",
  "crop_name": "Boro Rice",
  "growth_stage": "Tillering",
  "timestamp_utc": "2026-03-15T06:00:00Z",
  "valid_until_utc": "2026-03-17T06:00:00Z",
  "severity": "ADVISORY",
  "status": "ACTIVE",
  "headline_bn": "সেচ স্থগিত রাখুন (পরামর্শ)",
  "plain_language_bn": "আগামী ৪৮ থেকে ৭২ ঘণ্টার মধ্যে আপনার এলাকায় উল্লেখযোগ্য বৃষ্টির সম্ভাবনা রয়েছে (সম্ভাবনা ৭৫%, আনুমানিক ২৫ মিমি)। নলকূপ চালু করার আগে অপেক্ষা করুন। বৃষ্টি হলে সেচের জ্বালানি খরচ সাশ্রয় হবে।",
  "action_items_bn": [
    "পরবর্তী ৪৮ ঘণ্টা গভীর বা অগভীর নলকূপ চালু করা স্থগিত রাখুন।",
    "জমির আইল ভালোভাবে মেরামত করুন যাতে বৃষ্টির পানি জমিতে ধরে রাখা যায়।",
    "যদি বৃষ্টি ২০ মিলিমিটারের কম হয়, তবে মাটির আর্দ্রতা পরীক্ষা করে সেচ দিন।"
  ],
  "field_verification_bn": "সেচ বন্ধ রাখার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন। যদি জমি ইতিমধ্যে ফেটে গিয়ে থাকে, তবে হালকা পানি দিন।",
  "uncertainty_description_bn": "আবহাওয়া মডেলের পূর্বাভাসের বিস্তার ২০%। পূর্বাভাসে স্বাভাবিক অনিশ্চয়তা বিদ্যমান থাকায় সরাসরি মাঠ পর্যবেক্ষণ বাঞ্ছনীয়।",
  "suppression_reason": null,
  "supporting_indicators": {
    "qpf_48h_mm": 25.0,
    "rain_prob_pct": 75.0,
    "soil_depletion_mm": 10.0,
    "taw_mm": 56.0,
    "ensemble_spread_pct": 20.0
  },
  "provenance_manifest": {
    "forecast_model": "ECMWF-IFS/Open-Meteo",
    "agroclimatology": "NASA-POWER/FAO-56"
  }
}
```
