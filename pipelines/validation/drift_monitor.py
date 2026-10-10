"""Data Pipeline Reliability & Distribution Drift Monitor for Ritucast.

Performs dataset freshness auditing against the 36-hour suppression ceiling (DEC-10),
anomaly detection via physical semantic bounds, duplicate-record auditing, and
circuit-breaker safety status evaluation.
"""

from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import pyarrow.parquet as pq

from pipelines.validation.semantic_validator import SemanticValidator


@dataclass
class TableHealthStatus:
    """Health and reliability metrics for an individual Parquet feature table."""
    table_name: str
    exists: bool
    size_bytes: int
    row_count: int
    latest_record_utc: Optional[str]
    age_hours: Optional[float]
    is_stale: bool
    missing_value_pct: float
    duplicate_rows: int
    out_of_bounds_count: int
    status: str  # "HEALTHY", "DEGRADED", "STALE", "MISSING"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PipelineHealthReport:
    """Aggregate health and reliability report across all processed feature tables."""
    evaluated_at_utc: str
    overall_status: str  # "HEALTHY", "DEGRADED", "CRITICAL"
    circuit_breaker_tripped: bool
    recommended_action: str  # "PROCEED", "DEGRADE_CONFIDENCE", "SUPPRESS_ADVISORY"
    stale_tables_count: int
    missing_tables_count: int
    table_details: Dict[str, TableHealthStatus]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evaluated_at_utc": self.evaluated_at_utc,
            "overall_status": self.overall_status,
            "circuit_breaker_tripped": self.circuit_breaker_tripped,
            "recommended_action": self.recommended_action,
            "stale_tables_count": self.stale_tables_count,
            "missing_tables_count": self.missing_tables_count,
            "table_details": {k: v.to_dict() for k, v in self.table_details.items()},
        }


class PipelineDriftMonitor:
    """Monitors processed datasets for staleness, drift, and anomalous sensor inputs."""

    MAX_STALENESS_HOURS = 36.0  # Inviolable ceiling per DEC-10 and NFR-REL-03
    REQUIRED_TABLES = [
        "meteorology_daily_upazila.parquet",
        "forecast_hourly_pilot.parquet",
        "catchment_rainfall_daily.parquet",
        "hydrology_river_stage.parquet",
    ]

    @classmethod
    def audit_table(cls, table_path: Path, table_name: str) -> TableHealthStatus:
        """Audit a single Parquet file for physical bounds, missingness, and staleness."""
        if not table_path.exists():
            return TableHealthStatus(
                table_name=table_name,
                exists=False,
                size_bytes=0,
                row_count=0,
                latest_record_utc=None,
                age_hours=None,
                is_stale=True,
                missing_value_pct=100.0,
                duplicate_rows=0,
                out_of_bounds_count=0,
                status="MISSING",
            )

        stat = table_path.stat()
        size_bytes = stat.st_size
        if size_bytes == 0:
            return TableHealthStatus(
                table_name=table_name,
                exists=True,
                size_bytes=0,
                row_count=0,
                latest_record_utc=None,
                age_hours=None,
                is_stale=True,
                missing_value_pct=100.0,
                duplicate_rows=0,
                out_of_bounds_count=0,
                status="MISSING",
            )

        try:
            arrow_table = pq.read_table(table_path)
            row_count = arrow_table.num_rows
            col_names = arrow_table.column_names

            # Null / missing value calculation
            total_cells = row_count * len(col_names)
            null_cells = sum(arrow_table[c].null_count for c in col_names)
            missing_pct = (null_cells / total_cells * 100.0) if total_cells > 0 else 0.0

            # Inspect modification / generation time
            # Fallback to file mtime if date column is not directly parseable
            mtime_dt = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
            now_utc = datetime.now(timezone.utc)
            age_hours = (now_utc - mtime_dt).total_seconds() / 3600.0
            is_stale = age_hours > cls.MAX_STALENESS_HOURS

            # Audit physical out-of-bounds on numeric rows
            out_of_bounds = 0
            df = arrow_table.to_pandas()
            for _, row in df.head(100).iterrows():
                row_dict = row.to_dict()
                valid, errors = SemanticValidator.validate_meteorology(row_dict)
                if not valid:
                    out_of_bounds += len(errors)

            # Check duplicates
            dup_rows = int(df.duplicated().sum())

            # Determine status
            if is_stale:
                status = "STALE"
            elif missing_pct > 15.0 or out_of_bounds > 10:
                status = "DEGRADED"
            else:
                status = "HEALTHY"

            return TableHealthStatus(
                table_name=table_name,
                exists=True,
                size_bytes=size_bytes,
                row_count=row_count,
                latest_record_utc=mtime_dt.isoformat(),
                age_hours=round(age_hours, 2),
                is_stale=is_stale,
                missing_value_pct=round(missing_pct, 2),
                duplicate_rows=dup_rows,
                out_of_bounds_count=out_of_bounds,
                status=status,
            )

        except Exception:
            return TableHealthStatus(
                table_name=table_name,
                exists=True,
                size_bytes=size_bytes,
                row_count=0,
                latest_record_utc=None,
                age_hours=None,
                is_stale=True,
                missing_value_pct=100.0,
                duplicate_rows=0,
                out_of_bounds_count=0,
                status="DEGRADED",
            )

    @classmethod
    def audit_pipeline(cls, processed_dir: Path) -> PipelineHealthReport:
        """Audit all core agricultural tables and evaluate circuit-breaker state."""
        table_statuses: Dict[str, TableHealthStatus] = {}
        stale_count = 0
        missing_count = 0

        for tbl_name in cls.REQUIRED_TABLES:
            path = processed_dir / tbl_name
            status = cls.audit_table(path, tbl_name)
            table_statuses[tbl_name] = status
            if status.status in ("MISSING",):
                missing_count += 1
            if status.is_stale:
                stale_count += 1

        now_utc = datetime.now(timezone.utc).isoformat()

        # Circuit breaker rules:
        # If any required table is completely missing or critically stale (>36h),
        # trip circuit breaker to protect farmers (DEC-10).
        if missing_count > 0:
            overall = "CRITICAL"
            tripped = True
            action = "SUPPRESS_ADVISORY"
        elif stale_count > 0:
            overall = "DEGRADED"
            tripped = True
            action = "SUPPRESS_ADVISORY"
        else:
            overall = "HEALTHY"
            tripped = False
            action = "PROCEED"

        return PipelineHealthReport(
            evaluated_at_utc=now_utc,
            overall_status=overall,
            circuit_breaker_tripped=tripped,
            recommended_action=action,
            stale_tables_count=stale_count,
            missing_tables_count=missing_count,
            table_details=table_statuses,
        )
