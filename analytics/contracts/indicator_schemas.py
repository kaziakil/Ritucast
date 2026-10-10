"""Pydantic v2 schemas for agricultural indicators and descriptive analytics."""

from typing import Dict, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class DescriptiveAgroclimaticSummary(BaseModel):
    """Aggregated agroclimatic statistics over a specified temporal window."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Target Upazila identifier")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    days_count: int = Field(..., ge=1, description="Number of days in analysis window")
    mean_t2m_c: float = Field(..., description="Mean 2m air temperature in Celsius")
    max_t2m_c: float = Field(..., description="Maximum 2m air temperature in Celsius")
    min_t2m_c: float = Field(..., description="Minimum 2m air temperature in Celsius")
    cumulative_precipitation_mm: float = Field(..., ge=0.0, description="Total precipitation in mm")
    mean_solar_rad_mj_m2: float = Field(..., ge=0.0, description="Mean daily solar radiation in MJ/m2/day")
    mean_rh2m_pct: float = Field(..., ge=0.0, le=100.0, description="Mean relative humidity in %")
    completeness_pct: float = Field(..., ge=0.0, le=100.0, description="Observation completeness percentage")


class ReferenceET0Result(BaseModel):
    """FAO-56 Penman-Monteith reference evapotranspiration result."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Target Upazila identifier")
    date: str = Field(..., description="Observation date (YYYY-MM-DD)")
    et0_mm_day: float = Field(..., ge=0.0, le=25.0, description="Reference evapotranspiration in mm/day")
    elevation_m: float = Field(..., description="Elevation above sea level in meters")
    net_radiation_mj_m2: float = Field(..., description="Calculated net radiation Rn in MJ/m2/day")
    vapor_pressure_deficit_kpa: float = Field(..., ge=0.0, description="Vapor pressure deficit (es - ea) in kPa")
    method: str = Field(default="FAO-56 Penman-Monteith", description="Calculation methodology")
    quality_flag: str = Field(default="VALID", description="Data quality status")


class CropWaterDemandResult(BaseModel):
    """Stage-specific crop water demand calculation."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Target Upazila identifier")
    date: str = Field(..., description="Observation date (YYYY-MM-DD)")
    crop_name: str = Field(..., description="Crop identifier, e.g. Boro Rice")
    growth_stage: str = Field(..., description="Active phenological stage")
    kc_current: float = Field(..., ge=0.2, le=2.0, description="Interpolated crop coefficient")
    et0_mm_day: float = Field(..., ge=0.0, description="Reference evapotranspiration ET0 in mm/day")
    etc_mm_day: float = Field(..., ge=0.0, description="Crop water demand ETc = Kc * ET0 in mm/day")


class SoilWaterDeficitResult(BaseModel):
    """Root-zone soil water balance and depletion modeling result."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Target Upazila identifier")
    date: str = Field(..., description="Date of water balance calculation")
    crop_name: str = Field(..., description="Crop identifier")
    growth_stage: str = Field(..., description="Active phenological stage")
    depletion_mm: float = Field(..., ge=0.0, description="Root-zone water depletion Dt in mm")
    taw_mm: float = Field(..., gt=0.0, description="Total available soil water in root zone (mm)")
    raw_mm: float = Field(..., gt=0.0, description="Readily available soil water threshold (mm)")
    effective_rain_mm: float = Field(..., ge=0.0, description="Infiltrated effective precipitation (mm)")
    irrigation_applied_mm: float = Field(default=0.0, ge=0.0, description="Irrigation depth applied (mm)")
    is_stress_critical: bool = Field(..., description="True if depletion Dt >= RAW")
    storage_capacity_remaining_mm: float = Field(..., ge=0.0, description="Available capacity to absorb rain without runoff")


class HaorFloodIndexResult(BaseModel):
    """Multi-factor transboundary Haor flash-flood hazard score."""
    model_config = ConfigDict(protected_namespaces=())

    catchment_id: str = Field(..., description="Target river/catchment ID")
    date: str = Field(..., description="Calculation date")
    i_flood: float = Field(..., ge=0.0, le=1.0, description="Normalized composite hazard index [0, 1]")
    hazard_tier: Literal["NORMAL", "ADVISORY", "WARNING", "EMERGENCY"] = Field(..., description="Categorical hazard level")
    p_cat_48h_mm: float = Field(..., ge=0.0, description="48h Meghalaya catchment accumulated rainfall (mm)")
    water_level_m_pwd: float = Field(..., description="Surma river water level (m PWD)")
    rate_of_rise_24h_m: float = Field(..., description="24-hour rate of water level rise (m/day)")
    inundation_fraction: float = Field(..., ge=0.0, le=1.0, description="Estimated/observed flooded area fraction")
    sub_indices: Dict[str, float] = Field(..., description="Breakdown of f_P, f_S, f_R, f_I sub-indices")


class ThermalStressResult(BaseModel):
    """Biometeorological temperature stress evaluation."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Target Upazila identifier")
    date: str = Field(..., description="Evaluation date")
    stress_type: Literal["HEAT", "COLD", "NONE"] = Field(..., description="Type of thermal stress detected")
    intensity_index: float = Field(..., ge=0.0, le=1.0, description="Normalized stress intensity [0, 1]")
    consecutive_days: int = Field(..., ge=0, description="Consecutive days threshold has been breached")
    is_critical: bool = Field(..., description="True if consecutive days meet agronomic warning trigger")
    mitigation_water_depth_cm: float = Field(default=0.0, description="Recommended water buffering layer depth in cm")
