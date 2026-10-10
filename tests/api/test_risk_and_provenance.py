"""Tests for physical risk assessment and system provenance endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_physical_risk_evaluation_barind(client: TestClient):
    """Verify physical hazard evaluation in Barind testbed."""
    payload = {
        "upazila_id": "BD-50-20-30",
        "crop_id": "boro_rice",
        "growth_stage": "Tillering",
        "hazard_types": ["moisture_deficit", "flash_flood", "thermal_stress"],
    }
    response = client.post("/api/v1/risk/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["upazila_id"] == "BD-50-20-30"
    assert data["overall_hazard_tier"] in ["LOW", "MODERATE", "HIGH", "CRITICAL"]
    assert len(data["hazard_assessments"]) == 3

    # Confirm mandatory scientific disclaimer (DEC-06)
    assert "scientific_disclaimer_bn" in data
    assert "আর্থিক ক্ষতি বা চূড়ান্ত ফলন হ্রাসের নিশ্চয়তা দেয় না" in data["scientific_disclaimer_bn"]


def test_physical_risk_evaluation_haor(client: TestClient):
    """Verify physical hazard evaluation in Haor testbed detects flood hazard."""
    payload = {
        "upazila_id": "BD-60-90-89",
        "crop_id": "boro_rice",
        "growth_stage": "Maturity",
        "hazard_types": ["flash_flood"],
    }
    response = client.post("/api/v1/risk/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["upazila_id"] == "BD-60-90-89"
    assert data["overall_hazard_tier"] == "CRITICAL"
    flood_item = data["hazard_assessments"][0]
    assert flood_item["hazard_domain"] == "flash_flood"
    assert flood_item["action_warranted"] is True


def test_system_provenance_and_freshness(client: TestClient):
    """Verify system provenance exposes datasets, equations, and DEC-06 non-goals."""
    response = client.get("/api/v1/provenance")
    assert response.status_code == 200
    data = response.json()
    assert data["system_name"] == "Ritucast Agricultural Intelligence Platform"
    assert "version" in data
    assert len(data["pilot_regions"]) == 2

    # Datasets
    datasets = data["datasets"]
    assert len(datasets) >= 3
    ds_ids = [d["dataset_id"] for d in datasets]
    assert "DATA-MET-01" in ds_ids
    assert "DATA-FCST-01" in ds_ids
    assert "DATA-HYD-01" in ds_ids

    # Methodologies
    methods = data["scientific_methodologies"]
    method_ids = [m["method_id"] for m in methods]
    assert "EQN-ET0-01" in method_ids
    assert "EQN-SWD-01" in method_ids
    assert "RULE-IRR-01" in method_ids

    # Scientific Boundaries (DEC-06)
    boundaries = data["scientific_boundaries"]
    assert "yield_prediction" in boundaries
    assert "chemical_diagnosis" in boundaries
    assert "hardware_actuation" in boundaries
