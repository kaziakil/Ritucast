"""
Semantic Data Validation & Physical Boundary Checks.
"""

from typing import Dict, Any, List, Optional, Tuple
from pipelines.common.exceptions import SemanticValidationError

# Approved physical boundaries from Phase 4 Table 2
PHYSICAL_BOUNDS = {
    "temperature_c": (-5.0, 55.0),
    "precipitation_mm": (0.0, 600.0),
    "solar_rad_mj_m2": (0.0, 35.0),
    "rh_pct": (0.0, 100.0),
    "wind_speed_ms": (0.0, 45.0),
    "soil_moisture_m3_m3": (0.02, 0.60),
    "water_level_m_pwd": (0.0, 25.0),
    "backscatter_db": (-40.0, 10.0),
}

FILL_VALUES = {-999.0, -9999.0, -99.0, 9999.0, -1.0e30}

class SemanticValidator:
    """Enforces physical sanity checks and fill-value auditing."""

    @staticmethod
    def check_bound(val: Optional[float], bound_key: str, param_name: str) -> Optional[str]:
        """Returns error message if val violates physical bounds; None if valid."""
        if val is None or val in FILL_VALUES:
            return None
        min_val, max_val = PHYSICAL_BOUNDS[bound_key]
        if not (min_val <= val <= max_val):
            return f"{param_name} ({val}) out of physical bounds [{min_val}, {max_val}]"
        return None

    @classmethod
    def validate_meteorology(cls, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Audits daily agrometeorology record."""
        errors = []
        for t_field in ["t2m_c", "t2m_max_c", "t2m_min_c"]:
            err = cls.check_bound(record.get(t_field), "temperature_c", t_field)
            if err:
                errors.append(err)

        err_p = cls.check_bound(record.get("precipitation_mm"), "precipitation_mm", "precipitation_mm")
        if err_p:
            errors.append(err_p)

        err_rad = cls.check_bound(record.get("solar_rad_mj_m2"), "solar_rad_mj_m2", "solar_rad_mj_m2")
        if err_rad:
            errors.append(err_rad)

        err_rh = cls.check_bound(record.get("rh2m_pct"), "rh_pct", "rh2m_pct")
        if err_rh:
            errors.append(err_rh)

        err_ws = cls.check_bound(record.get("wind_speed_2m_ms"), "wind_speed_ms", "wind_speed_2m_ms")
        if err_ws:
            errors.append(err_ws)

        return (len(errors) == 0, errors)

    @classmethod
    def validate_forecast(cls, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Audits forecast record."""
        errors = []
        err_t = cls.check_bound(record.get("temp_2m_c"), "temperature_c", "temp_2m_c")
        if err_t:
            errors.append(err_t)

        err_p = cls.check_bound(record.get("rain_amount_mm"), "precipitation_mm", "rain_amount_mm")
        if err_p:
            errors.append(err_p)

        prob = record.get("rain_prob_pct")
        if prob is not None and not (0.0 <= prob <= 100.0):
            errors.append(f"rain_prob_pct ({prob}) out of bounds [0.0, 100.0]")

        return (len(errors) == 0, errors)

    @classmethod
    def validate_catchment_rain(cls, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Audits transboundary catchment rain."""
        errors = []
        err = cls.check_bound(record.get("precipitation_mm"), "precipitation_mm", "precipitation_mm")
        if err:
            errors.append(err)
        return (len(errors) == 0, errors)

    @classmethod
    def validate_soil_moisture(cls, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Audits volumetric soil moisture."""
        errors = []
        sm = record.get("soil_moisture_mean_m3_m3")
        err = cls.check_bound(sm, "soil_moisture_m3_m3", "soil_moisture_mean_m3_m3")
        if err:
            errors.append(err)
        return (len(errors) == 0, errors)

    @classmethod
    def validate_hydrology(cls, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Audits river water level."""
        errors = []
        wl = record.get("water_level_m_pwd")
        err = cls.check_bound(wl, "water_level_m_pwd", "water_level_m_pwd")
        if err:
            errors.append(err)
        return (len(errors) == 0, errors)
