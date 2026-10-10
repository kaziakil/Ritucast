# Ritucast: Data Provenance & Quality Assurance Architecture

## 1. Provenance Invariant

Every analytical result emitted by the Ritucast API maintains end-to-end traceability back to:
1. Ingested raw environmental sensor observations ([Phase 8](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-08/validation-report.md)).
2. Verified physical equations and algorithms ([Phase 4](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-04/validation-report.md)).
3. Evaluated decision rules ([Phase 9](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-09/validation-report.md)).

---

## 2. Ingested Dataset Inventory (`GET /api/v1/provenance`)

| Dataset ID | Agency Source | Physical Variables | Spatial / Temporal Scale | Update Latency |
| :--- | :--- | :--- | :--- | :--- |
| **`DATA-MET-01`** | NASA POWER / BMD Station | $T_{\max}$, $T_{\min}$, $RH_{2m}$, $U_2$, Radiation, Rain | Upazila Centroid / Daily | $14.5\text{ hours}$ |
| **`DATA-FCST-01`** | ECMWF IFS / NOAA GFS | QPF Rainfall, Probability, Temperature | Upazila Grid / Hourly to 72h | $3.0\text{ hours}$ |
| **`DATA-HYD-01`** | BWDB Hydrology / GPM IMERG | Surma River Stage, Meghalaya Rain | River Gauge / 3-Hourly | $2.5\text{ hours}$ |

---

## 3. Data Freshness & Automated Suppression (`DEC-10`)

When upstream pipeline disruptions cause forecast latency to exceed 36 hours:
- The system flags `is_suppressed: true`.
- The recommendation is replaced with a safe fallback directing farmers to local SAAO field verification.
- Stale data is never masked as current.

---

## 4. Quality Checks & Physical Sanity Bounds

Incoming and cached datasets are guarded by strict physical domain bounds established in Phase 8:
- Temperature: $-5.0^\circ\text{C} \le T \le 55.0^\circ\text{C}$
- Relative Humidity: $0\% \le RH \le 100\%$
- Precipitation: $0.0\text{ mm} \le P \le 600.0\text{ mm/day}$
- Solar Radiation: $0.0 \le R_s \le 35.0\text{ MJ/m}^2/\text{day}$

Data violating these physical bounds triggers automatic advisory suppression.

---

## 5. Related Documentation

- Architecture: [phase-10-backend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md)
- Known Limitations: [known-limitations.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/known-limitations.md)
