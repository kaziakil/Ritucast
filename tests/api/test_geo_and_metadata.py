"""Tests for geographic boundaries and crop/season metadata endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_list_pilot_upazilas(client: TestClient):
    """Verify list of supported pilot Upazilas in Barind and Haor."""
    response = client.get("/api/v1/upazilas")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["count"] == 4
    items = payload["data"]
    ids = [item["upazila_id"] for item in items]
    assert "BD-50-20-30" in ids  # Godagari
    assert "BD-50-20-90" in ids  # Tanore
    assert "BD-60-90-86" in ids  # Sunamganj Sadar
    assert "BD-60-90-89" in ids  # Tahirpur

    # Check centroid structure
    for item in items:
        assert "centroid" in item
        assert "lat" in item["centroid"]
        assert "lon" in item["centroid"]
        assert item["aez_code"] in [21, 26]


def test_get_upazila_detail_canonical(client: TestClient):
    """Verify detailed lookup for canonical Upazila ID."""
    response = client.get("/api/v1/upazilas/BD-50-20-30")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    data = payload["data"]
    assert data["upazila_id"] == "BD-50-20-30"
    assert data["name_en"] == "Godagari"
    assert data["name_bn"] == "গোদাগাড়ী"
    assert data["district_name"] == "Rajshahi"
    assert data["aez_code"] == 26
    assert data["primary_risk"] == "DROUGHT_IRRIGATION"


def test_get_upazila_detail_shorthand_alias(client: TestClient):
    """Verify resolution of shorthand aliases (BD-50-28 -> BD-50-20-30)."""
    response = client.get("/api/v1/upazilas/BD-50-28")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    data = payload["data"]
    assert data["upazila_id"] == "BD-50-20-30"
    assert data["name_en"] == "Godagari"

    res_haor = client.get("/api/v1/upazilas/BD-60-90")
    assert res_haor.status_code == 200
    data_haor = res_haor.json()["data"]
    assert data_haor["upazila_id"] == "BD-60-90-89"
    assert data_haor["name_en"] == "Tahirpur"


def test_get_upazila_not_found(client: TestClient):
    """Verify non-pilot or non-existent Upazila returns HTTP 404."""
    response = client.get("/api/v1/upazilas/BD-99-99-99")
    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == "RESOURCE_NOT_FOUND"
    assert "not found" in data["message"].lower()


def test_get_crops_metadata(client: TestClient):
    """Verify crops metadata returns Boro Rice with calibrated stages."""
    response = client.get("/api/v1/crops")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    crops = payload["data"]
    assert len(crops) >= 1
    boro = crops[0]
    assert boro["crop_id"] == "boro_rice"
    assert "Tillering" in boro["supported_stages"]
    assert "Flowering" in boro["supported_stages"]
    assert boro["calibration_status"] == "PILOT_CALIBRATED"


def test_get_seasons_metadata(client: TestClient):
    """Verify seasons metadata returns Boro, Aus, and Aman seasons."""
    response = client.get("/api/v1/seasons")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    seasons = payload["data"]
    assert len(seasons) == 3
    active_seasons = [s for s in seasons if s["is_active_season"]]
    assert len(active_seasons) == 1
    assert active_seasons[0]["season_id"] == "boro_2026"


def test_geo_hierarchy_and_national_coverage(client: TestClient):
    """Verify Bangladesh administrative hierarchy has 8 divisions, 64 districts, and 495 upazilas."""
    response = client.get("/api/v1/geo/hierarchy")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["divisions"]) == 8
    assert len(data["districts_flat"]) == 64
    assert len(data["upazilas_flat"]) == 495


def test_list_all_64_districts_and_divisions(client: TestClient):
    """Verify all 8 divisions and 64 districts endpoints."""
    # Divisions
    res_div = client.get("/api/v1/geo/divisions")
    assert res_div.status_code == 200
    divs = res_div.json()["data"]
    assert len(divs) == 8
    div_names = [d["name_en"] for d in divs]
    assert "Rajshahi" in div_names
    assert "Sylhet" in div_names
    assert "Dhaka" in div_names
    assert "Chattogram" in div_names

    # Districts
    res_dist = client.get("/api/v1/geo/districts")
    assert res_dist.status_code == 200
    dists = res_dist.json()["data"]
    assert len(dists) == 64

    # All Upazilas
    res_all_upz = client.get("/api/v1/upazilas?all=true")
    assert res_all_upz.status_code == 200
    assert res_all_upz.json()["count"] == 495


def test_expanded_crops_catalog_all_24(client: TestClient):
    """Verify expanded crops catalog includes 24 crops across categories."""
    response = client.get("/api/v1/crops")
    assert response.status_code == 200
    crops = response.json()["data"]
    assert len(crops) >= 24
    crop_ids = [c["crop_id"] for c in crops]
    assert "boro_rice" in crop_ids
    assert "aman_rice" in crop_ids
    assert "aus_rice" in crop_ids
    assert "wheat" in crop_ids
    assert "maize" in crop_ids
    assert "potato" in crop_ids
    assert "jute" in crop_ids
    assert "mustard" in crop_ids
    assert "lentil" in crop_ids
    assert "mango" in crop_ids


def test_custom_date_range_advisories(client: TestClient):
    """Verify advisories accept start_date and end_date and return analysis_period."""
    response = client.get(
        "/api/v1/upazilas/BD-50-20-30/advisories",
        params={
            "crop": "boro_rice",
            "stage": "tillering",
            "start_date": "2026-10-03",
            "end_date": "2026-10-09",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "analysis_period" in payload
    period = payload["analysis_period"]
    assert period["start_date"] == "2026-10-03"
    assert period["end_date"] == "2026-10-09"
    assert period["period_days"] == 7

