"""Cardinal Thermal Stress Index Calculator (Heat & Cold Injury Indicators).

Evaluates high-temperature anthesis sterility risks and low-temperature booting microspore sterility
for Boro rice in Bangladesh.
"""

from typing import Optional, Literal
from analytics.contracts.indicator_schemas import ThermalStressResult


class ThermalStressCalculator:
    """Calculates cardinal heat and cold stress indices and mitigation advice."""

    HEAT_THRESHOLD_C = 35.0
    COLD_THRESHOLD_C = 15.0

    @classmethod
    def calculate_heat_stress(
        cls,
        upazila_id: str,
        date_str: str,
        t_max_c: float,
        consecutive_days: int = 1,
    ) -> ThermalStressResult:
        """Calculate Anthesis heat stress index (Iheat).

        Iheat = 0 if Tmax < 35.0; (Tmax - 35) / 5.0 if 35 <= Tmax <= 40; 1.0 if Tmax > 40.
        Critical if consecutive_days >= 2.
        """
        if t_max_c < cls.HEAT_THRESHOLD_C:
            index = 0.0
        elif t_max_c <= 40.0:
            index = (t_max_c - cls.HEAT_THRESHOLD_C) / 5.0
        else:
            index = 1.0

        is_critical = (index > 0.0) and (consecutive_days >= 2)
        mitigation_depth = 4.0 if is_critical else 0.0  # 3-5 cm cooling buffer

        return ThermalStressResult(
            upazila_id=upazila_id,
            date=date_str,
            stress_type="HEAT" if index > 0.0 else "NONE",
            intensity_index=round(index, 3),
            consecutive_days=consecutive_days,
            is_critical=is_critical,
            mitigation_water_depth_cm=mitigation_depth,
        )

    @classmethod
    def calculate_cold_stress(
        cls,
        upazila_id: str,
        date_str: str,
        t_min_c: float,
        consecutive_days: int = 1,
    ) -> ThermalStressResult:
        """Calculate Booting stage cold shock index (Icold).

        Icold = 0 if Tmin >= 15.0; (15.0 - Tmin) / 5.0 if 10.0 <= Tmin < 15.0; 1.0 if Tmin < 10.0.
        Critical if consecutive_days >= 3.
        """
        if t_min_c >= cls.COLD_THRESHOLD_C:
            index = 0.0
        elif t_min_c >= 10.0:
            index = (cls.COLD_THRESHOLD_C - t_min_c) / 5.0
        else:
            index = 1.0

        is_critical = (index > 0.0) and (consecutive_days >= 3)
        mitigation_depth = 6.0 if is_critical else 0.0  # 5-7 cm thermal blanket

        return ThermalStressResult(
            upazila_id=upazila_id,
            date=date_str,
            stress_type="COLD" if index > 0.0 else "NONE",
            intensity_index=round(index, 3),
            consecutive_days=consecutive_days,
            is_critical=is_critical,
            mitigation_water_depth_cm=mitigation_depth,
        )
