"""Root-Zone Daily Soil Water Balance and Deficit Calculator (EQN-SWD-01).

Implements FAO-56 mass-balance water depletion model for Barind heavy clay soils
and AWD irrigation scheduling for Boro rice.
"""

from typing import Optional
from analytics.contracts.indicator_schemas import SoilWaterDeficitResult


class SoilWaterDeficitCalculator:
    """Calculates daily root-zone soil water depletion Dt and stress levels."""

    # High Barind Tract soil hydraulic parameters (heavy silty clay / paleosols)
    THETA_FC = 0.32   # Volumetric water content at Field Capacity (m3/m3)
    THETA_PWP = 0.18  # Volumetric water content at Permanent Wilting Point (m3/m3)
    ROOT_DEPTH_M = 0.40  # Effective Boro rice root zone depth (m)

    @classmethod
    def calculate_taw(cls, root_depth_m: Optional[float] = None) -> float:
        """Total Available Water TAW (mm) = 1000 * (FC - PWP) * Zr."""
        zr = root_depth_m if root_depth_m is not None else cls.ROOT_DEPTH_M
        return round(1000.0 * (cls.THETA_FC - cls.THETA_PWP) * zr, 2)

    @classmethod
    def calculate_raw(cls, taw: float, growth_stage: str) -> float:
        """Readily Available Water RAW (mm) = p * TAW based on phenology."""
        stage_key = growth_stage.upper().replace(" ", "_")
        # In reproductive/flowering stages, Boro rice has near-zero depletion tolerance
        if stage_key in ["ANTHESIS", "FLOWERING", "BOOTING", "PANICLE_INITIATION"]:
            p = 0.10
        elif stage_key in ["MATURITY", "RIPENING", "HARVEST"]:
            p = 0.40
        else:
            # Vegetative tillering under AWD allows depletion up to 15cm below soil surface
            p = 0.35
        return round(p * taw, 2)

    @classmethod
    def calculate_effective_precipitation(cls, precip_mm: float) -> float:
        """USDA SCS effective rainfall calculation (Allen et al., 1998)."""
        if precip_mm <= 3.0:
            return 0.0
        elif precip_mm <= 250.0:
            p_eff = (precip_mm * (125.0 - 0.2 * precip_mm)) / 125.0
            return max(0.0, round(p_eff, 2))
        else:
            p_eff = 125.0 + 0.1 * precip_mm
            return round(p_eff, 2)

    @classmethod
    def step_daily_water_balance(
        cls,
        upazila_id: str,
        date_str: str,
        d_prev_mm: float,
        etc_mm: float,
        precip_mm: float,
        irrigation_mm: float = 0.0,
        growth_stage: str = "Tillering",
        crop_name: str = "Boro Rice",
    ) -> SoilWaterDeficitResult:
        """Execute one daily step of the root-zone soil water balance.

        Dt = D_{t-1} + ETc - P_eff - I + DP

        Args:
            upazila_id: Upazila identifier.
            date_str: Date string (YYYY-MM-DD).
            d_prev_mm: Previous day's root-zone water depletion D_{t-1} (mm).
            etc_mm: Daily crop evapotranspiration (mm/day).
            precip_mm: Total daily precipitation (mm).
            irrigation_mm: Irrigation applied (mm).
            growth_stage: Phenological growth stage.
            crop_name: Crop name.

        Returns:
            SoilWaterDeficitResult model.
        """
        taw = cls.calculate_taw()
        raw = cls.calculate_raw(taw, growth_stage)
        p_eff = cls.calculate_effective_precipitation(precip_mm)

        # Depletion increment: ETc increases depletion, rain and irrigation decrease depletion
        net_depletion = d_prev_mm + etc_mm - p_eff - irrigation_mm

        # Physical constraints: Depletion cannot be negative (surplus drains as percolation DP)
        # Depletion cannot exceed TAW (soil cannot dry beyond permanent wilting point)
        d_t = max(0.0, min(taw, net_depletion))

        is_critical = d_t >= raw
        remaining_storage = max(0.0, taw - d_t)

        return SoilWaterDeficitResult(
            upazila_id=upazila_id,
            date=date_str,
            crop_name=crop_name,
            growth_stage=growth_stage,
            depletion_mm=round(d_t, 2),
            taw_mm=round(taw, 2),
            raw_mm=round(raw, 2),
            effective_rain_mm=round(p_eff, 2),
            irrigation_applied_mm=round(irrigation_mm, 2),
            is_stress_critical=is_critical,
            storage_capacity_remaining_mm=round(remaining_storage, 2),
        )
