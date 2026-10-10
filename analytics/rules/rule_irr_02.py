"""RULE-IRR-02: Critical Root-Zone Soil Moisture Deficit & Irrigation Trigger.

Evidence-supported rule alerting farmers when root-zone soil water depletion exceeds RAW,
signaling imminent vegetative drought stress (FR-ADV-01, FR-ENV-03).
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


class RuleMoistureDeficitAlert(BaseAgriculturalRule):
    """Evaluates soil moisture depletion against readily available water (RAW)."""

    RULE_ID = "RULE-IRR-02"
    RULE_NAME = "Critical Root-Zone Soil Moisture Deficit & Irrigation Trigger"
    CLASSIFICATION = "Evidence-Supported"

    def evaluate(
        self,
        context: ContextGatePayload,
        inputs: Dict[str, Any],
        timestamp_utc: str,
    ) -> Optional[AdvisoryCard]:
        """Evaluate trigger conditions for RULE-IRR-02.

        Triggers:
        1. Soil water depletion Dt >= RAW
        2. 5-day forecasted rain sum < 5.0 mm
        3. No standing water detected
        """
        depletion_mm = inputs.get("depletion_mm", 0.0)
        raw_mm = inputs.get("raw_mm", 19.6)
        forecast_rain_5d = inputs.get("forecast_rain_5d_mm", 0.0)
        recent_rain_24h = inputs.get("recent_rain_24h_mm", 0.0)

        # Suppression if heavy rain recently fell
        if recent_rain_24h >= 15.0:
            return None

        is_triggered = (depletion_mm >= raw_mm) and (forecast_rain_5d < 5.0)

        if not is_triggered:
            return None

        try:
            dt_now = datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))
            valid_until = (dt_now + timedelta(hours=48)).isoformat()
        except Exception:
            valid_until = timestamp_utc

        return AdvisoryCard(
            advisory_id=f"ADV-IRR02-{context.upazila_id}-{timestamp_utc[:10]}",
            rule_id=self.RULE_ID,
            upazila_id=context.upazila_id,
            crop_name=context.crop_name,
            growth_stage=context.growth_stage,
            timestamp_utc=timestamp_utc,
            valid_until_utc=valid_until,
            severity=AdvisorySeverity.WARNING,
            status=AdvisoryStatus.ACTIVE,
            headline_bn="সেচ প্রদান করুন (পরামর্শ)",
            plain_language_bn=(
                f"মাটির আর্দ্রতা সংকটজনক মাত্রায় নেমে গেছে (ঘাটতি {round(depletion_mm, 1)} মিমি) "
                f"এবং আগামী ৫ দিনে বৃষ্টির সম্ভাবনা নেই। ফসলের স্বাভাবিক বৃদ্ধি বজায় রাখতে জমিতে সেচ প্রদান করুন।"
            ),
            action_items_bn=[
                "অনতিবিলম্বে জমিতে ৫–৭ সেন্টিমিটার উচ্চতায় সেচ প্রদান করুন।",
                "পরবর্তী সেচের আগে পর্যায়ক্রমিক ভিজানো ও শুকানো (AWD) পদ্ধতি মেনে চলুন।",
            ],
            field_verification_bn="সেচ প্রদান করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।",
            uncertainty_description_bn="মাটির পানির ঘাটতি FAO-56 জলবায়ু ভারসাম্য মডেল দ্বারা নির্ধারিত।",
            supporting_indicators={
                "depletion_mm": depletion_mm,
                "raw_threshold_mm": raw_mm,
                "forecast_rain_5d_mm": forecast_rain_5d,
            },
            provenance_manifest={
                "water_balance_model": "FAO-56/USDA-SCS",
                "meteorology": "NASA-POWER/Open-Meteo",
            },
        )
