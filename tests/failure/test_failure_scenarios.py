"""
Failure Scenario & Network Resilience Tests.
"""

from unittest.mock import patch, MagicMock
import pytest
import requests

from pipelines.common.exceptions import NetworkError, RateLimitError, SchemaValidationError
from pipelines.common.base_adapter import BaseAdapter
from pipelines.ingestion.nasa_power import NasaPowerAdapter
from pipelines.validation.schema_validator import validate_record, MeteorologyDailySchema

class DummyAdapter(BaseAdapter):
    def fetch_live(self, **kwargs):
        return self._execute_http_get("https://example.com/api")
    def load_sample(self, fixture_path=None):
        return {}

def test_adapter_retries_on_timeout_and_eventually_fails():
    adapter = DummyAdapter(
        source_id="TEST-01",
        name="Test Timeout",
        timeout_seconds=1,
        max_retries=2,
        backoff_factor=1.0,
    )

    with patch.object(adapter.session, "get", side_effect=requests.exceptions.Timeout("Connection timed out")):
        with pytest.raises(NetworkError) as exc_info:
            adapter.fetch_live()
        assert "retries" in str(exc_info.value).lower()

def test_adapter_rate_limit_429():
    adapter = DummyAdapter(
        source_id="TEST-02",
        name="Test 429",
        timeout_seconds=1,
        max_retries=1,
        backoff_factor=1.0,
    )

    mock_resp = MagicMock()
    mock_resp.status_code = 429
    with patch.object(adapter.session, "get", return_value=mock_resp):
        with pytest.raises(NetworkError):
            adapter.fetch_live()

def test_missing_mandatory_field_raises_validation_error():
    corrupt_rec = {
        # Missing upazila_id
        "date": "2026-03-01",
        "t2m_c": 25.0,
    }
    with pytest.raises(SchemaValidationError):
        validate_record(MeteorologyDailySchema, corrupt_rec)
