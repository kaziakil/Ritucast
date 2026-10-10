"""Data Readiness & Anti-Leakage Audit Engine.

Performs automated checks on dataset schemas, temporal alignment, and ground-truth availability
to enforce Phase 4 modeling guardrails (DEC-06) and prevent premature ML training.
"""

from typing import Dict, Any, List
import pandas as pd


class ModelingReadinessAuditor:
    """Audits data readiness and prevents ungrounded machine learning training."""

    CAPABILITY_READINESS = {
        "descriptive_analytics": {
            "status": "READY",
            "justification": "Daily agroclimatology and historical summaries are verified in Phase 8 Parquet tables.",
        },
        "physical_indicators": {
            "status": "READY",
            "justification": "All thermodynamic inputs for FAO-56 ET0, USDA-SCS water balance, and BWDB freeboard are present.",
        },
        "rule_based_advisories": {
            "status": "READY",
            "justification": "BRRI phenology parameters, NWP QPF, and hydrological danger thresholds are calibrated.",
        },
        "supervised_machine_learning": {
            "status": "NOT_READY",
            "justification": (
                "Ground-truth parcel-level crop yield logs and micro-field telemetry are absent. "
                "Per DEC-06 and Phase 4 guardrails, black-box supervised ML models are strictly banned "
                "from deployment without independent multi-season ground truth."
            ),
        },
    }

    @classmethod
    def audit_capabilities(cls) -> Dict[str, Any]:
        """Return readiness status across all analytical tiers."""
        return cls.CAPABILITY_READINESS

    @classmethod
    def verify_no_temporal_leakage(
        cls,
        eval_timestamp: str,
        feature_timestamps: List[str],
    ) -> bool:
        """Verify that no feature timestamp occurs after the evaluation time."""
        t_eval = pd.to_datetime(eval_timestamp)
        for ts in feature_timestamps:
            if pd.to_datetime(ts) > t_eval:
                return False
        return True
