"""FAO-56 Penman-Monteith Reference Evapotranspiration Calculator (EQN-ET0-01).

Implements the internationally standardized FAO-56 Penman-Monteith equation (Allen et al., 1998)
for daily reference evapotranspiration (ET0) over a hypothetical grass reference crop.
"""

import math
from typing import Optional
from analytics.contracts.indicator_schemas import ReferenceET0Result


class PenmanMonteithCalculator:
    """Standardized FAO-56 Penman-Monteith physical calculation."""

    # Stefan-Boltzmann constant in MJ / K^4 / m^2 / day
    STEFAN_BOLTZMANN = 4.903e-9
    # Solar constant in MJ / m^2 / min
    SOLAR_CONSTANT = 0.0820

    @classmethod
    def calculate_et0(
        cls,
        upazila_id: str,
        date_str: str,
        t_max_c: float,
        t_min_c: float,
        rh_mean_pct: float,
        wind_speed_2m_ms: float,
        solar_rad_mj_m2: float,
        elevation_m: float = 20.0,
        latitude_deg: float = 24.5,
    ) -> ReferenceET0Result:
        """Compute daily ET0 in mm/day from daily meteorological inputs.

        Args:
            upazila_id: Upazila identifier.
            date_str: Date string (YYYY-MM-DD).
            t_max_c: Maximum air temperature (°C).
            t_min_c: Minimum air temperature (°C).
            rh_mean_pct: Mean relative humidity (0–100%).
            wind_speed_2m_ms: Wind speed at 2 m height (m/s).
            solar_rad_mj_m2: Measured/modeled solar radiation (MJ/m²/day).
            elevation_m: Elevation above sea level (m). Defaults to 20m (Barind).
            latitude_deg: Decimal latitude (degrees N). Defaults to 24.5°N.

        Returns:
            ReferenceET0Result instance.
        """
        # 1. Mean temperature
        t_mean_c = (t_max_c + t_min_c) / 2.0

        # 2. Atmospheric pressure (kPa) and Psychrometric constant (kPa/°C)
        p_atm = 101.3 * math.pow((293.0 - 0.0065 * elevation_m) / 293.0, 5.26)
        gamma = 0.000665 * p_atm

        # 3. Saturation vapor pressure es (kPa)
        e_tmax = 0.6108 * math.exp((17.27 * t_max_c) / (t_max_c + 237.3))
        e_tmin = 0.6108 * math.exp((17.27 * t_min_c) / (t_min_c + 237.3))
        e_s = (e_tmax + e_tmin) / 2.0

        # 4. Actual vapor pressure ea (kPa)
        rh_clipped = max(5.0, min(100.0, rh_mean_pct))
        e_a = e_s * (rh_clipped / 100.0)
        vpd = max(0.0, e_s - e_a)

        # 5. Slope of vapor pressure curve Delta (kPa/°C)
        delta = (4098.0 * (0.6108 * math.exp((17.27 * t_mean_c) / (t_mean_c + 237.3)))) / math.pow(
            t_mean_c + 237.3, 2
        )

        # 6. Extraterrestrial radiation Ra (MJ/m²/day) & Clear-sky radiation Rso
        # Parse day of year
        try:
            from datetime import datetime
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            doy = dt.timetuple().tm_yday
        except Exception:
            doy = 75  # Mid-March fallback

        phi = math.radians(latitude_deg)
        dr = 1.0 + 0.033 * math.cos((2.0 * math.pi * doy) / 365.0)
        delta_sol = 0.409 * math.sin(((2.0 * math.pi * doy) / 365.0) - 1.39)
        omega_arg = -math.tan(phi) * math.tan(delta_sol)
        omega_arg = max(-1.0, min(1.0, omega_arg))
        omega_s = math.acos(omega_arg)

        ra = ((24.0 * 60.0) / math.pi) * cls.SOLAR_CONSTANT * dr * (
            omega_s * math.sin(phi) * math.sin(delta_sol)
            + math.cos(phi) * math.cos(delta_sol) * math.sin(omega_s)
        )
        r_so = (0.75 + 2e-5 * elevation_m) * ra

        # 7. Net Radiation Rn (MJ/m²/day)
        # Net solar shortwave radiation (albedo = 0.23 for reference grass)
        r_ns = (1.0 - 0.23) * solar_rad_mj_m2

        # Net longwave radiation Rnl
        t_max_k4 = math.pow(t_max_c + 273.16, 4)
        t_min_k4 = math.pow(t_min_c + 273.16, 4)
        rel_solar = min(1.0, max(0.3, solar_rad_mj_m2 / max(0.1, r_so)))
        r_nl = (
            cls.STEFAN_BOLTZMANN
            * ((t_max_k4 + t_min_k4) / 2.0)
            * (0.34 - 0.14 * math.sqrt(max(0.01, e_a)))
            * (1.35 * rel_solar - 0.35)
        )
        r_n = r_ns - r_nl
        # Soil heat flux G = 0 for daily time steps
        g = 0.0

        # 8. Penman-Monteith Combination Equation
        u2 = max(0.2, min(25.0, wind_speed_2m_ms))
        numerator = 0.408 * delta * (r_n - g) + gamma * (900.0 / (t_mean_c + 273.0)) * u2 * vpd
        denominator = delta + gamma * (1.0 + 0.34 * u2)

        et0 = max(0.1, numerator / denominator)

        return ReferenceET0Result(
            upazila_id=upazila_id,
            date=date_str,
            et0_mm_day=round(et0, 2),
            elevation_m=elevation_m,
            net_radiation_mj_m2=round(r_n, 2),
            vapor_pressure_deficit_kpa=round(vpd, 3),
            method="FAO-56 Penman-Monteith",
            quality_flag="VALID",
        )
