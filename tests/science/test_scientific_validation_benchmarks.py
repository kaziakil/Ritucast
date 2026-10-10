"""Automated Tests for Scientific & Agricultural Ground-Truth Benchmarks."""

import pytest
from analytics.validation.ground_truth_validator import (
    GroundTruthValidator,
    ContinuousMetrics,
    ContingencyMetrics,
)


def test_continuous_metrics_calculation_accuracy():
    """Verify exact mathematical calculation of continuous metrics (MBE, RMSE, Pearson r, NSE)."""
    observed = [10.0, 20.0, 30.0, 40.0, 50.0]
    simulated = [12.0, 19.0, 31.0, 38.0, 52.0]

    metrics = GroundTruthValidator.calculate_continuous_metrics(simulated, observed)

    assert isinstance(metrics, ContinuousMetrics)
    assert metrics.sample_size == 5
    # Diffs: [+2, -1, +1, -2, +2] -> Mean = +0.4
    assert metrics.mean_bias_error == 0.4
    # Squared diffs: [4, 1, 1, 4, 4] -> Mean = 14 / 5 = 2.8 -> sqrt(2.8) ~= 1.6733
    assert metrics.root_mean_square_error == round((14.0 / 5.0) ** 0.5, 4)
    assert metrics.pearson_r > 0.98
    assert metrics.nash_sutcliffe_efficiency > 0.95


def test_contingency_metrics_calculation_accuracy():
    """Verify exact calculation of 2x2 contingency matrix (Hits, False Alarms, POD, FAR, CSI)."""
    # 10 events:
    # 4 Hits, 1 False Alarm, 1 Miss, 4 Correct Rejections
    observed = [True, True, True, True, True, False, False, False, False, False]
    simulated = [True, True, True, True, False, True, False, False, False, False]

    metrics = GroundTruthValidator.calculate_contingency_metrics(simulated, observed)

    assert isinstance(metrics, ContingencyMetrics)
    assert metrics.total_samples == 10
    assert metrics.hits == 4
    assert metrics.false_alarms == 1
    assert metrics.misses == 1
    assert metrics.correct_rejections == 4

    # POD = 4 / (4 + 1) = 0.80
    assert metrics.probability_of_detection == 0.8
    # FAR = 1 / (4 + 1) = 0.20
    assert metrics.false_alarm_ratio == 0.2
    # CSI = 4 / (4 + 1 + 1) = 4 / 6 ~= 0.6667
    assert metrics.critical_success_index == round(4.0 / 6.0, 4)
    # Accuracy = (4 + 4) / 10 = 80.0%
    assert metrics.accuracy_pct == 80.0


def test_bmd_meteorological_benchmark_passes_target_criteria():
    """Verify that NASA POWER & Open-Meteo benchmark passes BMD synoptic station criteria."""
    result = GroundTruthValidator.benchmark_bmd_meteorology()

    assert result["status"] == "PASS"
    assert result["passes_criteria"] is True

    tmax_m = result["temperature_tmax_metrics"]
    assert tmax_m["root_mean_square_error"] <= 1.5

    et0_m = result["et0_metrics"]
    assert et0_m["root_mean_square_error"] <= 0.65
    assert et0_m["r_squared"] >= 0.85

    pcp_m = result["precipitation_detection_metrics"]
    assert pcp_m["probability_of_detection"] >= 0.85


def test_bwdb_flood_hazard_benchmark_passes_target_criteria():
    """Verify that Haor Flood Index (I_flood) passes BWDB Sunamganj Surma gauge criteria."""
    result = GroundTruthValidator.benchmark_bwdb_flood_indices()

    assert result["status"] == "PASS"
    assert result["passes_criteria"] is True

    m = result["metrics"]
    assert m["probability_of_detection"] >= 0.85
    assert m["false_alarm_ratio"] <= 0.20
    assert m["critical_success_index"] >= 0.70


def test_brri_water_balance_benchmark_passes_target_criteria():
    """Verify that Soil Water Deficit passes BRRI Barind AWD lysimeter criteria."""
    result = GroundTruthValidator.benchmark_brri_water_balance()

    assert result["status"] == "PASS"
    assert result["passes_criteria"] is True

    cont = result["continuous_deficit_metrics"]
    assert cont["root_mean_square_error"] <= 5.0

    cat = result["awd_trigger_contingency_metrics"]
    assert cat["accuracy_pct"] >= 90.0
    assert cat["probability_of_detection"] >= 0.85


def test_full_scientific_benchmark_triad_execution():
    """Verify that the full triad benchmark aggregates and validates all 3 domains."""
    full = GroundTruthValidator.run_full_scientific_benchmark()

    assert full["overall_status"] == "PASS"
    assert "bmd_meteorological_benchmark" in full
    assert "bwdb_hydrological_benchmark" in full
    assert "brri_agronomic_benchmark" in full
