"""Explainability and Scientific Attribution Engine.

Produces transparent, agronomically interpretable explanations for why an advisory was emitted,
including parameter audits, rule traces, and uncertainty boundaries.
"""

from typing import Dict, Any, List
from analytics.contracts.advisory_schemas import AdvisoryCard


class AdvisoryExplainer:
    """Compiles transparent audit logs and user-facing explanations for advisory decisions."""

    @classmethod
    def generate_explanation_report(cls, card: AdvisoryCard) -> Dict[str, Any]:
        """Compile complete explainability payload for a generated advisory card.

        Returns:
            Dictionary containing agronomic rationale, parameter inputs, and caveats.
        """
        return {
            "advisory_id": card.advisory_id,
            "rule_id": card.rule_id,
            "severity": card.severity.value,
            "status": card.status.value,
            "summary_bn": card.plain_language_bn,
            "parameter_audit": card.supporting_indicators,
            "data_provenance": card.provenance_manifest,
            "field_check_mandatory": card.field_verification_bn,
            "uncertainty_statement": card.uncertainty_description_bn,
            "is_suppressed": card.status.value == "SUPPRESSED",
            "suppression_reason": card.suppression_reason,
        }
