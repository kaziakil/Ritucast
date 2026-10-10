"""Metadata schemas for crops, phenology stages, and agricultural seasons."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class CropInfo(BaseModel):
    """Calibrated and supported crop metadata."""
    model_config = ConfigDict(protected_namespaces=())

    crop_id: str = Field(..., description="Crop identifier code (e.g. boro_rice)")
    name_en: str = Field(..., description="English crop name")
    name_bn: str = Field(..., description="Bengali crop name")
    category: str = Field(default="cereals", description="Crop category code")
    category_en: str = Field(default="Cereals & Grains", description="Crop category in English")
    category_bn: str = Field(default="দানাশস্য", description="Crop category in Bengali")
    scientific_name: str = Field(default="Oryza sativa L.", description="Botanical name")
    typical_duration_days: int = Field(..., description="Life cycle duration in days")
    supported_stages: List[str] = Field(..., description="Supported phenological stages")
    calibration_status: str = Field(default="PILOT_CALIBRATED", description="Calibration level: PILOT_CALIBRATED, FULL_CALIBRATION, or REGIONAL_SUPPORT")
    primary_season: Optional[str] = Field(default=None, description="Primary cropping season in Bangladesh")
    kc_mid: Optional[float] = Field(default=None, description="Mid-season crop coefficient (FAO-56 Kc)")
    analytical_support_description: Optional[str] = Field(default=None, description="Description of analytical capability")


class SeasonInfo(BaseModel):
    """Agricultural cropping season metadata."""
    model_config = ConfigDict(protected_namespaces=())

    season_id: str = Field(..., description="Season code (e.g. boro_2026)")
    name_en: str = Field(..., description="English season name")
    name_bn: str = Field(..., description="Bengali season name")
    start_month: str = Field(..., description="Season start calendar month")
    end_month: str = Field(..., description="Season harvest calendar month")
    primary_crops: List[str] = Field(..., description="Primary crops cultivated")
    is_active_season: bool = Field(..., description="Whether currently in active season window")
