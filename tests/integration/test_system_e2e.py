"""Comprehensive End-to-End System Integration Test Suite for Phase 12.

Validates the full system flow:
Raw Sample Data -> Ingestion Pipeline -> Parquet Tables -> Data Repository ->
Analytics Engine -> FastAPI REST API -> 4-Tier Advisories & Safety Guardrails.
"""

import os
import shutil
import tempfile
import pytest
from fastapi.testclient import TestClient

from pipelines.orchestrator import PipelineOrchestrator
from api.data_access.repository import AgriculturalDataRepository
from api.dependencies import get_repository
from api.main import app


@pytest.fixture(scope="module")
def e2e_system_env():
    """Runs data pipeline to generate fresh Parquet tables in a temporary directory

    and sets up an AgriculturalDataRepository and TestClient hooked to it.
    """
    temp_dir = tempfile.mkdtemp(prefix="ritucast_e2e_")

    try:
        # 1. Run pipeline orchestrator to produce Parquet feature tables
        orchestrator = PipelineOrchestrator(
            output_dir=temp_dir,
            use_sample=True,
            dry_run=False,
        )
        pipeline_result = orchestrator.run(
            datasets=["all"],
            upazila_scope="pilot",
            start_date="2026-03-01",
            end_date="2026-03-05",
        )
        assert pipeline_result["status"] == "PASS", f"Pipeline failed: {pipeline_result}"

        # 2. Instantiate repository pointing to the newly generated artifacts
        test_repo = AgriculturalDataRepository(
            processed_dir=temp_dir,
            sample_dir="data/sample",
        )

        # 3. Create FastAPI client with dependency override
        app.dependency_overrides[get_repository] = lambda: test_repo
        client = TestClient(app)

        yield {
            "temp_dir": temp_dir,
            "repo": test_repo,
            "client": client,
        }

    finally:
        app.dependency_overrides.clear()
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_e2e_health_and_readiness(e2e_system_env):
    """Verify system readiness reflects generated Parquet tables."""
    client: TestClient = e2e_system_env["client"]

    # Health probe
    res_health = client.get("/health")
    assert res_health.status_code == 200
    health_data = res_health.json()
    assert health_data["status"] == "healthy"

    # Readiness probe
    res_ready = client.get("/ready")
    assert res_ready.status_code == 200
    ready_data = res_ready.json()
    assert ready_data["status"] == "ready"
    assert ready_data["data_store_ready"] is True
    assert ready_data["analytics_ready"] is True
    assert len(ready_data["verified_datasets"]) >= 4


def test_e2e_pilot_geographic_and_crop_metadata(e2e_system_env):
    """Verify geographic and crop metadata across pilot testbeds."""
    client: TestClient = e2e_system_env["client"]

    # Upazilas list
    res_upz = client.get("/api/v1/upazilas")
    assert res_upz.status_code == 200
    upz_data = res_upz.json()
    assert upz_data["status"] == "success"
    assert upz_data["count"] == 4

    uids = {u["upazila_id"] for u in upz_data["data"]}
    assert "BD-50-20-30" in uids  # Godagari
    assert "BD-50-20-90" in uids  # Tanore
    assert "BD-60-90-86" in uids  # Sunamganj Sadar
    assert "BD-60-90-89" in uids  # Tahirpur

    # Detail check with shorthand alias resolution
    res_alias = client.get("/api/v1/upazilas/BD-50-28")
    assert res_alias.status_code == 200
    assert res_alias.json()["data"]["upazila_id"] == "BD-50-20-30"

    # Crops list
    res_crops = client.get("/api/v1/crops")
    assert res_crops.status_code == 200
    crops = res_crops.json()["data"]
    assert any(c["crop_id"] == "boro_rice" for c in crops)


def test_e2e_weather_and_water_balance_flow(e2e_system_env):
    """Verify end-to-end data flow from meteorology to FAO-56 water balance."""
    client: TestClient = e2e_system_env["client"]

    # 1. Weather feed
    res_weather = client.get("/api/v1/upazilas/BD-50-20-30/weather")
    assert res_weather.status_code == 200
    w_data = res_weather.json()
    assert "tier_1_observations" in w_data
    assert "tier_3_forecasts" in w_data
    assert len(w_data["tier_3_forecasts"]["daily_forecast"]) >= 1

    # 2. Water balance with contextual gating (DEC-17)
    res_wb = client.get(
        "/api/v1/upazilas/BD-50-20-30/water-balance",
        params={"crop": "boro_rice", "stage": "Tillering"},
    )
    assert res_wb.status_code == 200
    wb_data = res_wb.json()
    t2 = wb_data["tier_2_indicators"]

    # Physical indicator assertions
    assert t2["fao56_et0_mm_day"] > 0.0
    assert t2["calibrated_kc"] > 0.0
    assert t2["crop_etc_mm_day"] > 0.0
    assert t2["current_soil_water_deficit_dt_mm"] >= 0.0
    assert t2["status"] in ["AWD_DRYING_PERMISSIBLE", "IRRIGATION_RECOMMENDED", "CRITICAL_DEFICIT"]
    assert t2["soil_properties"]["total_available_water_taw_mm"] == 56.0
    assert t2["soil_properties"]["readily_available_water_raw_mm"] == 19.6


def test_e2e_haor_flood_hazard_and_pilot_bounds(e2e_system_env):
    """Verify transboundary flood index in Haor vs non-applicability in Barind."""
    client: TestClient = e2e_system_env["client"]

    # Tahirpur (Haor Basin)
    res_haor = client.get("/api/v1/upazilas/BD-60-90-89/flood-hazard")
    assert res_haor.status_code == 200
    h_data = res_haor.json()["tier_2_indicators"]
    assert h_data["flood_hazard_index_iflood"] >= 0.0
    assert h_data["hazard_tier"] in ["NORMAL", "ADVISORY", "WARNING", "EMERGENCY"]
    assert "f_P" in h_data["sub_indices"]
    assert "f_S" in h_data["sub_indices"]

    # Godagari (High Barind Tract - Outside Haor)
    res_barind = client.get("/api/v1/upazilas/BD-50-20-30/flood-hazard")
    assert res_barind.status_code == 200
    b_data = res_barind.json()["tier_2_indicators"]
    assert b_data["hazard_tier"] == "NOT_APPLICABLE"
    assert b_data["trigger_early_harvest"] is False


def test_e2e_four_tier_advisory_generation_and_safety(e2e_system_env):
    """Verify complete 4-tier advisory output and anti-overconfidence enforcement."""
    client: TestClient = e2e_system_env["client"]

    # Request advisory for Godagari tillering stage
    res = client.get(
        "/api/v1/upazilas/BD-50-20-30/advisories",
        params={"crop": "boro_rice", "stage": "Tillering"},
    )
    assert res.status_code == 200
    data = res.json()

    # Four-Tier Separation (DEC-08)
    assert "tier_1_observations" in data
    assert "tier_2_indicators" in data
    assert "tier_3_predictions" in data
    assert "tier_4_recommendation" in data

    t4 = data["tier_4_recommendation"]
    assert t4["rule_id"].startswith("RULE-")
    assert len(t4["headline_bn"]) > 0
    assert len(t4["body_bn"]) > 0
    assert t4["confidence"]["score"] > 0.0

    # Mandatory field verification copy (DEC-10, AGENTS.md)
    disclaimer = t4["mandatory_disclaimer_bn"]
    assert "সেচ বন্ধ" in disclaimer or "মাটির রস" in disclaimer
    assert "পরীক্ষা করুন" in disclaimer

    # Anti-overconfidence linguistic check (AGENTS.md)
    banned_terms = ["১০০% নিশ্চিত", "নিশ্চিত বৃষ্টি", "ফলনের নিশ্চয়তা"]
    full_text = str(data)
    for term in banned_terms:
        assert term not in full_text, f"Banned overconfident term '{term}' found in advisory!"


def test_e2e_contextual_gating_and_error_envelopes(e2e_system_env):
    """Verify contextual gating rejections and uniform error envelopes."""
    client: TestClient = e2e_system_env["client"]

    # 1. Missing crop & stage -> 422
    res_ungated = client.get("/api/v1/upazilas/BD-50-20-30/advisories")
    assert res_ungated.status_code == 422
    err_ungated = res_ungated.json()
    assert err_ungated["status"] == "error"
    assert err_ungated["code"] in ["REQUEST_VALIDATION_ERROR", "VALIDATION_ERROR"]
    assert "timestamp_utc" in err_ungated

    # 2. Unknown Upazila -> 404
    res_404 = client.get("/api/v1/upazilas/BD-99-99-99")
    assert res_404.status_code == 404
    err_404 = res_404.json()
    assert err_404["status"] == "error"
    assert err_404["code"] in ["RESOURCE_NOT_FOUND", "UPAZILA_NOT_FOUND"]


def test_e2e_provenance_and_non_goals(e2e_system_env):
    """Verify system provenance reports verified datasets, methodologies, and DEC-06 non-goals."""
    client: TestClient = e2e_system_env["client"]

    res_prov = client.get("/api/v1/provenance")
    assert res_prov.status_code == 200
    prov_data = res_prov.json()

    # Datasets
    ds_names = [d["dataset_id"] for d in prov_data["datasets"]]
    assert "DATA-MET-01" in ds_names
    assert "DATA-FCST-01" in ds_names

    # Methodologies
    methods = [m["method_id"] for m in prov_data["scientific_methodologies"]]
    assert "EQN-ET0-01" in methods
    assert "IDX-FLD-01" in methods

    # Scientific boundaries (DEC-06 Non-Goals)
    bounds = prov_data["scientific_boundaries"]
    assert "yield_prediction" in bounds
    assert "chemical_diagnosis" in bounds
    assert "hardware_actuation" in bounds
