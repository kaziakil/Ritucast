"""Tests for health and readiness probes."""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Confirm liveness probe returns HTTP 200 and status healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp_utc" in data

    # Versioned alias
    res_v1 = client.get("/api/v1/health")
    assert res_v1.status_code == 200
    assert res_v1.json()["status"] == "healthy"


def test_readiness_probe(client: TestClient):
    """Confirm readiness probe verifies parquet tables and analytics dependencies."""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["data_store_ready"] is True
    assert data["analytics_ready"] is True
    assert len(data["verified_datasets"]) >= 4
    assert len(data["missing_dependencies"]) == 0

    # Versioned alias
    res_v1 = client.get("/api/v1/ready")
    assert res_v1.status_code == 200
    assert res_v1.json()["status"] == "ready"
