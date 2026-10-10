"""Unit tests for Benchmark Evaluations and Modeling Readiness Audits."""

import pytest
from analytics.evaluation.benchmark_evaluator import BenchmarkEvaluator
from analytics.evaluation.readiness_audit import ModelingReadinessAuditor


def test_fao56_benchmark_case():
    """Verify FAO-56 benchmark test vector."""
    res = BenchmarkEvaluator.evaluate_fao56_reference_benchmark()
    assert res["is_valid"]
    assert 4.0 <= res["calculated_et0_mm_day"] <= 6.5


def test_effective_rainfall_benchmark():
    """Verify USDA SCS effective precipitation benchmark test vector."""
    res = BenchmarkEvaluator.evaluate_effective_rainfall_benchmark()
    assert res["is_valid"]
    assert res["p_light_effective"] == 0.0


def test_modeling_readiness_audit_bans_unsupervised_ml():
    """Verify that supervised ML is audited as NOT_READY with explicit justification."""
    audit = ModelingReadinessAuditor.audit_capabilities()
    assert audit["descriptive_analytics"]["status"] == "READY"
    assert audit["physical_indicators"]["status"] == "READY"
    assert audit["rule_based_advisories"]["status"] == "READY"
    assert audit["supervised_machine_learning"]["status"] == "NOT_READY"
    assert "DEC-06" in audit["supervised_machine_learning"]["justification"]


def test_anti_leakage_timestamp_verification():
    """Verify temporal anti-leakage audit function."""
    eval_time = "2026-03-15T00:00:00Z"
    past_features = ["2026-03-13T00:00:00Z", "2026-03-14T00:00:00Z"]
    leaking_features = ["2026-03-14T00:00:00Z", "2026-03-16T00:00:00Z"]  # March 16 is in future

    assert ModelingReadinessAuditor.verify_no_temporal_leakage(eval_time, past_features)
    assert not ModelingReadinessAuditor.verify_no_temporal_leakage(eval_time, leaking_features)
