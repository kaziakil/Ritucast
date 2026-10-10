"""Metadata schemas for crops, phenology stages, and agricultural seasons."""

from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class CropInfo(BaseModel):
    """Calibrated crop metadata."""
    model_config = ConfigDict(protected_namespaces=())

    crop_id: str = Field(..., description="Crop identifier code (e.g. boro_rice)")
    name_en: str = Field(..., description="English crop name")
    name_bn: str = Field(..., description="Bengali crop name")
    scientific_name: str = Field(default="Oryza sativa L.", description="Botanical name")
    typical_duration_days: int = Field(..., description="Life cycle duration in days")
    supported_stages: List[str] = Field(..., description="Calibrated phenological stages")
    calibration_status: str = Field(default="PILOT_CALIBRATED", description="Calibration status")


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
