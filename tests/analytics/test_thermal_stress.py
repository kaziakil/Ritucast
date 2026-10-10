"""Unit tests for Cardinal Thermal Stress Indices (Iheat & Icold)."""

import pytest
from analytics.indicators.thermal_stress import ThermalStressCalculator


def test_heat_stress_sub_threshold():
    """Verify heat stress is zero when Tmax < 35°C."""
    res = ThermalStressCalculator.calculate_heat_stress(
        upazila_id="BD-50-20-30",
        date_str="2026-04-10",
        t_max_c=33.5,
        consecutive_days=3,
    )

    assert res.intensity_index == 0.0
    assert not res.is_critical
    assert res.stress_type == "NONE"


def test_heat_stress_critical_breach():
    """Verify heat stress triggers critical state after 2 consecutive days >= 35°C."""
    res = ThermalStressCalculator.calculate_heat_stress(
        upazila_id="BD-50-20-30",
        date_str="2026-04-15",
        t_max_c=37.5,
        consecutive_days=2,
    )

    # (37.5 - 35) / 5 = 0.5
    assert res.intensity_index == 0.5
    assert res.is_critical
    assert res.stress_type == "HEAT"
    assert res.mitigation_water_depth_cm == 4.0


def test_cold_stress_critical_breach():
    """Verify cold stress triggers critical state after 3 consecutive days <= 15°C."""
    res = ThermalStressCalculator.calculate_cold_stress(
        upazila_id="BD-50-20-90",
        date_str="2026-01-20",
        t_min_c=12.5,
        consecutive_days=3,
    )

    # (15 - 12.5) / 5 = 0.5
    assert res.intensity_index == 0.5
    assert res.is_critical
    assert res.stress_type == "COLD"
    assert res.mitigation_water_depth_cm == 6.0
