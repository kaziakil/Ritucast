"""Unit tests for FAO-56 Penman-Monteith ET0 Calculator (EQN-ET0-01)."""

import pytest
from analytics.indicators.penman_monteith import PenmanMonteithCalculator


def test_penman_monteith_standard_subtropical_conditions():
    """Verify ET0 calculation under typical Bangladesh spring conditions (March)."""
    res = PenmanMonteithCalculator.calculate_et0(
        upazila_id="BD-50-20-30",
        date_str="2026-03-15",
        t_max_c=32.0,
        t_min_c=20.0,
        rh_mean_pct=60.0,
        wind_speed_2m_ms=2.2,
        solar_rad_mj_m2=21.5,
        elevation_m=20.0,
        latitude_deg=24.46,
    )

    assert res.et0_mm_day > 3.5
    assert res.et0_mm_day < 7.0
    assert res.vapor_pressure_deficit_kpa > 0.5
    assert res.quality_flag == "VALID"
    assert res.method == "FAO-56 Penman-Monteith"


def test_penman_monteith_cool_humid_winter_conditions():
    """Verify ET0 calculation under cool, foggy winter conditions (January)."""
    res = PenmanMonteithCalculator.calculate_et0(
        upazila_id="BD-50-20-90",
        date_str="2026-01-15",
        t_max_c=22.0,
        t_min_c=11.0,
        rh_mean_pct=85.0,
        wind_speed_2m_ms=1.1,
        solar_rad_mj_m2=14.0,
        elevation_m=20.0,
        latitude_deg=24.58,
    )

    # In cool humid winter, ET0 should be low (typically 2.0 to 3.5 mm/day)
    assert 1.5 <= res.et0_mm_day <= 3.8
    assert res.vapor_pressure_deficit_kpa < 1.0


def test_penman_monteith_extreme_hot_dry_spring_conditions():
    """Verify ET0 calculation under pre-monsoon heatwave conditions (April)."""
    res = PenmanMonteithCalculator.calculate_et0(
        upazila_id="BD-50-20-30",
        date_str="2026-04-20",
        t_max_c=39.0,
        t_min_c=25.0,
        rh_mean_pct=40.0,
        wind_speed_2m_ms=3.5,
        solar_rad_mj_m2=26.0,
        elevation_m=20.0,
        latitude_deg=24.46,
    )

    # Pre-monsoon high radiation, dry air, and wind produce peak ET0 (6.0 to 9.0 mm/day)
    assert 5.5 <= res.et0_mm_day <= 9.5
    assert res.vapor_pressure_deficit_kpa > 2.0
