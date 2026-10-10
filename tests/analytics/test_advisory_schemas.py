"""Unit tests for Advisory Card Schema and Anti-Overconfidence Linguistic Standards."""

import pytest
from pydantic import ValidationError
from analytics.contracts.advisory_schemas import AdvisoryCard, AdvisorySeverity, AdvisoryStatus


def test_advisory_card_rejects_banned_overconfident_phrase_1():
    """Verify validation error when card contains '১০০% নিশ্চিত'."""
    with pytest.raises(ValidationError) as exc_info:
        AdvisoryCard(
            advisory_id="TEST-FAIL-01",
            rule_id="RULE-IRR-01",
            upazila_id="BD-50-20-30",
            crop_name="Boro Rice",
            growth_stage="Tillering",
            timestamp_utc="2026-03-15T06:00:00Z",
            valid_until_utc="2026-03-17T06:00:00Z",
            severity=AdvisorySeverity.ADVISORY,
            status=AdvisoryStatus.ACTIVE,
            headline_bn="১০০% নিশ্চিত বৃষ্টির পূর্বাভাস",  # Banned phrase
            plain_language_bn="বৃষ্টি নিশ্চিত আসবে।",
            action_items_bn=["সেচ বন্ধ রাখুন।"],
            field_verification_bn="সেচ বন্ধ রাখার আগে পরীক্ষা করুন।",
            uncertainty_description_bn="কোন অনিশ্চয়তা নেই।",
        )

    assert "Banned overconfident linguistic phrase" in str(exc_info.value)


def test_advisory_card_rejects_banned_overconfident_phrase_2():
    """Verify validation error when card contains 'ফলনের নিশ্চয়তা'."""
    with pytest.raises(ValidationError) as exc_info:
        AdvisoryCard(
            advisory_id="TEST-FAIL-02",
            rule_id="RULE-IRR-01",
            upazila_id="BD-50-20-30",
            crop_name="Boro Rice",
            growth_stage="Tillering",
            timestamp_utc="2026-03-15T06:00:00Z",
            valid_until_utc="2026-03-17T06:00:00Z",
            severity=AdvisorySeverity.ADVISORY,
            status=AdvisoryStatus.ACTIVE,
            headline_bn="সেচ স্থগিত রাখুন",
            plain_language_bn="এই পরামর্শ মানলে শতভাগ ফলনের নিশ্চয়তা দেওয়া হচ্ছে।",  # Banned phrase
            action_items_bn=["সেচ বন্ধ রাখুন।"],
            field_verification_bn="সেচ বন্ধ রাখার আগে পরীক্ষা করুন।",
            uncertainty_description_bn="অনিশ্চয়তা কম।",
        )

    assert "Banned overconfident linguistic phrase" in str(exc_info.value)


def test_advisory_card_serializes_cleanly():
    """Verify valid advisory card serializes to dictionary and JSON format."""
    card = AdvisoryCard(
        advisory_id="TEST-PASS-01",
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
        action_items_bn=["নলকূপ চালু করা স্থগিত রাখুন।"],
        field_verification_bn="সেচ বন্ধ রাখার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।",
        uncertainty_description_bn="পূর্বাভাসে স্বাভাবিক অনিশ্চয়তা বিদ্যমান।",
    )

    data = card.model_dump()
    assert data["advisory_id"] == "TEST-PASS-01"
    assert data["severity"] == "ADVISORY"
    assert "জমির আইল এবং মাটির রস" in data["field_verification_bn"]
