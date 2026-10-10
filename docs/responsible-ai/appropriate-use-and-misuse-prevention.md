# Appropriate Use, Misuse Prevention, and Non-Goals — Ritucast

## 1. Executive Mission & Appropriate Use

**Ritucast** is designed exclusively as an **informational decision-support tool** to help smallholders, lead farmers, and Sub-Assistant Agriculture Officers (SAAOs) make better-informed day-to-day farming choices regarding irrigation scheduling and seasonal harvest timing.

The platform assists farmers in:
1. Postponing unnecessary groundwater pumping when rain is imminent.
2. Identifying critical soil moisture deficit during tillering or panicle initiation.
3. Taking early harvesting measures when pre-monsoon flash floods threaten Haor Boro rice.
4. Monitoring agro-meteorological anomalies across authorized pilot Upazilas.

---

## 2. Strict Project Scope Non-Goals (`DEC-06`, `AGENTS.md`)

To protect scientific integrity and avoid creating misleading dependencies, Ritucast establishes clear, immutable non-goals:

```
+-------------------------------------------------------------------------------+
|                        STRICT PROJECT NON-GOALS (DEC-06)                      |
+-------------------------------------------------------------------------------+
| [X] NO Parcel-Level Yield Prediction (MOD-YLD-01):                            |
|     Ritucast does NOT predict kilogram-per-bigha harvest yields for plots.    |
|                                                                               |
| [X] NO Automated Chemical Pesticide Diagnosis (MOD-DIS-01):                  |
|     Ritucast does NOT diagnose crop pests from satellite pixels.              |
|                                                                               |
| [X] NO Remote Hardware Actuation:                                             |
|     Ritucast has ZERO IoT switches or tubewell pump controls.                 |
|                                                                               |
| [X] NO Financial Underwriting or Credit Scoring:                              |
|     Ritucast risk indexes must NOT be used to deny loans or insurance.        |
|                                                                               |
| [X] NO Commercial Brand Endorsements:                                         |
|     Ritucast NEVER recommends branded agrochemicals or commercial inputs.     |
+-------------------------------------------------------------------------------+
```

---

## 3. Misuse Prevention: Financial & Institutional Safeguards

### 3.1 Prohibition of Loan Underwriting Misuse
- **Threat Scenario**: A rural microfinance institution (MFI) or commercial bank queries Ritucast's Upazila drought index or flood hazard index to deny micro-loans or credit to a farmer whose land falls within an affected Upazila.
- **Scientific Limitation**: Regional agro-meteorological indicators do **not** reflect a farmer's individual solvency, creditworthiness, or specific field management practices (e.g. access to private low-lift pumps or farm ponds).
- **Mandatory Policy & Disclaimer**:
  All risk assessment endpoints ([`api/routers/risk.py`](file:///Users/kazi/Projects/RITUCAST/api/routers/risk.py#L31)) and responses carry the explicit legal disclaimer:
  > *"এই মূল্যায়ন শুধুমাত্র প্রাকৃতিক পরিবেশগত ঝুঁকির নির্দেশক; এটি আর্থিক ক্ষতি বা চূড়ান্ত ফলন হ্রাসের নিশ্চয়তা দেয় না।"*
  *(This assessment is an indicator of natural environmental hazard only; it does not guarantee financial loss or final crop yield outcome.)*

### 3.2 Prohibition of Insurance Denial Misuse
- Regional hazard scores must not be treated as parcel-level loss adjusters. An insurance payout or claim rejection requires on-the-ground crop cutting experiments (CCE) or official government damage surveys by the Department of Agricultural Extension (DAE).

---

## 4. Operational Fallback & Human-in-the-Loop Safeguards

1. **Local Agronomist Supremacy**: Digital advice from Ritucast serves to augment, never supplant, the expert judgment of Upazila Agriculture Officers (UAOs) and SAAOs.
2. **Farmer Intuition Primacy**: As emphasized in every advisory card, the farmer's tactile inspection of field soil moisture takes precedence over satellite estimates.

Related documentation:
- [`docs/responsible-ai/agricultural-recommendation-safeguards.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/agricultural-recommendation-safeguards.md)
- [`docs/responsible-ai/model-limitations-and-uncertainty.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/model-limitations-and-uncertainty.md)
- [`docs/responsible-ai/geographic-coverage-and-fairness.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/geographic-coverage-and-fairness.md)
