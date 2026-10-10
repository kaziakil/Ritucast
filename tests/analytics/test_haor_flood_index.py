"""Unit tests for Haor Flash Flood Hazard Index (IDX-FLD-01)."""

import pytest
from analytics.indicators.haor_flood_index import HaorFloodIndexCalculator


def test_haor_flood_index_normal_conditions():
    """Verify normal baseflow tier (< 0.35)."""
    res = HaorFloodIndexCalculator.calculate_index(
        catchment_id="BWDB-177",
        date_str="2026-04-10",
        p_cat_48h_mm=15.0,  # Below 30mm baseflow threshold
        water_level_m=6.50,  # Well below 8.25m DL
        danger_level_m=8.25,
        rate_of_rise_24h_m=0.10,  # Minimal rise
        inundation_fraction=0.02,
    )

    assert res.i_flood < 0.35
    assert res.hazard_tier == "NORMAL"
    assert res.sub_indices["f_P"] == 0.0
    assert res.sub_indices["f_S"] == 0.0
    assert res.sub_indices["f_R"] == 0.0


def test_haor_flood_index_emergency_surge():
    """Verify emergency surge tier (>= 0.75)."""
    res = HaorFloodIndexCalculator.calculate_index(
        catchment_id="BWDB-177",
        date_str="2026-04-18",
        p_cat_48h_mm=140.0,  # Massive Meghalaya cloudburst
        water_level_m=8.50,  # Exceeding danger level by >0.2m (8.25m + 0.25m)
        danger_level_m=8.25,
        rate_of_rise_24h_m=0.90,  # Severe surge
        inundation_fraction=0.30,
    )

    assert res.i_flood >= 0.75
    assert res.hazard_tier == "EMERGENCY"
    assert res.sub_indices["f_P"] > 0.8
    assert res.sub_indices["f_S"] == 1.0  # Above DL + 0.2m
    assert res.sub_indices["f_R"] > 0.8
