"""End-to-end integration test verifying that Phase 8 Parquet outputs feed Phase 9 Analytics."""

import os
import pytest
import pandas as pd
from analytics.descriptive.climatology import ClimatologyAggregator
from analytics.indicators.penman_monteith import PenmanMonteithCalculator
from analytics.indicators.crop_water_demand import CropWaterDemandCalculator
from analytics.indicators.soil_water_deficit import SoilWaterDeficitCalculator
from analytics.indicators.haor_flood_index import HaorFloodIndexCalculator
from analytics.engine.advisory_engine import AgriculturalRecommendationEngine


def test_end_to_end_pipeline_parquet_to_advisories():
    """Verify that processed Parquet files from Phase 8 can be read and evaluated by Phase 9."""
    parquet_path = "data/processed/meteorology_daily_upazila.parquet"
    if not os.path.exists(parquet_path):
        pytest.skip(f"Parquet file {parquet_path} not found")

    df_met = pd.read_parquet(parquet_path)
    assert not df_met.empty
    assert "upazila_id" in df_met.columns

    # 1. Test descriptive aggregation for Godagari
    godagari_id = "BD-50-20-30"
    summary = ClimatologyAggregator.summarize_period(
        df_met=df_met,
        upazila_id=godagari_id,
    )
    assert summary.days_count >= 1
    assert summary.mean_t2m_c > 0.0

    # 2. Test physical indicator calculation
    first_row = df_met[df_met["upazila_id"] == godagari_id].iloc[0]
    et0_res = PenmanMonteithCalculator.calculate_et0(
        upazila_id=godagari_id,
        date_str=str(first_row["date"])[:10],
        t_max_c=float(first_row["t2m_max_c"]),
        t_min_c=float(first_row["t2m_min_c"]),
        rh_mean_pct=float(first_row["rh2m_pct"]),
        wind_speed_2m_ms=float(first_row["wind_speed_2m_ms"]),
        solar_rad_mj_m2=float(first_row["solar_rad_mj_m2"]),
    )
    assert et0_res.et0_mm_day > 0.0

    etc_res = CropWaterDemandCalculator.calculate_etc(
        upazila_id=godagari_id,
        date_str=str(first_row["date"])[:10],
        et0_mm_day=et0_res.et0_mm_day,
        growth_stage="Tillering",
    )
    assert etc_res.etc_mm_day > 0.0

    # 3. Test recommendation engine evaluation with simulated pre-rain inputs
    engine = AgriculturalRecommendationEngine()
    advisories = engine.evaluate_all_rules(
        upazila_id=godagari_id,
        crop_name="Boro Rice",
        growth_stage="Tillering",
        inputs={
            "qpf_48h_mm": 28.0,
            "rain_prob_pct": 75.0,
            "depletion_mm": 12.0,
            "taw_mm": 56.0,
            "ensemble_spread_pct": 20.0,
        },
    )

    assert len(advisories) >= 1
    card = advisories[0]
    assert card.rule_id == "RULE-IRR-01"
    assert card.status.value == "ACTIVE"
    assert "সেচ বন্ধ রাখার আগে" in card.field_verification_bn
