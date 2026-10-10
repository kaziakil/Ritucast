"""Tests for advisory generation, mandatory contextual gating, and suppression safeguards."""

import pytest
from fastapi.testclient import TestClient


def test_contextual_gating_missing_parameters(client: TestClient):
    """Confirm omission of crop or stage returns HTTP 422 (DEC-17)."""
    # Missing both
    res1 = client.get("/api/v1/upazilas/BD-50-20-30/advisories")
    assert res1.status_code == 422
    assert res1.json()["status"] == "error"

    # Missing stage
    res2 = client.get("/api/v1/upazilas/BD-50-20-30/advisories?crop=boro_rice")
    assert res2.status_code == 422
    assert res2.json()["status"] == "error"

    # Missing crop
    res3 = client.get("/api/v1/upazilas/BD-50-20-30/advisories?stage=tillering")
    assert res3.status_code == 422
    assert res3.json()["status"] == "error"


def test_barind_irrigation_postponement_advisory(client: TestClient):
    """Verify 4-tier advisory response for Godagari tillering stage."""
    response = client.get(
        "/api/v1/upazilas/BD-50-20-30/advisories",
        params={"crop": "boro_rice", "stage": "tillering"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["upazila_id"] == "BD-50-20-30"
    assert data["crop_id"] == "boro_rice"
    assert data["growth_stage"] == "Tillering"

    # Four-Tier Separation (DEC-08)
    assert "tier_1_observations" in data
    assert "tier_2_indicators" in data
    assert "tier_3_predictions" in data
    assert "tier_4_recommendation" in data

    t4 = data["tier_4_recommendation"]
    assert t4["rule_id"] in ["RULE-IRR-01", "RULE-IRR-02", "RULE-NOM-01"]
    assert len(t4["headline_bn"]) > 0
    assert len(t4["body_bn"]) > 0

    # Mandatory field verification copy (DEC-10, AGENTS.md)
    assert "সেচ বন্ধ" in t4["mandatory_disclaimer_bn"]
    assert "পরীক্ষা করুন" in t4["mandatory_disclaimer_bn"]

    # Anti-overconfidence linguistic check (AGENTS.md)
    banned_terms = ["১০০% নিশ্চিত", "নিশ্চিত বৃষ্টি", "ফলনের নিশ্চয়তা"]
    full_text = str(data)
    for term in banned_terms:
        assert term not in full_text, f"Banned overconfident term '{term}' found in advisory payload!"


def test_haor_emergency_harvest_advisory(client: TestClient):
    """Verify emergency harvest advisory for Tahirpur during maturity stage."""
    response = client.get(
        "/api/v1/upazilas/BD-60-90-89/advisories",
        params={"crop": "boro_rice", "stage": "maturity"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["upazila_id"] == "BD-60-90-89"
    assert data["crop_id"] == "boro_rice"

    t4 = data["tier_4_recommendation"]
    assert t4["rule_id"] == "RULE-FLD-01"
    assert t4["category"] == "FLASH_FLOOD"
    assert t4["action_code"] == "EMERGENCY_HARVEST"
    assert t4["severity"] == "EMERGENCY"
    assert "কর্তন" in t4["headline_bn"] or "ফসল" in t4["headline_bn"]


def test_custom_advisory_evaluate_post(client: TestClient):
    """Verify direct POST /api/v1/advisories/evaluate with custom environmental inputs."""
    payload = {
        "upazila_id": "BD-50-20-30",
        "crop_name": "Boro Rice",
        "growth_stage": "Tillering",
        "inputs": {
            "qpf_48h_mm": 35.0,
            "rain_prob_pct": 80.0,
            "depletion_mm": 12.0,
            "taw_mm": 56.0,
            "ensemble_spread_pct": 18.0,
        },
    }
    response = client.post("/api/v1/advisories/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["upazila_id"] == "BD-50-20-30"
    t4 = data["tier_4_recommendation"]
    assert t4["rule_id"] == "RULE-IRR-01"
    assert t4["action_code"] == "POSTPONE_IRRIGATION"


def test_suppression_stale_data(client: TestClient):
    """Verify automated advisory suppression when data is >36 hours old (DEC-10)."""
    stale_timestamp = "2026-03-01T00:00:00Z"  # > 36 hours before current evaluation
    payload = {
        "upazila_id": "BD-50-20-30",
        "crop_name": "Boro Rice",
        "growth_stage": "Tillering",
        "data_timestamp_utc": stale_timestamp,
        "inputs": {
            "qpf_48h_mm": 35.0,
            "rain_prob_pct": 80.0,
            "depletion_mm": 12.0,
            "taw_mm": 56.0,
            "ensemble_spread_pct": 18.0,
        },
    }
    response = client.post("/api/v1/advisories/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    t4 = data["tier_4_recommendation"]
    assert t4["is_suppressed"] is True
    assert "স্থগিত" in t4["headline_bn"]
