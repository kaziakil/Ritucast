"""Unit tests for Automated Advisory Suppression Policy (DEC-10)."""

import pytest
from datetime import datetime, timezone, timedelta
from analytics.contracts.advisory_schemas import AdvisoryCard, AdvisorySeverity, AdvisoryStatus
from analytics.engine.suppression import AdvisorySuppressionEngine


@pytest.fixture
def sample_active_card() -> AdvisoryCard:
    return AdvisoryCard(
        advisory_id="TEST-ADV-001",
        rule_id="RULE-IRR-01",
        upazila_id="BD-50-20-30",
        crop_name="Boro Rice",
        growth_stage="Tillering",
        timestamp_utc="2026-03-15T06:00:00Z",
        valid_until_utc="2026-03-17T06:00:00Z",
        severity=AdvisorySeverity.ADVISORY,
        status=AdvisoryStatus.ACTIVE,
        headline_bn="সেচ স্থগিত রাখুন (পরামর্শ)",
        plain_language_bn="আগামী ৪৮ ঘণ্টার মধ্যে বৃষ্টির সম্ভাবনা রয়েছে।",
        action_items_bn=["নলকূপ বন্ধ রাখুন।"],
        field_verification_bn="সেচ বন্ধ রাখার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।",
        uncertainty_description_bn="পূর্বাভাস মডেল বিস্তার ২৫%।",
    )


def test_suppression_on_stale_data(sample_active_card):
    """Verify advisory is suppressed if input data is older than 36 hours (NFR-REL-03)."""
    # 40 hours ago
    stale_timestamp = (datetime.now(timezone.utc) - timedelta(hours=40)).isoformat()

    suppressed_card = AdvisorySuppressionEngine.apply_suppression_if_needed(
        card=sample_active_card,
        data_timestamp_utc=stale_timestamp,
    )

    assert suppressed_card.status == AdvisoryStatus.SUPPRESSED
    assert "exceeds 36-hour safety limit" in suppressed_card.suppression_reason
    assert "পরামর্শ স্থগিত" in suppressed_card.headline_bn


def test_suppression_on_high_ensemble_spread(sample_active_card):
    """Verify suppression when ensemble spread > 50% and rain prob is 40-60% (DEC-10)."""
    suppressed_card = AdvisorySuppressionEngine.apply_suppression_if_needed(
        card=sample_active_card,
        ensemble_spread_pct=55.0,  # > 50%
        rain_prob_pct=50.0,        # in 40-60% ambiguous range
    )

    assert suppressed_card.status == AdvisoryStatus.SUPPRESSED
    assert "ensemble spread exceeds 50%" in suppressed_card.suppression_reason


def test_suppression_on_physical_range_violation(sample_active_card):
    """Verify suppression when physical sanity violations are flagged."""
    suppressed_card = AdvisorySuppressionEngine.apply_suppression_if_needed(
        card=sample_active_card,
        physical_violations=["solar_rad_mj_m2 out of physical range (42.0 > 35.0)"],
    )

    assert suppressed_card.status == AdvisoryStatus.SUPPRESSED
    assert "Input physical range violations" in suppressed_card.suppression_reason
