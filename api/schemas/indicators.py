"""Response schemas for environmental observations, indicators, and flood hazards."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class WeatherDailyObservation(BaseModel):
    """Daily meteorological observation (Tier 1)."""
    date: str = Field(..., description="Date (YYYY-MM-DD)")
    temp_max_c: float = Field(..., description="Maximum 2m air temperature (°C)")
    temp_min_c: float = Field(..., description="Minimum 2m air temperature (°C)")
    solar_radiation_mj_m2: float = Field(..., description="Daily solar radiation (MJ/m2/day)")
    precip_24h_mm: float = Field(..., description="24-hour precipitation total (mm)")
    rh_mean_pct: float = Field(..., description="Mean relative humidity (%)")
    wind_speed_ms: Optional[float] = Field(default=None, description="Wind speed at 2m (m/s)")


class WeatherDailyForecast(BaseModel):
    """Daily numerical weather prediction (Tier 3)."""
    date: str = Field(..., description="Forecast valid date (YYYY-MM-DD)")
    lead_time_h: int = Field(..., description="Forecast lead time in hours")
    temp_max_c: float = Field(..., description="Projected maximum temperature (°C)")
    temp_min_c: float = Field(..., description="Projected minimum temperature (°C)")
    qpf_precip_mm: float = Field(..., description="Quantitative precipitation forecast (mm)")
    precip_probability_pct: int = Field(..., description="Precipitation probability (0-100%)")
    confidence: str = Field(default="MODERATE", description="Confidence classification")


class WeatherFeedResponse(BaseModel):
    """Combined Tier 1 observations and Tier 3 forecast feed."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Upazila code")
    name_bn: str = Field(..., description="Upazila name in Bengali")
    timezone: str = Field(default="Asia/Dhaka", description="Local timezone")
    tier_1_observations: Dict[str, Any] = Field(..., description="Empirical sensor observations")
    tier_3_forecasts: Dict[str, Any] = Field(..., description="Probabilistic weather forecasts")


class SoilPropertiesSchema(BaseModel):
    """Soil physical properties."""
    texture: str = Field(..., description="Soil texture class")
    root_zone_depth_m: float = Field(..., description="Effective root zone depth in meters")
    total_available_water_taw_mm: float = Field(..., description="TAW in mm")
    readily_available_water_raw_mm: float = Field(..., description="RAW in mm")


class WaterBalanceIndicators(BaseModel):
    """Tier 2 water balance indicators."""
    calculation_date: str = Field(..., description="Calculation date (YYYY-MM-DD)")
    fao56_et0_mm_day: float = Field(..., description="FAO-56 reference evapotranspiration (mm/day)")
    calibrated_kc: float = Field(..., description="Active crop coefficient Kc")
    crop_etc_mm_day: float = Field(..., description="Crop water demand ETc (mm/day)")
    soil_properties: SoilPropertiesSchema = Field(..., description="Soil parameters")
    current_soil_water_deficit_dt_mm: float = Field(..., description="Root-zone water depletion Dt in mm")
    status: str = Field(..., description="Agronomic status code")
    status_bn: str = Field(..., description="Agronomic status in Bengali")


class WaterBalanceResponse(BaseModel):
    """Root-zone water balance response."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Upazila code")
    crop_id: str = Field(..., description="Crop code")
    growth_stage: str = Field(..., description="Phenological growth stage")
    tier_2_indicators: WaterBalanceIndicators = Field(..., description="Derived water balance indicators")
    provenance: Dict[str, Any] = Field(default_factory=dict, description="Algorithm and dataset provenance")


class FloodHazardIndicators(BaseModel):
    """Tier 2 Haor flash flood hazard indicators."""
    evaluation_timestamp_bst: str = Field(..., description="Evaluation timestamp in BST")
    flood_hazard_index_iflood: float = Field(..., description="Normalized flood index (0.0 to 1.0)")
    hazard_tier: str = Field(..., description="Hazard level (NORMAL, ADVISORY, WARNING, EMERGENCY)")
    hazard_tier_bn: str = Field(..., description="Hazard level in Bengali")
    sub_indices: Dict[str, float] = Field(..., description="Sub-index breakdown")
    trigger_early_harvest: bool = Field(..., description="Whether emergency harvest criteria are met")


class FloodHazardResponse(BaseModel):
    """Haor flash flood hazard response."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Upazila code")
    name_bn: str = Field(..., description="Upazila name in Bengali")
    tier_2_indicators: FloodHazardIndicators = Field(..., description="Derived hydrological hazard indicators")
    provenance: Dict[str, Any] = Field(default_factory=dict, description="Gauge and satellite provenance")
