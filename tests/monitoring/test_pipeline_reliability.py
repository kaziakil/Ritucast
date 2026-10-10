"""Automated Tests for Data Pipeline Reliability, Freshness, and Circuit Breakers."""

from pathlib import Path
import pytest
from pipelines.validation.drift_monitor import (
    PipelineDriftMonitor,
    TableHealthStatus,
    PipelineHealthReport,
)


@pytest.fixture
def processed_dir():
    # Returns the repository's processed feature tables directory
    return Path(__file__).resolve().parents[2] / "data" / "processed"


def test_drift_monitor_audits_existing_parquet_tables(processed_dir):
    """Verify that existing processed Parquet feature tables are audited cleanly."""
    report = PipelineDriftMonitor.audit_pipeline(processed_dir)

    assert isinstance(report, PipelineHealthReport)
    assert report.missing_tables_count == 0
    assert len(report.table_details) == 4

    for name, table_status in report.table_details.items():
        assert isinstance(table_status, TableHealthStatus)
        assert table_status.exists is True
        assert table_status.size_bytes > 0
        assert table_status.row_count > 0
        assert table_status.missing_value_pct <= 15.0


def test_drift_monitor_detects_missing_table(tmp_path):
    """Verify that a missing table is correctly flagged and trips the circuit breaker."""
    report = PipelineDriftMonitor.audit_pipeline(tmp_path)

    assert report.missing_tables_count == 4
    assert report.overall_status == "CRITICAL"
    assert report.circuit_breaker_tripped is True
    assert report.recommended_action == "SUPPRESS_ADVISORY"


def test_drift_monitor_circuit_breaker_contract():
    """Verify circuit-breaker serialization to dict for deep health endpoints."""
    report = PipelineDriftMonitor.audit_pipeline(Path("non_existent_directory"))
    d = report.to_dict()

    assert "evaluated_at_utc" in d
    assert "overall_status" in d
    assert "circuit_breaker_tripped" in d
    assert "recommended_action" in d
    assert "table_details" in d
