# Phase 9: Work Plan — Agricultural Analytics and Recommendation Engine

## 1. Executive Summary & Purpose

Phase 9 establishes the scientific analytics and decision-support core for **Ritucast**. Following the validation of processed environmental tables in [Phase 8](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-08/validation-report.md), this phase implements derived agroclimatic indicators, water balance simulations, flash-flood risk indices, and actionable, context-gated advisory rules for smallholder farmers in Bangladesh.

---

## 2. Sequential Phase Objectives

1. **Step 1: Inspect Repository & Processed Datasets**: Verify Phase 8 Parquet tables (`meteorology_daily_upazila.parquet`, `forecast_hourly_pilot.parquet`, `catchment_rainfall_daily.parquet`, `hydrology_river_stage.parquet`).
2. **Step 2: Analytics Contracts & Schemas**: Author Pydantic v2 data models for indicators, descriptive statistics, and the 5-section recommendation card anatomy (`DEC-30`).
3. **Step 3: Implement Physical Indicators**: Vectorized implementations of FAO-56 Penman-Monteith $ET_0$ (`EQN-ET0-01`), crop demand $ET_c$, soil water balance $D_t$ (`EQN-SWD-01`), Haor flash-flood index $I_{\text{flood}}$ (`IDX-FLD-01`), and cardinal thermal indices ($I_{\text{heat}}, I_{\text{cold}}$).
4. **Step 4: Agricultural Decision Rules**: Implement `RULE-IRR-01`, `RULE-IRR-02`, `RULE-FLD-01`, `RULE-TMP-01`, and `RULE-TMP-02`.
5. **Step 5: Governance Middleware**: Contextual Gating (`DEC-17`), Automated Advisory Suppression (`DEC-10`), and Explainability compilations.
6. **Step 6: Automated Testing & Benchmarking**: Implement unit, spatial, boundary, and end-to-end integration tests.
7. **Step 7: Verification & Phase 10 Handoff**: Publish complete documentation and prepare integration contract for Phase 10.
