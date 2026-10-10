"""
Data Quality Reporting & Audit Summary Generator.
"""

from typing import Dict, Any, List
import json
import os
from pipelines.common.models import QualityAuditSummary

class QualityReporter:
    """Collects validation outcomes and generates machine- and human-readable quality reports."""

    def __init__(self):
        self.stats_by_dataset: Dict[str, Dict[str, Any]] = {}

    def record_outcome(
        self,
        dataset_name: str,
        received: int,
        accepted: int,
        rejected: int,
        missing_fields_count: int = 0,
        errors: List[str] = None,
    ):
        """Records validation audit for a dataset."""
        self.stats_by_dataset[dataset_name] = {
            "records_received": received,
            "records_accepted": accepted,
            "records_rejected": rejected,
            "missing_fields_count": missing_fields_count,
            "errors": errors or [],
        }

    def get_summary(self) -> QualityAuditSummary:
        """Returns consolidated QualityAuditSummary."""
        total_checked = sum(d["records_received"] for d in self.stats_by_dataset.values())
        total_passed = sum(d["records_accepted"] for d in self.stats_by_dataset.values())
        total_rejected = sum(d["records_rejected"] for d in self.stats_by_dataset.values())
        total_warnings = sum(d["missing_fields_count"] for d in self.stats_by_dataset.values())

        status = "PASS" if total_rejected == 0 else ("PARTIAL" if total_passed > 0 else "FAIL")

        return QualityAuditSummary(
            total_records_checked=total_checked,
            passed_count=total_passed,
            rejected_count=total_rejected,
            warnings_count=total_warnings,
            status=status,
        )

    def write_json_report(self, filepath: str):
        """Writes machine-readable JSON quality report."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        summary = self.get_summary()
        payload = {
            "summary": summary.model_dump(),
            "datasets": self.stats_by_dataset,
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def generate_markdown_report(self) -> str:
        """Generates human-readable Markdown quality report table."""
        summary = self.get_summary()
        lines = [
            "# Ritucast Data Quality Audit Report",
            "",
            f"**Overall Status**: `{summary.status}` | **Total Records**: `{summary.total_records_checked}` | **Passed**: `{summary.passed_count}` | **Rejected**: `{summary.rejected_count}`",
            "",
            "| Dataset | Received | Accepted | Rejected | Missing / Warnings | Error Samples |",
            "| :--- | :---: | :---: | :---: | :---: | :--- |",
        ]

        for d_name, d_stats in self.stats_by_dataset.items():
            err_sample = "; ".join(d_stats["errors"][:2]) if d_stats["errors"] else "None"
            lines.append(
                f"| **{d_name}** | {d_stats['records_received']} | {d_stats['records_accepted']} | {d_stats['records_rejected']} | {d_stats['missing_fields_count']} | {err_sample} |"
            )

        return "\n".join(lines)
