"""RULE-IRR-01: Pre-Rain Boro Rice Irrigation Postponement Advisory.

Evidence-supported rule advising tubewell operators in the Barind Tract to withhold irrigation
48-72h prior to forecasted rainfall events (FR-ADV-01, FR-ADV-03).
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


class RuleIrrigationPostponement(BaseAgriculturalRule):
    """Evaluates 48-hour rainfall forecast and soil water deficit to advise irrigation postponement."""

    RULE_ID = "RULE-IRR-01"
    RULE_NAME = "Pre-Rain Boro Rice Irrigation Postponement Advisory"
    CLASSIFICATION = "Evidence-Supported"

    # Supported phenological stages for pre-rain postponement
    SUPPORTED_STAGES = ["VEGETATIVE", "TILLERING", "PANICLE_INITIATION", "EARLY_PANICLE_INITIATION"]

    def evaluate(
        self,
        context: ContextGatePayload,
        inputs: Dict[str, Any],
        timestamp_utc: str,
    ) -> Optional[AdvisoryCard]:
        """Evaluate trigger conditions for RULE-IRR-01.

        Triggers:
        1. 48h QPF >= 20.0 mm
        2. Rain probability >= 65%
        3. Soil depletion Dt < (TAW - 25.0 mm)
        4. Model ensemble spread <= 35%
        5. Growth stage is Vegetative/Tillering or Panicle Initiation
        """
        stage_key = context.growth_stage.upper().replace(" ", "_")
        if stage_key not in self.SUPPORTED_STAGES:
            return None

        qpf_48h = inputs.get("qpf_48h_mm", 0.0)
        rain_prob = inputs.get("rain_prob_pct", 0.0)
        depletion_mm = inputs.get("depletion_mm", 0.0)
        taw_mm = inputs.get("taw_mm", 56.0)
        ensemble_spread = inputs.get("ensemble_spread_pct", 20.0)

        # Trigger logic
        storage_threshold = taw_mm - 25.0
        is_triggered = (
            qpf_48h >= 20.0
            and rain_prob >= 65.0
            and depletion_mm < storage_threshold
            and ensemble_spread <= 35.0
        )

        if not is_triggered:
            return None

        # Expiration is 48 hours after generation
        try:
            dt_now = datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))
            valid_until = (dt_now + timedelta(hours=48)).isoformat()
        except Exception:
            valid_until = timestamp_utc

        return AdvisoryCard(
            advisory_id=f"ADV-IRR01-{context.upazila_id}-{timestamp_utc[:10]}",
            rule_id=self.RULE_ID,
            upazila_id=context.upazila_id,
            crop_name=context.crop_name,
            growth_stage=context.growth_stage,
            timestamp_utc=timestamp_utc,
            valid_until_utc=valid_until,
            severity=AdvisorySeverity.ADVISORY,
            status=AdvisoryStatus.ACTIVE,
            headline_bn="সেচ স্থগিত রাখুন (পরামর্শ)",
            plain_language_bn=(
                f"আগামী ৪৮ থেকে ৭২ ঘণ্টার মধ্যে আপনার এলাকায় উল্লেখযোগ্য বৃষ্টির সম্ভাবনা রয়েছে "
                f"(সম্ভাবনা {int(rain_prob)}%, আনুমানিক {int(qpf_48h)} মিমি)। নলকূপ চালু করার আগে অপেক্ষা করুন। "
                f"বৃষ্টি হলে সেচের জ্বালানি খরচ সাশ্রয় হবে।"
            ),
            action_items_bn=[
                "পরবর্তী ৪৮ ঘণ্টা গভীর বা অগভীর নলকূপ চালু করা স্থগিত রাখুন।",
                "জমির আইল ভালোভাবে মেরামত করুন যাতে বৃষ্টির পানি জমিতে ধরে রাখা যায়।",
                "যদি বৃষ্টি ২০ মিলিমিটারের কম হয়, তবে মাটির আর্দ্রতা পরীক্ষা করে সেচ দিন।",
            ],
            field_verification_bn="সেচ বন্ধ রাখার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন। যদি জমি ইতিমধ্যে ফেটে গিয়ে থাকে, তবে হালকা পানি দিন।",
            uncertainty_description_bn=(
                f"আবহাওয়া মডেলের পূর্বাভাসের বিস্তার {int(ensemble_spread)}%। "
                "পূর্বাভাসে স্বাভাবিক অনিশ্চয়তা বিদ্যমান থাকায় সরাসরি মাঠ পর্যবেক্ষণ বাঞ্ছনীয়।"
            ),
            supporting_indicators={
                "qpf_48h_mm": qpf_48h,
                "rain_prob_pct": rain_prob,
                "soil_depletion_mm": depletion_mm,
                "taw_mm": taw_mm,
                "ensemble_spread_pct": ensemble_spread,
            },
            provenance_manifest={
                "forecast_model": inputs.get("forecast_model", "ECMWF-IFS/Open-Meteo"),
                "agroclimatology": "NASA-POWER/FAO-56",
            },
        )
