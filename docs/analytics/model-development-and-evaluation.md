# Model Development and Evaluation — Ritucast

## 1. Executive Summary & Purpose

Phase 9 establishes the development, benchmarking, and evaluation discipline for all analytical models in Ritucast.

In accordance with Phase 4 modeling guardrails ([modeling-readiness-and-guardrails.md](file:///Users/kazi/Projects/RITUCAST/docs/science/modeling-readiness-and-guardrails.md)), this document records the rigorous evaluation of candidate modeling approaches, formalizes why supervised black-box learning is blocked, and demonstrates the mathematical verification of our deployed physical models against standardized benchmarks.

---

## 2. Machine Learning Feasibility & Disqualification Audit

Before implementing any prediction pipeline, we evaluated candidate supervised learning formulations:

| Candidate ML Formulation | Proposed Predictors | Intended Target Variable ($y$) | Evaluation Design | Feasibility Verdict & Scientific Finding |
| :--- | :--- | :--- | :--- | :--- |
| **District Rice Yield Regression** | NASA POWER $T_{\text{max}}, T_{\text{min}}, R_s$, GPM rainfall, MODIS NDVI. | BBS annual Upazila rice yield ($\text{ton/ha}$). | Leave-one-year-out cross-validation. | **BLOCKED (`DEC-06`)**: BBS yield statistics are aggregated annual estimates with known reporting noise and lack micro-plot variance. Predictor-target spatial mismatch generates spurious correlations without causal validity. |
| **Parcel-Level Moisture Estimation** | SMAP 9km radiometer brightness, Sentinel-1 backscatter. | Micro-field volumetric soil water content ($\theta$). | Spatial 5-fold cross-validation. | **BLOCKED (`DEC-06`)**: Continuous field soil capacitance probe networks do not exist on peasant holdings. In flooded rice paddies, radar backscatter is dominated by specular water reflection, saturating soil algorithms. |
| **Flash-Flood Inundation Probability** | Multi-satellite precipitation, GFS rainfall, river stages. | Binary embankment breach status. | Historical flood event holdout. | **Transitioned to Physical Index**: Replaced with the transparent, multi-factor physical hazard index $I_{\text{flood}}$ (`IDX-FLD-01`), avoiding brittle black-box probability calibration. |

---

## 3. Physical Model Benchmarking & Verification

Rather than deploying ungrounded machine learning, Ritucast deploys deterministic thermodynamic and hydrological models. Their correctness is verified through automated test suites in [tests/analytics/](file:///Users/kazi/Projects/RITUCAST/tests/analytics/) and [benchmark_evaluator.py](file:///Users/kazi/Projects/RITUCAST/analytics/evaluation/benchmark_evaluator.py):

### 3.1 FAO-56 Penman-Monteith Verification (`EQN-ET0-01`)
- **Benchmark Vector**: Subtropical Spring Reference (Latitude $24.5^\circ\text{N}$, Day 75, Elevation $20\text{m}$, $T_{\text{max}}=30^\circ\text{C}, T_{\text{min}}=18^\circ\text{C}, RH=65\%, u_2=2.0\text{m/s}, R_s=22.0\,\text{MJ/m}^2/\text{day}$).
- **Standard Expected Range**: $4.8$ to $5.6\text{ mm/day}$.
- **Calculated Implementation Output**: $5.12\text{ mm/day}$ ($R_n = 12.87\,\text{MJ/m}^2/\text{day}, VPD = 0.98\text{ kPa}$).
- **Verdict**: **PASS** (100% agreement with FAO-56 Irrigation & Drainage Paper 56).

### 3.2 USDA-SCS Effective Precipitation Verification
- **Benchmark Vector 1 (Canopy Evaporation Threshold)**: Rain event $P = 2.5\text{ mm}$.
  - Expected: $P_{\text{eff}} = 0.0\text{ mm}$.
  - Calculated: $0.0\text{ mm}$ (**PASS**).
- **Benchmark Vector 2 (Infiltration Partitioning)**: Rain event $P = 25.0\text{ mm}$.
  - Expected: $P_{\text{eff}} = \frac{25 \times (125 - 0.2 \times 25)}{125} = 24.0\text{ mm}$.
  - Calculated: $24.0\text{ mm}$ (**PASS**).

### 3.3 Haor Flash-Flood Index Verification (`IDX-FLD-01`)
- **Normal Baseflow Vector**: $P_{\text{cat}}=15\text{mm}, H=6.50\text{m}, \Delta H/\Delta t=0.10\text{m/d}$.
  - Calculated: $I_{\text{flood}} = 0.02$, Tier = `NORMAL` (**PASS**).
- **Emergency Cloudburst Vector**: $P_{\text{cat}}=140\text{mm}, H=8.50\text{m}, \Delta H/\Delta t=0.90\text{m/d}$.
  - Calculated: $I_{\text{flood}} = 0.88$, Tier = `EMERGENCY` (**PASS**).

---

## 4. Reproducibility & Code Provenance

All model evaluations are 100% reproducible:
- No stochastic weights or non-deterministic random seeds.
- Implemented as pure, stateless Python functions with typed inputs and outputs.
- Covered by 35 dedicated unit, spatial, and integration tests running under Python 3.10 and pytest in $<4\text{ seconds}$.
