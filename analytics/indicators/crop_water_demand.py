"""Crop Water Demand Calculator (ETc = Kc * ET0).

Implements FAO-56 stage-specific crop evapotranspiration with dynamic Kc interpolation
calibrated for BRRI Boro rice varieties in Bangladesh.
"""

from typing import Dict, Optional
from analytics.contracts.indicator_schemas import CropWaterDemandResult


class CropWaterDemandCalculator:
    """Calculates daily crop water demand ETc from reference ET0 and phenology."""

    # Stage-based nominal Kc lookup table for BRRI Boro rice varieties
    BORO_STAGE_KC = {
        "TRANSPLANTING": 1.10,
        "TILLERING": 1.15,
        "VEGETATIVE": 1.15,
        "PANICLE_INITIATION": 1.25,
        "BOOTING": 1.28,
        "ANTHESIS": 1.30,
        "FLOWERING": 1.30,
        "MILK_DOUGH": 1.10,
        "GRAIN_FILLING": 1.10,
        "MATURITY": 0.75,
        "HARVEST": 0.65,
    }

    # Timeline knots for continuous linear interpolation (Day after transplanting -> Kc)
    BORO_KNOTS = [
        (1, 1.10),
        (40, 1.15),
        (75, 1.30),
        (100, 1.30),
        (145, 0.65),
    ]

    @classmethod
    def interpolate_kc(cls, days_after_transplant: int) -> float:
        """Linearly interpolate continuous Kc along the Boro rice development curve."""
        if days_after_transplant <= cls.BORO_KNOTS[0][0]:
            return cls.BORO_KNOTS[0][1]
        if days_after_transplant >= cls.BORO_KNOTS[-1][0]:
            return cls.BORO_KNOTS[-1][1]

        for i in range(len(cls.BORO_KNOTS) - 1):
            t_prev, kc_prev = cls.BORO_KNOTS[i]
            t_next, kc_next = cls.BORO_KNOTS[i + 1]
            if t_prev <= days_after_transplant <= t_next:
                fraction = (days_after_transplant - t_prev) / (t_next - t_prev)
                return round(kc_prev + fraction * (kc_next - kc_prev), 3)

        return 1.15

    @classmethod
    def get_kc_for_stage(cls, growth_stage: str, days_after_transplant: Optional[int] = None) -> float:
        """Resolve crop coefficient Kc from stage string or day number."""
        if days_after_transplant is not None:
            return cls.interpolate_kc(days_after_transplant)

        stage_key = growth_stage.upper().replace(" ", "_")
        return cls.BORO_STAGE_KC.get(stage_key, 1.15)

    @classmethod
    def calculate_etc(
        cls,
        upazila_id: str,
        date_str: str,
        et0_mm_day: float,
        crop_name: str = "Boro Rice",
        growth_stage: str = "Tillering",
        days_after_transplant: Optional[int] = None,
    ) -> CropWaterDemandResult:
        """Calculate ETc = Kc * ET0."""
        kc = cls.get_kc_for_stage(growth_stage, days_after_transplant)
        etc = max(0.0, et0_mm_day * kc)

        return CropWaterDemandResult(
            upazila_id=upazila_id,
            date=date_str,
            crop_name=crop_name,
            growth_stage=growth_stage,
            kc_current=round(kc, 3),
            et0_mm_day=round(et0_mm_day, 2),
            etc_mm_day=round(etc, 2),
        )
