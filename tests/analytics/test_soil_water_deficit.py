"""Unit tests for Soil Water Deficit Calculator (EQN-SWD-01)."""

import pytest
from analytics.indicators.soil_water_deficit import SoilWaterDeficitCalculator


def test_taw_and_raw_calculation():
    """Verify TAW and RAW parameterization for Barind heavy clay paleosols."""
    taw = SoilWaterDeficitCalculator.calculate_taw()
    # 1000 * (0.32 - 0.18) * 0.40 = 56.0 mm
    assert taw == 56.0

    raw_tillering = SoilWaterDeficitCalculator.calculate_raw(taw, "Tillering")
    # p = 0.35 -> 0.35 * 56.0 = 19.6 mm
    assert raw_tillering == 19.6

    raw_flowering = SoilWaterDeficitCalculator.calculate_raw(taw, "Flowering")
    # p = 0.10 -> 0.10 * 56.0 = 5.6 mm
    assert raw_flowering == 5.6


def test_usda_scs_effective_precipitation():
    """Verify USDA-SCS effective precipitation sub-model."""
    # Under 3mm -> zero effective rain
    assert SoilWaterDeficitCalculator.calculate_effective_precipitation(2.0) == 0.0

    # 20mm rain -> (20 * (125 - 0.2*20)) / 125 = (20 * 121) / 125 = 19.36 mm
    p_eff_20 = SoilWaterDeficitCalculator.calculate_effective_precipitation(20.0)
    assert 19.0 <= p_eff_20 <= 19.5


def test_daily_water_balance_step_drying():
    """Verify daily depletion increment under dry weather."""
    res = SoilWaterDeficitCalculator.step_daily_water_balance(
        upazila_id="BD-50-20-30",
        date_str="2026-03-20",
        d_prev_mm=10.0,
        etc_mm=4.5,
        precip_mm=0.0,
        irrigation_mm=0.0,
        growth_stage="Tillering",
    )

    # Dt = 10.0 + 4.5 = 14.5 mm
    assert res.depletion_mm == 14.5
    assert not res.is_stress_critical  # RAW is 19.6 mm
    assert res.storage_capacity_remaining_mm == 56.0 - 14.5


def test_daily_water_balance_step_replenishment_and_bounds():
    """Verify depletion resets properly when irrigation or rain is applied."""
    res = SoilWaterDeficitCalculator.step_daily_water_balance(
        upazila_id="BD-50-20-30",
        date_str="2026-03-21",
        d_prev_mm=18.0,
        etc_mm=4.0,
        precip_mm=0.0,
        irrigation_mm=30.0,  # 30mm applied
        growth_stage="Tillering",
    )

    # 18 + 4 - 30 = -8 -> clamped to 0.0 (field capacity reached, surplus drains)
    assert res.depletion_mm == 0.0
    assert not res.is_stress_critical
    assert res.storage_capacity_remaining_mm == 56.0
