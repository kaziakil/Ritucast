"""Unit tests for Agricultural Rule Implementations (RULE-IRR-01, RULE-FLD-01, etc.)."""

import pytest
from analytics.contracts.advisory_schemas import ContextGatePayload, AdvisorySeverity
from analytics.rules.rule_irr_01 import RuleIrrigationPostponement
from analytics.rules.rule_irr_02 import RuleMoistureDeficitAlert
from analytics.rules.rule_fld_01 import RuleHaorEmergencyHarvest
from analytics.rules.rule_tmp_01 import RuleBootingColdInjury
from analytics.rules.rule_tmp_02 import RuleAnthesisHeatStress


def test_rule_irr_01_triggers_on_heavy_rain_forecast():
    """Verify RULE-IRR-01 triggers when 48h rain >= 20mm and prob >= 65%."""
    rule = RuleIrrigationPostponement()
    context = ContextGatePayload(
        upazila_id="BD-50-20-30",
        crop_name="Boro Rice",
        growth_stage="Tillering",
    )

    inputs = {
        "qpf_48h_mm": 25.0,
        "rain_prob_pct": 75.0,
        "depletion_mm": 10.0,
        "taw_mm": 56.0,
        "ensemble_spread_pct": 20.0,
    }

    card = rule.evaluate(context, inputs, "2026-03-15T06:00:00Z")
    assert card is not None
    assert card.rule_id == "RULE-IRR-01"
    assert card.severity == AdvisorySeverity.ADVISORY
    assert "সেচ স্থগিত রাখুন" in card.headline_bn
    assert "সেচ বন্ধ রাখার আগে" in card.field_verification_bn


def test_rule_irr_01_inactive_during_mature_ripening():
    """Verify RULE-IRR-01 does not trigger during terminal ripening stage."""
    rule = RuleIrrigationPostponement()
    context = ContextGatePayload(
        upazila_id="BD-50-20-30",
        crop_name="Boro Rice",
        growth_stage="Maturity",  # Inactive stage
    )

    inputs = {
        "qpf_48h_mm": 35.0,
        "rain_prob_pct": 80.0,
        "depletion_mm": 15.0,
        "taw_mm": 56.0,
        "ensemble_spread_pct": 15.0,
    }

    card = rule.evaluate(context, inputs, "2026-04-20T06:00:00Z")
    assert card is None


def test_rule_fld_01_triggers_emergency_harvest_in_haor():
    """Verify RULE-FLD-01 triggers emergency harvest when flood indices breach emergency levels."""
    rule = RuleHaorEmergencyHarvest()
    context = ContextGatePayload(
        upazila_id="BD-60-90-86",  # Sunamganj Sadar
        crop_name="Boro Rice",
        growth_stage="Dough",
    )

    inputs = {
        "i_flood": 0.82,
        "p_cat_48h_mm": 125.0,
        "water_level_m_pwd": 8.10,
        "danger_level_m_pwd": 8.25,
        "rate_of_rise_24h_m": 0.65,
        "grain_maturity_pct": 85.0,
    }

    card = rule.evaluate(context, inputs, "2026-04-18T06:00:00Z")
    assert card is not None
    assert card.rule_id == "RULE-FLD-01"
    assert card.severity == AdvisorySeverity.EMERGENCY
    assert "জরুরি ধান কর্তন প্রস্তুতি" in card.headline_bn


def test_rule_fld_01_suppressed_if_crop_is_immature():
    """Verify RULE-FLD-01 is suppressed if crop is still vegetative/milky (<80% grain yellowing)."""
    rule = RuleHaorEmergencyHarvest()
    context = ContextGatePayload(
        upazila_id="BD-60-90-86",
        crop_name="Boro Rice",
        growth_stage="Tillering",  # Immature, cannot harvest
    )

    inputs = {
        "i_flood": 0.85,
        "p_cat_48h_mm": 130.0,
        "water_level_m_pwd": 8.20,
        "danger_level_m_pwd": 8.25,
        "rate_of_rise_24h_m": 0.70,
        "grain_maturity_pct": 30.0,
    }

    card = rule.evaluate(context, inputs, "2026-04-18T06:00:00Z")
    assert card is None
