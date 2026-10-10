"""Master Agricultural Recommendation Engine Coordinator.

Coordinates contextual gating, multi-rule evaluation, automated suppression,
and explainability packaging for Phase 9 decision support.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from analytics.contracts.advisory_schemas import AdvisoryCard, AdvisoryStatus
from analytics.engine.context_gate import ContextGator, ContextGatingError
from analytics.engine.suppression import AdvisorySuppressionEngine
from analytics.engine.explainability import AdvisoryExplainer
from analytics.rules.rule_irr_01 import RuleIrrigationPostponement
from analytics.rules.rule_irr_02 import RuleMoistureDeficitAlert
from analytics.rules.rule_fld_01 import RuleHaorEmergencyHarvest
from analytics.rules.rule_tmp_01 import RuleBootingColdInjury
from analytics.rules.rule_tmp_02 import RuleAnthesisHeatStress


class AgriculturalRecommendationEngine:
    """Master coordinator executing evidence-supported agricultural advisory rules."""

    def __init__(self):
        """Initialize active rules catalog."""
        self.rules = [
            RuleIrrigationPostponement(),
            RuleMoistureDeficitAlert(),
            RuleHaorEmergencyHarvest(),
            RuleBootingColdInjury(),
            RuleAnthesisHeatStress(),
        ]

    def evaluate_all_rules(
        self,
        upazila_id: str,
        crop_name: str,
        growth_stage: str,
        inputs: Dict[str, Any],
        timestamp_utc: Optional[str] = None,
        data_timestamp_utc: Optional[str] = None,
        ensemble_spread_pct: Optional[float] = None,
        rain_prob_pct: Optional[float] = None,
        physical_violations: Optional[list] = None,
    ) -> List[AdvisoryCard]:
        """Execute complete recommendation pipeline for given field context and environmental state.

        Args:
            upazila_id: Target Upazila identifier.
            crop_name: Target crop (e.g. Boro Rice).
            growth_stage: Current validated phenological growth stage.
            inputs: Physical variables dictionary.
            timestamp_utc: Execution timestamp string.
            data_timestamp_utc: Age timestamp of ingested source observations.
            ensemble_spread_pct: NWP multi-model spread percentage.
            rain_prob_pct: 48h precipitation probability percentage.
            physical_violations: List of physical range errors, if any.

        Returns:
            List of generated AdvisoryCard objects.
        """
        # Step 1: Contextual Gating (DEC-17)
        is_valid, error_msg, gate_payload = ContextGator.validate_context(
            upazila_id=upazila_id,
            crop_name=crop_name,
            growth_stage=growth_stage,
        )
        if not is_valid or gate_payload is None:
            raise ContextGatingError(error_msg or "Context validation failed.")

        now_str = (
            timestamp_utc
            if timestamp_utc is not None
            else datetime.now(timezone.utc).isoformat()
        )

        cards: List[AdvisoryCard] = []

        # Step 2: Sequential Rule Evaluation
        for rule in self.rules:
            card = rule.evaluate(
                context=gate_payload,
                inputs=inputs,
                timestamp_utc=now_str,
            )
            if card is not None:
                # Step 3: Automated Suppression Middleware (DEC-10)
                card = AdvisorySuppressionEngine.apply_suppression_if_needed(
                    card=card,
                    data_timestamp_utc=data_timestamp_utc,
                    ensemble_spread_pct=ensemble_spread_pct,
                    rain_prob_pct=rain_prob_pct,
                    physical_violations=physical_violations,
                )
                cards.append(card)

        return cards
