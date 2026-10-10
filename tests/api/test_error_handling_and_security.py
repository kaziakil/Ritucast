"""Tests for error handling, CORS headers, and OpenAPI specification contract."""

import pytest
from fastapi.testclient import TestClient


def test_structured_error_response_format(client: TestClient):
    """Verify all error responses follow consistent envelope structure."""
    response = client.get("/api/v1/upazilas/INVALID_ID")
    assert response.status_code == 404
    payload = response.json()
    assert payload["status"] == "error"
    assert "code" in payload
    assert "message" in payload
    assert "timestamp_utc" in payload


def test_validation_error_envelope(client: TestClient):
    """Verify Pydantic request validation errors return structured 422 envelope."""
    # Send invalid type for risk evaluation request (missing required fields)
    response = client.post("/api/v1/risk/evaluate", json={"upazila_id": 12345})
    assert response.status_code == 422
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["code"] in ["VALIDATION_ERROR", "CONTEXT_GATING_FAILED", "REQUEST_VALIDATION_ERROR"]
    assert "message" in payload


def test_cors_headers_configured(client: TestClient):
    """Verify CORS middleware responds with permitted origin."""
    response = client.options(
        "/api/v1/upazilas",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_openapi_schema_endpoint(client: TestClient):
    """Verify OpenAPI 3.0 schema generation and endpoint accessibility."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["openapi"].startswith("3.")
    assert "info" in schema
    assert schema["info"]["title"] == "Ritucast Agricultural Intelligence API"
    paths = schema["paths"]
    assert "/api/v1/upazilas" in paths
    assert "/api/v1/upazilas/{upazila_id}/weather" in paths
    assert "/api/v1/upazilas/{upazila_id}/water-balance" in paths
    assert "/api/v1/upazilas/{upazila_id}/flood-hazard" in paths
    assert "/api/v1/upazilas/{upazila_id}/advisories" in paths
    assert "/api/v1/risk/evaluate" in paths
    assert "/api/v1/provenance" in paths
