"""RULE-FLD-01: Haor Basin 48-72h Pre-Flood Emergency Harvest Alert.

Evidence-supported rule issuing early harvest alerts to SAAOs and lead farmers
in the Haor basin prior to transboundary flash-flood inundation (FR-ADV-02, FR-ADV-03).
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


class RuleHaorEmergencyHarvest(BaseAgriculturalRule):
    """Evaluates transboundary flood indicators to trigger emergency early harvest."""

    RULE_ID = "RULE-FLD-01"
    RULE_NAME = "Haor Basin 48-72h Pre-Flood Emergency Harvest Alert"
    CLASSIFICATION = "Evidence-Supported"

    # Haor Upazila IDs permitted for flood advisory
    HAOR_UPAZILAS = ["BD-60-90-86", "BD-60-90-89"]  # Sunamganj Sadar, Tahirpur

    # Stages where rice can be safely harvested
    HARVESTABLE_STAGES = ["DOUGH", "MATURITY", "RIPENING", "GRAIN_FILLING", "HARVEST"]

    def evaluate(
        self,
        context: ContextGatePayload,
        inputs: Dict[str, Any],
        timestamp_utc: str,
    ) -> Optional[AdvisoryCard]:
        """Evaluate trigger conditions for RULE-FLD-01.

        Triggers:
        1. Composite Iflood >= 0.75
        2. Transboundary catchment 48h rain P_cat >= 100.0 mm
        3. Surma river level H >= (DL - 0.50 m) AND rate of rise >= 0.50 m/day
        4. Crop maturity >= 80% (grain yellowing) or stage is harvestable
        """
        # Suppression: Outside Haor zone
        if context.upazila_id not in self.HAOR_UPAZILAS:
            return None

        # Suppression: Crop not mature enough for early harvest
        stage_key = context.growth_stage.upper().replace(" ", "_")
        grain_maturity_pct = inputs.get("grain_maturity_pct", 80.0)

        is_mature_enough = (stage_key in self.HARVESTABLE_STAGES) or (grain_maturity_pct >= 80.0)
        if not is_mature_enough:
            return None

        i_flood = inputs.get("i_flood", 0.0)
        p_cat_48h = inputs.get("p_cat_48h_mm", 0.0)
        water_level = inputs.get("water_level_m_pwd", 0.0)
        danger_level = inputs.get("danger_level_m_pwd", 8.25)
        rate_of_rise = inputs.get("rate_of_rise_24h_m", 0.0)

        # Triggers check
        stage_threshold = danger_level - 0.50
        is_triggered = (
            (i_flood >= 0.75)
            and (p_cat_48h >= 100.0)
            and (water_level >= stage_threshold)
            and (rate_of_rise >= 0.50)
        )

        if not is_triggered:
            return None

        try:
            dt_now = datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))
            valid_until = (dt_now + timedelta(hours=36)).isoformat()
        except Exception:
            valid_until = timestamp_utc

        return AdvisoryCard(
            advisory_id=f"ADV-FLD01-{context.upazila_id}-{timestamp_utc[:10]}",
            rule_id=self.RULE_ID,
            upazila_id=context.upazila_id,
            crop_name=context.crop_name,
            growth_stage=context.growth_stage,
            timestamp_utc=timestamp_utc,
            valid_until_utc=valid_until,
            severity=AdvisorySeverity.EMERGENCY,
            status=AdvisoryStatus.ACTIVE,
            headline_bn="জরুরি ধান কর্তন প্রস্তুতি (জরুরি সতর্কবার্তা)",
            plain_language_bn=(
                "উজান থেকে মেঘালয়ের পাহাড়ি ঢল ও নদীর পানি দ্রুত বৃদ্ধি পাওয়ায় আগামী ৪৮–৭২ ঘণ্টার মধ্যে "
                "হাওড়ে আকস্মিক বন্যার উচ্চ ঝুঁকি রয়েছে। যেসকল জমির ধান ৮০% পেকেছে (শীষের শতকরা ৮০ ভাগ ধান সোনালী হয়েছে), "
                "অবিলম্বে দলবদ্ধভাবে বা কম্বাইন হারভেস্টার দিয়ে ধান কেটে নিরাপদ স্থানে নিয়ে যান।"
            ),
            action_items_bn=[
                "যেসব জমির ধান ৮০% পেকেছে, বিলম্ব না করে দ্রুত কর্তন সম্পন্ন করুন।",
                "কেটে আনা ধান তাৎক্ষণিকভাবে উঁচু স্থান বা ড্রায়ারে শুকানোর ব্যবস্থা করুন।",
                "হাওড়ের বাঁধের অবস্থা পর্যবেক্ষণে স্থানীয় ইউনিয়ন পরিষদ ও কৃষি কর্মকর্তার সাথে সার্বক্ষণিক যোগাযোগ রাখুন।",
            ],
            field_verification_bn="যেসব জমির ধান এখনও কাঁচা বা দুধ অবস্থায় রয়েছে, সেগুলো কাটা যাবে না। বাঁধের অবস্থা পর্যবেক্ষণে স্থানীয় ইউনিয়ন পরিষদ ও কৃষি কর্মকর্তার সাথে যোগাযোগ রাখুন।",
            uncertainty_description_bn=(
                f"মেঘালয় অববাহিকার ৪৮ ঘণ্টার বৃষ্টিপাত ({round(p_cat_48h, 1)} মিমি) ও সুরমা নদীর পানি বৃদ্ধি হারের "
                f"({round(rate_of_rise, 2)} মি/দিন) যৌথ সূচকের ভিত্তিতে এই সতর্কতা জারি করা হয়েছে।"
            ),
            supporting_indicators={
                "i_flood": i_flood,
                "p_cat_48h_mm": p_cat_48h,
                "water_level_m_pwd": water_level,
                "danger_level_m_pwd": danger_level,
                "rate_of_rise_24h_m": rate_of_rise,
                "grain_maturity_pct": grain_maturity_pct,
            },
            provenance_manifest={
                "hydrology": "BWDB-FFWC/Surma-Gauge",
                "satellite_precipitation": "GPM-IMERG-V07",
            },
        )
