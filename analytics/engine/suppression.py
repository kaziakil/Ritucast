"""Automated Advisory Suppression Policy Middleware (DEC-10, ADR-08).

Advisories must be automatically suppressed and a safe fallback notice displayed whenever:
1. Weather forecast or satellite data is > 36 hours old (NFR-REL-03).
2. Multi-model NWP ensemble spread exceeds 50% with rain probability between 40% and 60%.
3. Input variables violate physical sanity range checks.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple
from analytics.contracts.advisory_schemas import AdvisoryCard, AdvisoryStatus


class AdvisorySuppressionEngine:
    """Evaluates suppression rules before advisory publication."""

    MAX_DATA_LATENCY_HOURS = 36.0

    @classmethod
    def evaluate_suppression(
        cls,
        card: AdvisoryCard,
        data_timestamp_utc: Optional[str] = None,
        ensemble_spread_pct: Optional[float] = None,
        rain_prob_pct: Optional[float] = None,
        physical_violations: Optional[list] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Determine if an advisory must be suppressed according to DEC-10.

        Returns:
            Tuple of (is_suppressed, suppression_reason).
        """
        # 1. Physical sanity check violations
        if physical_violations and len(physical_violations) > 0:
            return True, f"Suppressed: Input physical range violations detected: {physical_violations}"

        # 2. Data freshness check (> 36 hours latency)
        if data_timestamp_utc:
            try:
                dt_data = datetime.fromisoformat(data_timestamp_utc.replace("Z", "+00:00"))
                dt_now = datetime.now(timezone.utc)
                age_hours = (dt_now - dt_data).total_seconds() / 3600.0
                if age_hours > cls.MAX_DATA_LATENCY_HOURS:
                    return (
                        True,
                        f"Suppressed: Data latency exceeds 36-hour safety limit ({round(age_hours, 1)}h old).",
                    )
            except Exception:
                pass

        # 3. Ensemble spread > 50% with ambiguous rain probability (40% - 60%)
        if ensemble_spread_pct is not None and rain_prob_pct is not None:
            if (ensemble_spread_pct > 50.0) and (40.0 <= rain_prob_pct <= 60.0):
                return (
                    True,
                    (
                        f"Suppressed: NWP ensemble spread exceeds 50% ({round(ensemble_spread_pct, 1)}%) "
                        f"with ambiguous rain probability ({round(rain_prob_pct, 1)}%)."
                    ),
                )

        return False, None

    @classmethod
    def apply_suppression_if_needed(
        cls,
        card: AdvisoryCard,
        data_timestamp_utc: Optional[str] = None,
        ensemble_spread_pct: Optional[float] = None,
        rain_prob_pct: Optional[float] = None,
        physical_violations: Optional[list] = None,
    ) -> AdvisoryCard:
        """Apply suppression state and fallback copy if suppression conditions are met."""
        is_suppressed, reason = cls.evaluate_suppression(
            card=card,
            data_timestamp_utc=data_timestamp_utc,
            ensemble_spread_pct=ensemble_spread_pct,
            rain_prob_pct=rain_prob_pct,
            physical_violations=physical_violations,
        )

        if is_suppressed:
            card.status = AdvisoryStatus.SUPPRESSED
            card.suppression_reason = reason
            card.plain_language_bn = (
                "উচ্চ আবহাওয়াগত অনিশ্চয়তা বা তথ্যের বিলম্বের কারণে স্বয়ংক্রিয় পরামর্শ সাময়িকভাবে স্থগিত রাখা হয়েছে। "
                "সেচ বা ফসল ব্যবস্থাপনার যেকোনো সিদ্ধান্তের জন্য স্থানীয় উপসহকারী কৃষি কর্মকর্তার (SAAO) সাথে যোগাযোগ করুন।"
            )
            card.headline_bn = "পরামর্শ স্থগিত (উচ্চ পূর্বাভাস অনিশ্চয়তা)"

        return card
