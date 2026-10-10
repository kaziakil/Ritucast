"""Tests for Tier 1 observations and Tier 2 physical indicator endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_weather_feed_godagari(client: TestClient):
    """Verify combined Tier 1 observations and Tier 3 forecasts."""
    response = client.get("/api/v1/upazilas/BD-50-20-30/weather")
    assert response.status_code == 200
    data = response.json()
    assert data["upazila_id"] == "BD-50-20-30"
    assert data["name_bn"] == "গোদাগাড়ী"
    assert data["timezone"] == "Asia/Dhaka"

    # Tier 1 Observations
    t1 = data["tier_1_observations"]
    assert "yesterday" in t1
    assert "temp_max_c" in t1["yesterday"]
    assert "temp_min_c" in t1["yesterday"]
    assert "solar_radiation_mj_m2" in t1["yesterday"]

    # Tier 3 Forecasts
    t3 = data["tier_3_forecasts"]
    assert "daily_forecast" in t3
    assert len(t3["daily_forecast"]) >= 2
    fcst_1 = t3["daily_forecast"][0]
    assert "lead_time_h" in fcst_1
    assert "qpf_precip_mm" in fcst_1
    assert "precip_probability_pct" in fcst_1


def test_weather_feed_invalid_upazila(client: TestClient):
    """Verify weather feed returns 404 for non-existent upazila."""
    response = client.get("/api/v1/upazilas/BD-99-99-99/weather")
    assert response.status_code == 404
    assert response.json()["status"] == "error"


def test_water_balance_calculation(client: TestClient):
    """Verify Tier 2 water balance calculation with FAO-56 Penman-Monteith."""
    response = client.get(
        "/api/v1/upazilas/BD-50-20-30/water-balance",
        params={"crop": "boro_rice", "stage": "vegetative_tillering"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["upazila_id"] == "BD-50-20-30"
    assert data["crop_id"] == "boro_rice"
    assert data["growth_stage"] == "vegetative_tillering"

    t2 = data["tier_2_indicators"]
    assert t2["fao56_et0_mm_day"] > 0.0
    assert t2["calibrated_kc"] > 0.0
    assert t2["crop_etc_mm_day"] > 0.0
    assert t2["current_soil_water_deficit_dt_mm"] >= 0.0
    assert "soil_properties" in t2
    assert t2["soil_properties"]["total_available_water_taw_mm"] > 0.0
    assert "status" in t2
    assert "provenance" in data


def test_water_balance_missing_context_fails(client: TestClient):
    """Verify water balance strictly enforces crop and stage query params."""
    response = client.get("/api/v1/upazilas/BD-50-20-30/water-balance")
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"


def test_flood_hazard_haor(client: TestClient):
    """Verify Tier 2 Haor flash flood hazard calculation for Tahirpur."""
    response = client.get("/api/v1/upazilas/BD-60-90-89/flood-hazard")
    assert response.status_code == 200
    data = response.json()
    assert data["upazila_id"] == "BD-60-90-89"
    assert data["name_bn"] == "তাহিরপুর"

    t2 = data["tier_2_indicators"]
    assert 0.0 <= t2["flood_hazard_index_iflood"] <= 1.0
    assert t2["hazard_tier"] in ["NORMAL", "ADVISORY", "WARNING", "EMERGENCY"]
    assert "sub_indices" in t2
    assert isinstance(t2["trigger_early_harvest"], bool)


def test_flood_hazard_outside_haor(client: TestClient):
    """Verify flood hazard returns NOT_APPLICABLE for Barind upazila."""
    response = client.get("/api/v1/upazilas/BD-50-20-30/flood-hazard")
    assert response.status_code == 200
    data = response.json()
    t2 = data["tier_2_indicators"]
    assert t2["hazard_tier"] == "NOT_APPLICABLE"
    assert t2["flood_hazard_index_iflood"] == 0.0
