"""Automated Tests for Structured JSON Logging, Correlation IDs, and Redaction."""

import json
import logging
import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.logging_config import (
    scrub_sensitive_value,
    StructuredJsonFormatter,
    correlation_id_ctx,
)


@pytest.fixture
def client():
    return TestClient(app)


def test_correlation_id_header_preserved_and_returned(client):
    """Verify that incoming X-Correlation-ID is preserved and returned in the response."""
    custom_cid = "test-corr-id-9988"
    response = client.get("/api/v1/upazilas", headers={"X-Correlation-ID": custom_cid})
    assert response.status_code == 200
    assert response.headers.get("X-Correlation-ID") == custom_cid


def test_correlation_id_auto_generated_when_missing(client):
    """Verify that an auto-generated correlation ID (req_...) is injected when header is missing."""
    response = client.get("/api/v1/upazilas")
    assert response.status_code == 200
    cid = response.headers.get("X-Correlation-ID")
    assert cid is not None
    assert cid.startswith("req_")


def test_sensitive_data_scrubbing_redacts_tokens_and_passwords():
    """Verify that scrub_sensitive_value redacts credentials and preserves agrarian parameters."""
    test_data = {
        "upazila_id": "BD-50-20-30",
        "crop": "boro_rice",
        "api_key": "secret-token-12345",
        "auth_token": "Bearer xyz-999",
        "db_password": "super-secret-password",
        "soil_water_deficit_mm": 24.5,
        "nested": {
            "private_key": "-----BEGIN RSA PRIVATE KEY-----",
            "fao56_et0": 3.8,
        },
    }

    scrubbed = {k: scrub_sensitive_value(k, v) for k, v in test_data.items()}

    # Agronomic fields preserved
    assert scrubbed["upazila_id"] == "BD-50-20-30"
    assert scrubbed["crop"] == "boro_rice"
    assert scrubbed["soil_water_deficit_mm"] == 24.5
    assert scrubbed["nested"]["fao56_et0"] == 3.8

    # Sensitive fields scrubbed
    assert scrubbed["api_key"] == "[REDACTED]"
    assert scrubbed["auth_token"] == "[REDACTED]"
    assert scrubbed["db_password"] == "[REDACTED]"
    assert scrubbed["nested"]["private_key"] == "[REDACTED]"


def test_structured_json_formatter_produces_valid_json():
    """Verify that StructuredJsonFormatter emits valid JSON with all required log attributes."""
    formatter = StructuredJsonFormatter()
    record = logging.LogRecord(
        name="ritucast.test",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Advisory evaluated successfully",
        args=(),
        exc_info=None,
    )
    record.correlation_id = "cid-abc-123"
    record.duration_ms = 12.4
    record.http_status = 200
    record.method = "GET"
    record.path = "/api/v1/advisories"

    formatted_str = formatter.format(record)
    parsed = json.loads(formatted_str)

    assert parsed["level"] == "INFO"
    assert parsed["logger"] == "ritucast.test"
    assert parsed["message"] == "Advisory evaluated successfully"
    assert parsed["correlation_id"] == "cid-abc-123"
    assert parsed["duration_ms"] == 12.4
    assert parsed["http_status"] == 200
    assert parsed["method"] == "GET"
    assert parsed["path"] == "/api/v1/advisories"
    assert "timestamp_utc" in parsed
