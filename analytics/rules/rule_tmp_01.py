"""RULE-TMP-01: Boro Rice Booting Stage Cold Injury Warning.

Evidence-supported rule warning of low night temperatures during pollen meiosis
and advising standing water depth buffering (FR-ADV-03, FR-ENV-02).
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


class RuleBootingColdInjury(BaseAgriculturalRule):
    """Evaluates minimum temperature forecasts against the 15°C critical threshold."""

    RULE_ID = "RULE-TMP-01"
    RULE_NAME = "Booting Stage Cold Injury Warning"
    CLASSIFICATION = "Evidence-Supported"

    SUPPORTED_STAGES = ["BOOTING", "PANICLE_INITIATION", "REPRODUCTIVE"]

    def evaluate(
        self,
        context: ContextGatePayload,
        inputs: Dict[str, Any],
        timestamp_utc: str,
    ) -> Optional[AdvisoryCard]:
        """Evaluate cold stress trigger conditions.

        Triggers:
        1. Tmin <= 15.0°C for >= 3 consecutive days
        2. Growth stage is Booting / Panicle Initiation
        """
        stage_key = context.growth_stage.upper().replace(" ", "_")
        if stage_key not in self.SUPPORTED_STAGES:
            return None

        t_min_forecast = inputs.get("t_min_c", 20.0)
        consecutive_days = inputs.get("consecutive_cold_days", 1)

        is_triggered = (t_min_forecast <= 15.0) and (consecutive_days >= 3)
        if not is_triggered:
            return None

        try:
            dt_now = datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))
            valid_until = (dt_now + timedelta(hours=72)).isoformat()
        except Exception:
            valid_until = timestamp_utc

        return AdvisoryCard(
            advisory_id=f"ADV-TMP01-{context.upazila_id}-{timestamp_utc[:10]}",
            rule_id=self.RULE_ID,
            upazila_id=context.upazila_id,
            crop_name=context.crop_name,
            growth_stage=context.growth_stage,
            timestamp_utc=timestamp_utc,
            valid_until_utc=valid_until,
            severity=AdvisorySeverity.WARNING,
            status=AdvisoryStatus.ACTIVE,
            headline_bn="শৈত্যপ্রবাহ ও বন্ধ্যাত্ব ঝুঁকি (সতর্কবার্তা)",
            plain_language_bn=(
                f"আগামী ৩ দিন রাতের তাপমাত্রা ১৫ ডিগ্রি সেলসিয়াসের নিচে নেমে যাওয়ার আশঙ্কা রয়েছে "
                f"(সর্বনিম্ন আনুমানিক {round(t_min_forecast, 1)}°C)। ধানের শীষ গজানোর এই সময়ে ঠান্ডা লাগলে "
                f"শীষ সাদা হয়ে চিটা হতে পারে। ঠান্ডা থেকে ফসল বাঁচাতে জমিতে রাতে ৫–৭ সেন্টিমিটার পানি ধরে রাখুন।"
            ),
            action_items_bn=[
                "সন্ধ্যায় জমিতে ৫–৭ সেমি গভীরতায় সেচের পানি প্রবেশ করান।",
                "সকালে অতিরিক্ত ঠান্ডা পানি নিষ্কাশন করে নতুন পানি দিন।",
                "শৈত্যপ্রবাহ চলাকালীন ইউরিয়া সারের উপরিপ্রয়োগ বন্ধ রাখুন।",
            ],
            field_verification_bn="জমিতে পানি দেওয়ার আগে ধানের থোড় ও শীষের বৃদ্ধির অবস্থা পর্যবেক্ষণ করুন।",
            uncertainty_description_bn="তাপমাত্রার পূর্বাভাস সংখ্যাসূচক আবহাওয়া মডেল (NWP) ভিত্তিক।",
            supporting_indicators={
                "t_min_c": t_min_forecast,
                "consecutive_cold_days": consecutive_days,
                "threshold_c": 15.0,
            },
            provenance_manifest={
                "forecast_provider": "Open-Meteo/ECMWF",
                "agronomic_reference": "BRRI-Cold-Manual-2019",
            },
        )
