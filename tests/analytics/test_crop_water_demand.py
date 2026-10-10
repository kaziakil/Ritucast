"""Unit tests for Crop Water Demand Calculator (ETc = Kc * ET0)."""

import pytest
from analytics.indicators.crop_water_demand import CropWaterDemandCalculator


def test_stage_based_kc_lookup():
    """Verify crop coefficient lookup across phenological stages."""
    kc_tillering = CropWaterDemandCalculator.get_kc_for_stage("Tillering")
    kc_flowering = CropWaterDemandCalculator.get_kc_for_stage("Flowering")
    kc_maturity = CropWaterDemandCalculator.get_kc_for_stage("Maturity")

    assert kc_tillering == 1.15
    assert kc_flowering == 1.30
    assert kc_maturity == 0.75


def test_continuous_kc_linear_interpolation():
    """Verify continuous linear interpolation along development timeline."""
    # Day 1 -> 1.10, Day 40 -> 1.15. At Day 20.5 (midpoint), Kc should be ~1.125
    kc_day_20 = CropWaterDemandCalculator.interpolate_kc(20)
    assert 1.11 <= kc_day_20 <= 1.14

    # Day 40 -> 1.15, Day 75 -> 1.30
    kc_day_57 = CropWaterDemandCalculator.interpolate_kc(57)
    assert 1.20 <= kc_day_57 <= 1.25

    # Day 100 -> 1.30, Day 145 -> 0.65
    kc_day_122 = CropWaterDemandCalculator.interpolate_kc(122)
    assert 0.90 <= kc_day_122 <= 1.05


def test_calculate_etc_formula():
    """Verify ETc = Kc * ET0."""
    res = CropWaterDemandCalculator.calculate_etc(
        upazila_id="BD-50-20-30",
        date_str="2026-03-20",
        et0_mm_day=4.5,
        growth_stage="Flowering",
    )

    expected_etc = round(4.5 * 1.30, 2)
    assert res.etc_mm_day == expected_etc
    assert res.kc_current == 1.30
    assert res.et0_mm_day == 4.5
