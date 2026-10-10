"""Unit tests for Mandatory Contextual Gating (DEC-17)."""

import pytest
from analytics.engine.context_gate import ContextGator, ContextGatingError
from analytics.engine.advisory_engine import AgriculturalRecommendationEngine


def test_context_gator_approves_valid_pilot_context():
    """Verify context gator succeeds on Godagari Boro Rice Tillering."""
    is_valid, err, payload = ContextGator.validate_context(
        upazila_id="BD-50-20-30",
        crop_name="Boro Rice",
        growth_stage="Tillering",
    )

    assert is_valid
    assert err is None
    assert payload is not None
    assert payload.upazila_id == "BD-50-20-30"


def test_context_gator_rejects_missing_upazila():
    """Verify rejection when upazila is missing."""
    is_valid, err, payload = ContextGator.validate_context(
        upazila_id="",
        crop_name="Boro Rice",
        growth_stage="Tillering",
    )

    assert not is_valid
    assert "Gate 1 Failed" in err
    assert payload is None


def test_context_gator_rejects_unknown_upazila():
    """Verify rejection when upazila is outside pilot testbeds."""
    is_valid, err, payload = ContextGator.validate_context(
        upazila_id="BD-99-99-99",  # Outside scope
        crop_name="Boro Rice",
        growth_stage="Tillering",
    )

    assert not is_valid
    assert "outside approved pilot testbeds" in err


def test_context_gator_rejects_uncalibrated_crop():
    """Verify rejection when crop is not calibrated (e.g. Cotton)."""
    is_valid, err, payload = ContextGator.validate_context(
        upazila_id="BD-50-20-30",
        crop_name="Cotton",
        growth_stage="Vegetative",
    )

    assert not is_valid
    assert "Gate 2 Failed" in err


def test_recommendation_engine_raises_on_gating_violation():
    """Verify master engine raises ContextGatingError if gating fails."""
    engine = AgriculturalRecommendationEngine()
    with pytest.raises(ContextGatingError):
        engine.evaluate_all_rules(
            upazila_id="UNKNOWN_ID",
            crop_name="Boro Rice",
            growth_stage="Tillering",
            inputs={},
        )
