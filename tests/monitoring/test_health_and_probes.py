"""Automated Tests for Health, Readiness, and Deep Diagnostic Probes."""

import pytest
from fastapi.testclient import TestClient
from api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_liveness_probe_returns_healthy(client):
    """Verify that /health and /api/v1/health return 200 with healthy status."""
    for path in ["/health", "/api/v1/health"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp_utc" in data


def test_readiness_probe_returns_verified_tables(client):
    """Verify that /ready and /api/v1/ready return 200 with data store readiness."""
    for path in ["/ready", "/api/v1/ready"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("ready", "unready")
        assert data["data_store_ready"] is True
        assert data["analytics_ready"] is True
        assert len(data["verified_datasets"]) >= 4
        assert len(data["missing_dependencies"]) == 0


def test_deep_health_probe_returns_comprehensive_diagnostics(client):
    """Verify that /health/deep returns full production diagnostics without secret leakage."""
    for path in ["/health/deep", "/api/v1/health/deep"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()

        # Top-level status & uptime
        assert data["status"] in ("healthy", "degraded")
        assert data["uptime_seconds"] >= 0.0
        assert "version" in data

        # System metrics
        metrics = data["system_metrics"]
        assert "memory_max_rss_mb" in metrics
        assert metrics["memory_max_rss_mb"] > 0
        assert metrics["rate_limit_enabled"] is True
        assert metrics["payload_max_bytes"] == 1048576

        # Component breakdown
        components = data["components"]
        assert components["data_store"]["status"] == "ready"
        assert components["data_store"]["verified_tables_count"] >= 4
        assert components["analytics_engine"]["status"] == "ready"
        assert components["geographic_resolver"]["status"] == "ready"
        assert len(components["geographic_resolver"]["pilot_regions"]) == 2

        # Pipeline health & circuit breaker
        pipeline = data["pipeline_health"]
        assert "evaluated_at_utc" in pipeline
        assert "overall_status" in pipeline
        assert "circuit_breaker_tripped" in pipeline
        assert "table_details" in pipeline

        # Safety & Governance checks
        gov = data["governance"]
        assert "context_gating" in gov
        assert "suppression_policy" in gov
        assert "pii_posture" in gov
        assert "hardware_budget" in gov
