# Data Contracts and Schemas — Ritucast System Integration

## 1. Overview

This document specifies the authoritative contracts and schemas governing data exchange between the data pipeline, the backend API, and the client frontend.

---

## 2. Parquet Feature Table Schemas

### 2.1 `weather_daily.parquet`
| Column Name | Data Type | Nullable | Units / Format | Description |
| :--- | :--- | :--- | :--- | :--- |
| `upazila_id` | String | No | BBS Code (`BD-XX-XX-XX`) | Administrative Upazila identifier |
| `date` | Date / String | No | ISO-8601 `YYYY-MM-DD` | Observation date |
| `temp_max_c` | Float32 | No | $^\circ\text{C}$ | Daily maximum temperature |
| `temp_min_c` | Float32 | No | $^\circ\text{C}$ | Daily minimum temperature |
| `temp_mean_c` | Float32 | No | $^\circ\text{C}$ | Daily mean temperature |
| `rh_mean_pct` | Float32 | No | $\%$ | Daily mean relative humidity ($0–100$) |
| `wind_speed_2m_ms` | Float32 | No | $\text{m/s}$ | Daily wind speed at 2m height |
| `solar_radiation_mj_m2` | Float32 | No | $\text{MJ/m}^2/\text{day}$ | Downward surface solar radiation |
| `precipitation_mm` | Float32 | No | $\text{mm}$ | Total daily precipitation |
| `source_dataset` | String | No | Enum | Source identifier (`DATA-MET-01`, `DATA-FCST-01`) |

### 2.2 `flood_hazard_daily.parquet`
| Column Name | Data Type | Nullable | Units / Format | Description |
| :--- | :--- | :--- | :--- | :--- |
| `upazila_id` | String | No | BBS Code | Must belong to AEZ-21 for valid index |
| `date` | Date / String | No | ISO-8601 | Observation timestamp |
| `meghalaya_rain_mm` | Float32 | No | $\text{mm}$ | 48h accumulated upstream rainfall ($f_P$) |
| `surma_river_stage_m`| Float32 | No | $\text{m}$ | BWDB river stage level ($f_S$) |
| `sar_inundation_pct` | Float32 | No | $\%$ | Sentinel-1 SAR inundation fraction ($f_I$) |
| `soil_saturation_index`| Float32 | No | Ratio ($0–1$) | Antecedent soil moisture saturation ($f_M$) |
| `flood_hazard_index` | Float32 | No | Ratio ($0–1$) | Computed composite index $I_{\text{flood}}$ |
| `early_harvest_alert`| Boolean | No | True / False | Triggered when $I_{\text{flood}} \ge 0.75$ |

---

## 3. Backend REST API Request/Response Schemas

### 3.1 Advisory Response Schema (`/api/v1/upazilas/{id}/advisories`)
```json
{
  "upazila_id": "BD-50-20-30",
  "upazila_name_bn": "গোদাগাড়ী",
  "crop_id": "boro_rice",
  "crop_name_bn": "বোরো ধান",
  "growth_stage": "panicle_initiation",
  "growth_stage_bn": "শীষ আসার সূচনা",
  "generated_at_bst": "2026-10-10 12:00:00 BST",
  "tier_1_observations": {
    "summary_bn": "গত ৭ দিনে মোট ৫.২ মিমি বৃষ্টিপাত হয়েছে।",
    "rainfall_7d_total_mm": 5.2,
    "mean_temp_c": 26.5
  },
  "tier_2_indicators": {
    "summary_bn": "মাটির আর্দ্রতা ঘাটতি ২৪.০ মিমি।",
    "soil_water_deficit_dt_mm": 24.0,
    "fao56_et0_mm_day": 3.8
  },
  "tier_3_predictions": {
    "summary_bn": "আগামী ৪৮ ঘণ্টায় মাঝারি বৃষ্টির সম্ভাবনা (৬৫%)।",
    "rain_probability_48h_pct": 65.0,
    "qpf_48h_mm": 18.0
  },
  "tier_4_recommendation": {
    "rule_id": "RULE-IRR-01",
    "category": "IRRIGATION_SCHEDULING",
    "action_code": "POSTPONE_IRRIGATION",
    "severity": "ADVISORY",
    "headline_bn": "আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন",
    "body_bn": "মাঝারি বৃষ্টির সম্ভাবনা থাকায় সেচ স্থগিত রাখা যুক্তিযুক্ত।",
    "mandatory_disclaimer_bn": "সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।",
    "action_items_bn": [
      "পাম্প বন্ধ রাখুন",
      "আইলের পানি ধরে রাখার ব্যবস্থা নিন"
    ],
    "rationale_breakdown": {
      "scientific_basis": "FAO-56 গণনা অনুযায়ী সম্ভাব্য বৃষ্টিপাত মাটির আর্দ্রতা পূরণ করবে।"
    },
    "confidence": {
      "score": 0.88,
      "tier": "HIGH",
      "tier_bn": "উচ্চ নির্ভরযোগ্যতা",
      "color_hex": "#15803D"
    },
    "is_suppressed": false
  },
  "provenance": {
    "engine_version": "1.0.0",
    "pilot_zone": "High Barind Tract"
  }
}
```

### 3.2 Standard Error Response Envelope
Every backend error response strictly adheres to the standard error envelope:
```json
{
  "code": "REQUEST_VALIDATION_ERROR",
  "message": "Invalid query parameters: growth stage is required for advisory calculation.",
  "status": 422,
  "timestamp": "2026-10-10T11:00:00Z",
  "details": {
    "missing_fields": ["stage"]
  }
}
```
Standard Error Codes:
- `REQUEST_VALIDATION_ERROR` (HTTP 422): Contextual gating violations (`DEC-17`).
- `RESOURCE_NOT_FOUND` (HTTP 404): Non-existent or non-pilot Upazila code.
- `ADVISORY_SUPPRESSED` (HTTP 200 or 503): Safe fallback notice when input data exceeds 36h latency (`DEC-10`).
- `RATE_LIMIT_EXCEEDED` (HTTP 429): Client exceeding request quota.
- `INTERNAL_SERVER_ERROR` (HTTP 500): Sanitized error message without leaking Python stack traces.
