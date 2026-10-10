"""RULE-TMP-02: Boro Rice Anthesis Terminal Heat Stress Warning.

Evidence-supported rule warning of pre-monsoon heatwaves during morning flowering
and advising water buffering to prevent floret desiccation (FR-ADV-03, FR-ENV-02).
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from analytics.rules.base_rule import BaseAgriculturalRule
from analytics.contracts.advisory_schemas import (
    AdvisoryCard,
    AdvisorySeverity,
    AdvisoryStatus,
    ContextGatePayload,
)


class RuleAnthesisHeatStress(BaseAgriculturalRule):
    """Evaluates maximum temperature forecasts against the 35°C critical anthesis threshold."""

    RULE_ID = "RULE-TMP-02"
    RULE_NAME = "Anthesis Terminal Heat Stress Warning"
    CLASSIFICATION = "Evidence-Supported"

    SUPPORTED_STAGES = ["ANTHESIS", "FLOWERING", "HEADING"]

    def evaluate(
        self,
        context: ContextGatePayload,
        inputs: Dict[str, Any],
        timestamp_utc: str,
    ) -> Optional[AdvisoryCard]:
        """Evaluate heat stress trigger conditions.

        Triggers:
        1. Tmax >= 35.0°C for >= 2 consecutive days
        2. Growth stage is Anthesis / Flowering
        """
        stage_key = context.growth_stage.upper().replace(" ", "_")
        if stage_key not in self.SUPPORTED_STAGES:
            return None

        t_max_forecast = inputs.get("t_max_c", 30.0)
        consecutive_days = inputs.get("consecutive_heat_days", 1)

        is_triggered = (t_max_forecast >= 35.0) and (consecutive_days >= 2)
        if not is_triggered:
            return None

        try:
            dt_now = datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))
            valid_until = (dt_now + timedelta(hours=48)).isoformat()
        except Exception:
            valid_until = timestamp_utc

        return AdvisoryCard(
            advisory_id=f"ADV-TMP02-{context.upazila_id}-{timestamp_utc[:10]}",
            rule_id=self.RULE_ID,
            upazila_id=context.upazila_id,
            crop_name=context.crop_name,
            growth_stage=context.growth_stage,
            timestamp_utc=timestamp_utc,
            valid_until_utc=valid_until,
            severity=AdvisorySeverity.WARNING,
            status=AdvisoryStatus.ACTIVE,
            headline_bn="তীব্র তাপদাহ সতর্কতা (সতর্কবার্তা)",
            plain_language_bn=(
                f"আগামী কয়েকদিন দিনের তাপমাত্রা ৩৫ ডিগ্রি সেলসিয়াসের বেশি হতে পারে "
                f"(সর্বোচ্চ আনুমানিক {round(t_max_forecast, 1)}°C)। এই সময়ে জমিতে ফুল ফোটার পরাগায়ন বিঘ্নিত হতে পারে। "
                f"পরাগায়ন সচল রাখতে জমিতে পর্যাপ্ত রস ও ৩–৫ সেমি পানি ধরে রাখুন।"
            ),
            action_items_bn=[
                "সকাল ৯টা থেকে দুপুর ১২টা পর্যন্ত জমির ক্যানোপি ঠান্ডা রাখতে ৩–৫ সেমি পানি ধরে রাখুন।",
                "তীব্র রোদে ফুল শুকিয়ে যাওয়া রোধে বিকেলে হালকা সেচ দিন।",
            ],
            field_verification_bn="সেচ দেওয়ার আগে জমিতে পর্যাপ্ত রস আছে কি না হাত দিয়ে পরীক্ষা করুন।",
            uncertainty_description_bn="তাপমাত্রার পূর্বাভাস সংখ্যাসূচক আবহাওয়া মডেল (NWP) ভিত্তিক।",
            supporting_indicators={
                "t_max_c": t_max_forecast,
                "consecutive_heat_days": consecutive_days,
                "threshold_c": 35.0,
            },
            provenance_manifest={
                "forecast_provider": "Open-Meteo/ECMWF",
                "agronomic_reference": "BRRI-Heat-Manual-2020",
            },
        )
