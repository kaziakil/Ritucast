"""
Structural Schema Validation using Pydantic v2.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field, model_validator, ConfigDict
from pipelines.common.exceptions import SchemaValidationError

class MeteorologyDailySchema(BaseModel):
    upazila_id: str = Field(..., min_length=5, max_length=20)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    t2m_c: Optional[float] = None
    t2m_max_c: Optional[float] = None
    t2m_min_c: Optional[float] = None
    solar_rad_mj_m2: Optional[float] = None
    rh2m_pct: Optional[float] = None
    wind_speed_2m_ms: Optional[float] = None
    precipitation_mm: Optional[float] = None
    source_id: str = Field(default="DATA-MET-01")

    @model_validator(mode="after")
    def validate_tmax_greater_equal_tmin(self) -> "MeteorologyDailySchema":
        if self.t2m_max_c is not None and self.t2m_min_c is not None:
            if self.t2m_max_c < self.t2m_min_c:
                raise ValueError(f"t2m_max_c ({self.t2m_max_c}) cannot be less than t2m_min_c ({self.t2m_min_c})")
        return self

class ForecastHourlySchema(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str
    valid_time_utc: str
    horizon_hours: int = Field(..., ge=0, le=168)
    temp_2m_c: Optional[float] = None
    rh_2m_pct: Optional[float] = None
    rain_prob_pct: Optional[float] = None
    rain_amount_mm: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    model_name: str
    source_id: str = Field(default="DATA-FCST-01")

class CatchmentRainfallSchema(BaseModel):
    catchment_id: str
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    precipitation_mm: float = Field(..., ge=0.0)
    random_error_mm: Optional[float] = None
    quality_flag: int = 0
    source_id: str = Field(default="DATA-PCP-01")

class Sentinel1MetadataSchema(BaseModel):
    product_id: str
    sensing_time_utc: str
    polarization: str
    water_extent_pct: float = Field(..., ge=0.0, le=100.0)
    mean_backscatter_vv_db: float
    coverage_upazilas: List[str]
    source_id: str = Field(default="DATA-SAR-01")

class SoilMoistureDailySchema(BaseModel):
    upazila_id: str
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    soil_moisture_am: Optional[float] = None
    soil_moisture_pm: Optional[float] = None
    soil_moisture_mean_m3_m3: Optional[float] = None
    quality_flag: int = 0
    source_id: str = Field(default="DATA-SMC-01")

class HydrologyReadingSchema(BaseModel):
    station_id: str
    timestamp_utc: str
    water_level_m_pwd: float
    danger_level_m_pwd: float
    freeboard_m: float
    rate_of_rise_24h_m: float
    is_above_danger: bool
    source_id: str = Field(default="DATA-HYD-01")

def validate_record(schema_cls, record: Dict[str, Any]) -> BaseModel:
    """Validates a single record against schema; raises SchemaValidationError on mismatch."""
    try:
        return schema_cls.model_validate(record)
    except Exception as err:
        raise SchemaValidationError(f"Schema violation in {schema_cls.__name__}: {err}") from err
