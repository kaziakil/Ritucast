"""Haor Transboundary Flash Flood Hazard Index Calculator (IDX-FLD-01).

Couples Meghalaya transboundary catchment rainfall with BWDB Surma river stage freeboard
and rate of water level rise to estimate flash-flood inundation risk.
"""

from typing import Dict, Optional, Literal
from analytics.contracts.indicator_schemas import HaorFloodIndexResult


class HaorFloodIndexCalculator:
    """Calculates the composite Haor Flash Flood Hazard Index (Iflood)."""

    WEIGHT_RAIN = 0.35
    WEIGHT_STAGE = 0.30
    WEIGHT_RISE = 0.20
    WEIGHT_INUND = 0.15

    # BWDB Surma River at Sunamganj gauge danger level (m PWD datum)
    DEFAULT_DANGER_LEVEL_M = 8.25

    @classmethod
    def calculate_sub_indices(
        cls,
        p_cat_48h_mm: float,
        water_level_m: float,
        danger_level_m: float,
        rate_of_rise_24h_m: float,
        inundation_fraction: float = 0.0,
    ) -> Dict[str, float]:
        """Compute individual normalized sub-indices [0.0, 1.0]."""
        # 1. Transboundary catchment precipitation f_P
        f_p = min(1.0, max(0.0, (p_cat_48h_mm - 30.0) / 120.0))

        # 2. River stage proximity to danger level f_S
        f_s = min(1.0, max(0.0, (water_level_m - (danger_level_m - 1.0)) / 1.20))

        # 3. River stage rate of rise f_R (m/day)
        f_r = min(1.0, max(0.0, (rate_of_rise_24h_m - 0.20) / 0.80))

        # 4. Satellite observed surface water fraction f_I
        f_i = min(1.0, max(0.0, inundation_fraction / 0.40))

        return {
            "f_P": round(f_p, 3),
            "f_S": round(f_s, 3),
            "f_R": round(f_r, 3),
            "f_I": round(f_i, 3),
        }

    @classmethod
    def calculate_index(
        cls,
        catchment_id: str,
        date_str: str,
        p_cat_48h_mm: float,
        water_level_m: float,
        danger_level_m: Optional[float] = None,
        rate_of_rise_24h_m: float = 0.0,
        inundation_fraction: float = 0.0,
    ) -> HaorFloodIndexResult:
        """Compute composite Iflood and determine hazard tier."""
        dl = danger_level_m if danger_level_m is not None else cls.DEFAULT_DANGER_LEVEL_M
        subs = cls.calculate_sub_indices(
            p_cat_48h_mm=p_cat_48h_mm,
            water_level_m=water_level_m,
            danger_level_m=dl,
            rate_of_rise_24h_m=rate_of_rise_24h_m,
            inundation_fraction=inundation_fraction,
        )

        i_flood = (
            cls.WEIGHT_RAIN * subs["f_P"]
            + cls.WEIGHT_STAGE * subs["f_S"]
            + cls.WEIGHT_RISE * subs["f_R"]
            + cls.WEIGHT_INUND * subs["f_I"]
        )
        i_flood = round(min(1.0, max(0.0, i_flood)), 3)

        if i_flood < 0.35:
            tier: Literal["NORMAL", "ADVISORY", "WARNING", "EMERGENCY"] = "NORMAL"
        elif i_flood < 0.55:
            tier = "ADVISORY"
        elif i_flood < 0.75:
            tier = "WARNING"
        else:
            tier = "EMERGENCY"

        return HaorFloodIndexResult(
            catchment_id=catchment_id,
            date=date_str,
            i_flood=i_flood,
            hazard_tier=tier,
            p_cat_48h_mm=round(p_cat_48h_mm, 1),
            water_level_m_pwd=round(water_level_m, 2),
            rate_of_rise_24h_m=round(rate_of_rise_24h_m, 2),
            inundation_fraction=round(inundation_fraction, 3),
            sub_indices=subs,
        )
