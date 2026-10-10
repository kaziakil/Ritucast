# Ritucast: API & Component Contracts Specification (OpenAPI 3.0)

## 1. Executive Summary & Design Principles

The Ritucast Application Programming Interface (API) is designed as a clean, versioned, RESTful interface adhering to the **OpenAPI 3.0** specification. It exposes structured endpoints that serve the mobile client Progressive Web App (PWA) and authorized extension services.

### Core API Design Principles:
1. **Four-Tier Information Separation (`DEC-08`)**: Response payloads maintain explicit key-level separation for `tier_1_observations`, `tier_2_indicators`, `tier_3_predictions`, and `tier_4_recommendation`.
2. **Mandatory Contextual Gating (`DEC-17`)**: Advisory requests **must require** `crop` and `stage` query parameters; queries missing these parameters are rejected with HTTP 422.
3. **Traceability by Default**: Every advisory payload includes an immutable `provenance` metadata block recording Rule ID, data timestamps, and equation semantic versions.
4. **Lightweight Payloads**: Response payloads are minified and compressed ($<15\text{KB}$ uncompressed) to preserve client 3G data budgets (`DEC-09`).

---

## 2. API Endpoint Architecture & Contracts

```mermaid
graph LR
    Client[Client PWA / Extension Tool] --> Ingress[Cloud CDN / Load Balancer]
    
    subgraph API_Endpoints[Ritucast REST API v1]
        Ingress --> EP1[GET /api/v1/upazilas<br>List pilot upazilas]
        Ingress --> EP2[GET /api/v1/upazilas/{id}/weather<br>Tier 1 & Tier 3 Weather]
        Ingress --> EP3[GET /api/v1/upazilas/{id}/water-balance<br>Tier 2 ET0 & Deficit Dt]
        Ingress --> EP4[GET /api/v1/upazilas/{id}/flood-hazard<br>Tier 2 Haor Flood Index]
        Ingress --> EP5[GET /api/v1/upazilas/{id}/advisories<br>Tier 4 Actionable Recommendation]
    end
```

---

### 2.1 Endpoint 1: Upazila Catalog (`GET /api/v1/upazilas`)
- **Summary**: Returns list of authorized pilot upazilas with geographic centroids and AEZ metadata.
- **Request**: `GET /api/v1/upazilas`
- **Response (`200 OK`)**:
```json
{
  "status": "success",
  "count": 4,
  "data": [
    {
      "upazila_id": "BD-50-28",
      "name_en": "Godagari",
      "name_bn": "গোদাগাড়ী",
      "district_name": "Rajshahi",
      "division_name": "Rajshahi",
      "aez_code": 26,
      "aez_name": "High Barind Tract",
      "centroid": { "lat": 24.4667, "lon": 88.3300 },
      "primary_risk": "DROUGHT_IRRIGATION"
    },
    {
      "upazila_id": "BD-60-90",
      "name_en": "Tahirpur",
      "name_bn": "তাহিরপুর",
      "district_name": "Sunamganj",
      "division_name": "Sylhet",
      "aez_code": 21,
      "aez_name": "Sylhet Basin (Haor)",
      "centroid": { "lat": 25.1000, "lon": 91.1800 },
      "primary_risk": "FLASH_FLOOD"
    }
  ]
}
```

---

### 2.2 Endpoint 2: Upazila Weather Feed (`GET /api/v1/upazilas/{upazila_id}/weather`)
- **Summary**: Returns 7-day historical observations (Tier 1) and 7-day probabilistic forecasts (Tier 3).
- **Request**: `GET /api/v1/upazilas/BD-50-28/weather`
- **Response (`200 OK`)**:
```json
{
  "upazila_id": "BD-50-28",
  "name_bn": "গোদাগাড়ী",
  "timezone": "Asia/Dhaka",
  "tier_1_observations": {
    "source": "NASA POWER / BMD Station #41926",
    "updated_at_bst": "2026-10-10T09:00:00+06:00",
    "yesterday": {
      "date": "2026-10-09",
      "temp_max_c": 32.4,
      "temp_min_c": 22.1,
      "solar_radiation_mj_m2": 18.2,
      "precip_24h_mm": 0.0,
      "rh_mean_pct": 68
    }
  },
  "tier_3_forecasts": {
    "model_sources": ["ECMWF IFS 9km", "NOAA GFS 13km"],
    "issued_at_bst": "2026-10-10T12:00:00+06:00",
    "ensemble_spread_pct": 18.5,
    "daily_forecast": [
      {
        "date": "2026-10-11",
        "lead_time_h": 24,
        "temp_max_c": 33.0,
        "temp_min_c": 22.5,
        "qpf_precip_mm": 24.5,
        "precip_probability_pct": 75,
        "confidence": "HIGH"
      },
      {
        "date": "2026-10-12",
        "lead_time_h": 48,
        "temp_max_c": 30.5,
        "temp_min_c": 21.0,
        "qpf_precip_mm": 12.0,
        "precip_probability_pct": 65,
        "confidence": "MODERATE"
      }
    ]
  }
}
```

---

### 2.3 Endpoint 3: Upazila Water Balance (`GET /api/v1/upazilas/{upazila_id}/water-balance`)
- **Summary**: Returns FAO-56 Reference Evapotranspiration ($ET_0$) and daily soil water deficit ($D_t$) for Barind upazilas.
- **Request**: `GET /api/v1/upazilas/BD-50-28/water-balance?crop=boro_rice&stage=vegetative_tillering`
- **Response (`200 OK`)**:
```json
{
  "upazila_id": "BD-50-28",
  "crop_id": "boro_rice",
  "growth_stage": "vegetative_tillering",
  "tier_2_indicators": {
    "calculation_date": "2026-10-10",
    "fao56_et0_mm_day": 4.25,
    "calibrated_kc": 1.15,
    "crop_etc_mm_day": 4.89,
    "soil_properties": {
      "texture": "Heavy Silty Clay",
      "root_zone_depth_m": 0.40,
      "total_available_water_taw_mm": 56.0,
      "readily_available_water_raw_mm": 19.6
    },
    "current_soil_water_deficit_dt_mm": 16.4,
    "status": "AWD_DRYING_PERMISSIBLE",
    "status_bn": "মাটিতে পর্যাপ্ত রস রয়েছে (এডাব্লিউডি কার্যকর)"
  }
}
```

---

### 2.4 Endpoint 4: Upazila Flood Hazard (`GET /api/v1/upazilas/{upazila_id}/flood-hazard`)
- **Summary**: Returns Haor Flash-Flood Hazard Index ($I_{\text{flood}}$) combining Meghalaya rain and Surma river gauge status.
- **Request**: `GET /api/v1/upazilas/BD-60-90/flood-hazard`
- **Response (`200 OK`)**:
```json
{
  "upazila_id": "BD-60-90",
  "name_bn": "তাহিরপুর",
  "tier_2_indicators": {
    "evaluation_timestamp_bst": "2026-10-10T14:00:00+06:00",
    "flood_hazard_index_iflood": 0.78,
    "hazard_tier": "EMERGENCY",
    "hazard_tier_bn": "জরুরি সতর্কতা (লাল)",
    "sub_indices": {
      "meghalaya_catchment_48h_rain_mm": 135.0,
      "surma_river_stage_m": 8.45,
      "surma_danger_level_m": 8.25,
      "surma_rate_of_rise_m_day": 0.85,
      "sentinel1_sar_inundation_pct": 28.5
    },
    "trigger_early_harvest": true
  }
}
```

---

### 2.5 Endpoint 5: Core Advisory Service (`GET /api/v1/upazilas/{upazila_id}/advisories`)
- **Summary**: Primary recommendation endpoint generating 4-Tier decision cards.
- **Request**: `GET /api/v1/upazilas/BD-50-28/advisories?crop=boro_rice&stage=vegetative_tillering`
- **Mandatory Query Parameters**:
  - `crop` (String): e.g., `boro_rice`
  - `stage` (String): e.g., `vegetative_tillering`, `flowering_anthesis`, `dough_maturity`
- **Response (`200 OK`)**:
```json
{
  "upazila_id": "BD-50-28",
  "upazila_name_bn": "গোদাগাড়ী",
  "crop_id": "boro_rice",
  "crop_name_bn": "বোরো ধান",
  "growth_stage": "vegetative_tillering",
  "growth_stage_bn": "কুশি পর্যায় (বৃদ্ধি)",
  "generated_at_bst": "2026-10-10T14:30:00+06:00",
  
  "tier_1_observations": {
    "summary_bn": "বিগত ৭ দিনে মোট ১৮ মিমি বৃষ্টি হয়েছে; গড় তাপমাত্রা ২৮.৫° সে."
  },
  
  "tier_2_indicators": {
    "summary_bn": "মাটিতে পানির ঘাটতি ১৬.৪ মিমি; দৈনিক বাষ্পীভবন ৪.৯ মিমি"
  },
  
  "tier_3_predictions": {
    "summary_bn": "আগামী ৪৮ ঘণ্টায় ৭৫% সম্ভাবনায় ২৫-৩৫ মিমি বৃষ্টির পূর্বাভাস রয়েছে"
  },
  
  "tier_4_recommendation": {
    "rule_id": "RULE-IRR-01",
    "category": "IRRIGATION",
    "action_code": "POSTPONE_IRRIGATION",
    "headline_bn": "সেচ স্থগিত রাখুন (পরামর্শ)",
    "body_bn": "আগামী ৪৮ থেকে ৭২ ঘণ্টার মধ্যে আপনার এলাকায় উল্লেখযোগ্য বৃষ্টির সম্ভাবনা রয়েছে (আনুমানিক ২০–৩৫ মিমি)। অগভীর বা গভীর নলকূপ চালু করার আগে অপেক্ষা করুন। বৃষ্টি হলে সেচের খরচ সাশ্রয় হবে।",
    "mandatory_disclaimer_bn": "সেচ বন্ধ রাখার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।",
    "rationale_breakdown": {
      "why_bn": "আগামীকালের সম্ভাব্য বৃষ্টিপাত বর্তমান মাটির ঘাটতি পূরণ করতে সক্ষম। এখন সেচ দিলে জ্বালানি অপচয় হবে ও সার ধুয়ে যেতে পারে।",
      "pumping_savings_est_bdt": "১২০০-১৫০০ টাকা/হেক্টর"
    },
    "confidence": {
      "score": 0.82,
      "tier": "HIGH",
      "tier_bn": "উচ্চ নির্ভরযোগ্যতা",
      "color_hex": "#2e7d32"
    },
    "is_suppressed": false
  },
  
  "provenance": {
    "ruleset_version": "1.0.0",
    "equations_used": ["EQN-ET0-01", "EQN-ETC-01", "EQN-SWD-01"],
    "weather_data_age_hours": 3.5,
    "suppression_check": "PASSED"
  }
}
```

---

## 3. Standardized Error Responses & Error Codes

All error responses return standard JSON envelopes with machine-readable error codes:

| HTTP Status | Error Code (`code`) | Trigger Condition | Example Error Response Payload |
| :--- | :--- | :--- | :--- |
| **`422 Unprocessable Entity`** | `MISSING_CONTEXT_PARAMETER` | Missing `crop` or `stage` query parameter (`DEC-17`). | `{"status": "error", "code": "MISSING_CONTEXT_PARAMETER", "message": "Field 'crop' and 'stage' are required for advisory generation."}` |
| **`422 Unprocessable Entity`** | `OUT_OF_SEASON_CROP` | Crop queried outside biologically viable months. | `{"status": "error", "code": "OUT_OF_SEASON_CROP", "message": "Selected crop is biologically inactive in current calendar month."}` |
| **`404 Not Found`** | `UPAZILA_NOT_FOUND` | Queried Upazila ID not in the database. | `{"status": "error", "code": "UPAZILA_NOT_FOUND", "message": "Upazila 'BD-99-99' not recognized."}` |
| **`429 Too Many Requests`** | `RATE_LIMIT_EXCEEDED` | Request rate $>60\text{ req/min}$ from IP. | `{"status": "error", "code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests. Retry after 60 seconds."}` |
| **`200 OK (Suppressed Fallback)`** | `STALE_DATA_SUPPRESSED` | Weather forecast data is $>36\text{ hours}$ old (`DEC-10`). | Returns `200 OK` with `is_suppressed: true`, headline: *"তথ্য হালনাগাদ হচ্ছে"*, and fallback copy directing to SAAO. |
