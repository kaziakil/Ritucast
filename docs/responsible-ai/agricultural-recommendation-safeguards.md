# Agricultural Recommendation Safeguards and Scientific Safety — Ritucast

## 1. Executive Summary

In agricultural decision support, algorithmic advice directly influences operational farm management, including irrigation pumping, tubewell fuel expenditure, drainage operations, and emergency crop harvesting. Misleading, overconfident, or uncalibrated guidance can result in catastrophic crop failure, groundwater waste, or unrecoverable financial debt for resource-poor smallholders in Bangladesh.

This document details the scientific safeguards, four-tier information separation, contextual gating, anti-overconfidence standards, and automated suppression policies governing **Ritucast**.

---

## 2. Four-Tier Information Taxonomy (`DEC-08`)

To prevent cognitive conflation between empirical facts, mathematical models, and operational advice, all Ritucast outputs are strictly categorized and visually separated into four distinct information tiers:

```
+-------------------------------------------------------------------------------+
| Tier 1: Empirical Observations (পর্যবেক্ষণ)                                  |
| Direct physical measurements: BMD rainfall, NASA solar radiation, SAR radar   |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| Tier 2: Derived Agronomic Indicators (হিসাবকৃত সূচক)                          |
| Deterministic physical equations: FAO-56 Penman-Monteith ET0, Soil Deficit Dt |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| Tier 3: Probabilistic Predictions (পূর্বাভাস)                                 |
| Forecasts with explicit probabilities and confidence bands (e.g. Rain 75%)   |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| Tier 4: Actionable Recommendations (পরামর্শ)                                  |
| Synthesized operational guidance with plain-language Bangla action items      |
| + Mandatory Ground-Verification Copy (DEC-10)                                 |
+-------------------------------------------------------------------------------+
```

1. **Tier 1 (Empirical Observations)**: Ground-truth sensor telemetry or satellite observations without model interpretation.
2. **Tier 2 (Derived Agronomic Indicators)**: Deterministic physical balance calculations (e.g., daily soil water balance, Haor flood index $I_{\text{flood}}$).
3. **Tier 3 (Probabilistic Predictions)**: Multi-model numerical weather predictions displaying explicit event probabilities ($P_{\text{rain}}$) and lead times (24h/48h).
4. **Tier 4 (Actionable Recommendations)**: Action directives synthesized from validated Phase 9 agronomic rules (`RULE-IRR-01` to `RULE-TMP-02`).

---

## 3. Mandatory Contextual Gating (`DEC-17`)

An agricultural advisory is scientifically invalid without local farming context. In Boro rice cultivation, irrigation postponement that is safe during the vegetative tillering stage can cause severe sterility if applied during flowering or anthesis.

- **Mandatory Triad**:
  1. Administrative Upazila (`upazila_id`)
  2. Active Crop (`crop_id`)
  3. Active Phenological Growth Stage (`growth_stage`)
- **Backend Gating**: Implemented in [`api/routers/advisories.py`](file:///Users/kazi/Projects/RITUCAST/api/routers/advisories.py#L37) and [`analytics/engine/context_gate.py`](file:///Users/kazi/Projects/RITUCAST/analytics/engine/context_gate.py). Requests lacking any element are rejected with HTTP 422 `CONTEXT_GATING_FAILED`.
- **Frontend Gating**: The user interface disables advisory card rendering and displays an interactive context selector until the user confirms all three parameters.

---

## 4. Automated Suppression Policy (`DEC-10`)

When environmental data is stale, contradictory, or physically inconsistent, the recommendation engine must suppress operational directives to prevent harm:

### 4.1 Stale Data Suppression (`NFR-REL-03`)
- **Trigger**: When satellite or weather observation timestamp is $> 36\text{ hours}$ old.
- **Action**: Card status changes to `SUPPRESSED`; headline changes to *"পরামর্শ স্থগিত (উপাত্ত বিলম্বিত)"*; suppression reason states *"Observation data timestamp exceeds 36-hour safety limit"*.

### 4.2 High Ensemble Uncertainty Suppression
- **Trigger**: When numerical weather prediction ensemble spread exceeds $50\%$ while rainfall probability is in the ambiguous $40\%\text{--}60\%$ window.
- **Action**: Suppresses definitive irrigation postponement advice; displays advisory cautioning the farmer of high forecast divergence.

### 4.3 Physical Sanity Violation Suppression
- **Trigger**: Ingested sensor readings violate physical laws (e.g., daily solar radiation $> 35\text{ MJ/m}^2$, relative humidity $< 5\%$ or $> 100\%$, rainfall $< 0\text{ mm}$).
- **Action**: Suppresses rule evaluation and alerts system operators.

---

## 5. Anti-Overconfidence Linguistic Standards

To eliminate deterministic overconfidence and maintain epistemic humility:

### 5.1 Banned Terms
The following Bangla terms are strictly banned from all system-generated copy:
- *"১০০% নিশ্চিত"* (100% Guaranteed)
- *"নিশ্চিত বৃষ্টি"* (Guaranteed Rain)
- *"ফলনের নিশ্চয়তা"* (Yield Guarantee)
- *"নিখুঁত পরামর্শ"* (Flawless Advice)

### 5.2 Mandatory Ground-Verification Copy (`DEC-10`, `AGENTS.md`)
Every Tier 4 advisory card must display the mandatory field inspection notice:
> *"সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*
*(Before stopping irrigation, inspect the field bunds and soil moisture yourself by hand.)*

This reminder prevents farmers from relying solely on regional satellite indicators when hyper-local field conditions (e.g. sandy soil patches) differ from the Upazila mean.

---

## 6. Verification Evidence

Automated tests in [`tests/api/test_security_hardening.py`](file:///Users/kazi/Projects/RITUCAST/tests/api/test_security_hardening.py):
- `test_context_gating_safeguard_dec17`: Verifies HTTP 422 rejection when crop or stage is absent.
- `test_suppression_safeguard_dec10_stale_data`: Verifies suppression when timestamp $>36\text{h}$.
- `test_suppression_safeguard_dec10_ensemble_uncertainty`: Verifies suppression when ensemble spread $>50\%$.
- `test_mandatory_field_verification_disclaimer_present`: Verifies presence of mandatory field verification copy.
- `test_anti_overconfidence_linguistic_standards`: Verifies absence of all prohibited overconfident words.

Related documentation:
- [`docs/responsible-ai/model-limitations-and-uncertainty.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/model-limitations-and-uncertainty.md)
- [`docs/responsible-ai/geographic-coverage-and-fairness.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/geographic-coverage-and-fairness.md)
- [`docs/responsible-ai/appropriate-use-and-misuse-prevention.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/appropriate-use-and-misuse-prevention.md)
