# Ritucast: Backend API Specification (OpenAPI 3.0)

## 1. Scope & Protocol Standards

The Ritucast API exposes RESTful endpoints over HTTP/1.1 and HTTP/2, returning JSON payloads conforming to the OpenAPI 3.0 specification.

The official OpenAPI 3.0 specification artifact is generated directly from the codebase at:
[openapi.json](file:///Users/kazi/Projects/RITUCAST/docs/backend/openapi.json).

### Base URLs & Prefixes
- Development: `http://localhost:8000`
- API v1 Prefix: `/api/v1`
- Documentation UI: `/docs` (Swagger UI) and `/redoc` (ReDoc)
- Machine-Readable Spec: `/openapi.json`

---

## 2. Information Taxonomy Architecture (`DEC-08`)

Every response containing agronomic data enforces strict top-level separation across four tiers:

| Tier | Category | Bangla Descriptor | Underlying Data Source / Methodology |
| :--- | :--- | :--- | :--- |
| **Tier 1** | Empirical Observations | পর্যবেক্ষণ | NASA POWER, BMD Station Observations, Sentinel-1 SAR Backscatter |
| **Tier 2** | Derived Agronomic Indicators | হিসাবকৃত সূচক | FAO-56 Penman-Monteith $ET_0$, Soil Deficit $D_t$, Haor Flood Index $I_{\text{flood}}$ |
| **Tier 3** | Probabilistic Predictions | পূর্বাভাস | ECMWF IFS 9km, NOAA GFS, Ensemble Spread Metrics |
| **Tier 4** | Actionable Recommendations | পরামর্শ | Context-Gated Advisory Cards (`RULE-IRR-01`, `RULE-FLD-01`, etc.) |

---

## 3. Mandatory Contextual Gating (`DEC-17`)

Per `DEC-17`, advisory endpoints reject queries missing any of the three core contextual parameters:
1. `upazila_id`: Administrative Upazila code (must be within approved pilot testbeds).
2. `crop`: Crop identifier (pilot anchor: Boro rice).
3. `stage`: Validated phenological growth stage.

Requests lacking these parameters will fail with `HTTP 422 Unprocessable Entity` and error code `CONTEXT_GATING_FAILED`.

---

## 4. Automated Suppression Standards (`DEC-10`)

When data freshness or meteorological spread thresholds are exceeded:
- Endpoint returns `HTTP 200 OK`.
- `tier_4_recommendation.is_suppressed` is set to `true`.
- Headline is replaced with `"পরামর্শ সাময়িকভাবে স্থগিত"` or `"তথ্য হালনাগাদ হচ্ছে"`.
- Body text directs farmer to local Sub-Assistant Agriculture Officer (SAAO) fallback:
  > *"পূর্বাভাস ডেটার বয়স ৩৬ ঘণ্টার বেশি হওয়ায় পরামর্শটি সাময়িকভাবে স্থগিত রাখা হয়েছে। মাঠের অবস্থা যাচাইয়ের জন্য আপনার উপসহকারী কৃষি কর্মকর্তার সাথে যোগাযোগ করুন।"*

---

## 5. Anti-Overconfidence Safeguards

1. **Banned Terminology**: No endpoint may emit *"১০০% নিশ্চিত"*, *"নিশ্চিত বৃষ্টি"*, or *"ফলনের নিশ্চয়তা"*.
2. **Mandatory Verification Copy**: Every advisory must carry:
   > *"সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*

---

## 6. Related Specifications

- Architecture: [phase-10-backend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md)
- Endpoints Catalog: [api-endpoints.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/api-endpoints.md)
- Validation & Errors: [request-validation-and-errors.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/request-validation-and-errors.md)
