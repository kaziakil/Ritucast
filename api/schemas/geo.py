"""Geographic metadata and administrative boundary schemas."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class CentroidCoord(BaseModel):
    """Geographic centroid coordinate."""
    lat: float = Field(..., description="Latitude in decimal degrees")
    lon: float = Field(..., description="Longitude in decimal degrees")


class UpazilaSummary(BaseModel):
    """Summary of an authorized pilot Upazila."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Official BBS Upazila code (e.g. BD-50-20-30)")
    name_en: str = Field(..., description="English Upazila name")
    name_bn: str = Field(..., description="Bengali Upazila name")
    district_name: str = Field(..., description="District (Zila) name")
    division_name: str = Field(..., description="Administrative Division name")
    aez_code: int = Field(..., description="Agro-Ecological Zone (AEZ) numeric code")
    aez_name: str = Field(..., description="Agro-Ecological Zone canonical name")
    centroid: CentroidCoord = Field(..., description="Geographic administrative centroid")
    primary_risk: str = Field(..., description="Primary agricultural hazard domain")


class UpazilaDetail(UpazilaSummary):
    """Detailed metadata for an Upazila including geometry and crop calibration."""
    area_sq_km: Optional[float] = Field(default=None, description="Geographic area in km2")
    calibrated_crops: List[str] = Field(default_factory=list, description="List of calibrated crops")
    geometry_type: str = Field(default="Polygon", description="GeoJSON geometry type")
    available_analysis_periods: List[str] = Field(
        default_factory=lambda: ["2025-2026 Boro Season", "Current Operational (7-Day)"],
        description="Supported analysis windows",
    )
