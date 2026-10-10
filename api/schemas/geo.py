"""Geographic metadata and administrative boundary schemas supporting all 64 districts of Bangladesh."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class CentroidCoord(BaseModel):
    """Geographic centroid coordinate."""
    lat: float = Field(..., description="Latitude in decimal degrees")
    lon: float = Field(..., description="Longitude in decimal degrees")


class UpazilaSummary(BaseModel):
    """Summary of an administrative Upazila in Bangladesh."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Official BBS Upazila code (e.g. BD-50-20-30)")
    name_en: str = Field(..., description="English Upazila name")
    name_bn: str = Field(..., description="Bengali Upazila name")
    district_name: str = Field(..., description="District (Zila) name in English")
    division_name: str = Field(..., description="Administrative Division name in English")
    aez_code: int = Field(..., description="Agro-Ecological Zone (AEZ) numeric code")
    aez_name: str = Field(..., description="Agro-Ecological Zone canonical name")
    centroid: CentroidCoord = Field(..., description="Geographic administrative centroid")
    primary_risk: str = Field(..., description="Primary agricultural hazard domain")
    district_id: Optional[str] = Field(default=None, description="Parent District code (e.g. DIST-20)")
    division_id: Optional[str] = Field(default=None, description="Parent Division code (e.g. DIV-50)")
    district_name_bn: Optional[str] = Field(default=None, description="District name in Bengali")
    division_name_bn: Optional[str] = Field(default=None, description="Division name in Bengali")
    is_pilot: bool = Field(default=False, description="Whether Upazila is a primary pilot testbed with full telemetry")


class UpazilaDetail(UpazilaSummary):
    """Detailed metadata for an Upazila including geometry and crop calibration."""
    area_sq_km: Optional[float] = Field(default=None, description="Geographic area in km2")
    calibrated_crops: List[str] = Field(default_factory=list, description="List of calibrated crops")
    geometry_type: str = Field(default="Polygon", description="GeoJSON geometry type")
    available_analysis_periods: List[str] = Field(
        default_factory=lambda: ["Previous 7 Days (Default)", "Previous 14 Days", "Previous 30 Days", "Custom Range"],
        description="Supported analysis windows",
    )


class DistrictSummary(BaseModel):
    """District (Zila) representation."""
    model_config = ConfigDict(protected_namespaces=())

    district_id: str = Field(..., description="District code (e.g. DIST-20)")
    name_en: str = Field(..., description="District name in English")
    name_bn: str = Field(..., description="District name in Bengali")
    division_id: str = Field(..., description="Division code")
    division_name: str = Field(..., description="Division name in English")
    division_name_bn: str = Field(..., description="Division name in Bengali")
    aez_code: int = Field(..., description="Dominant Agro-Ecological Zone code")
    aez_name: str = Field(..., description="Dominant AEZ name")
    primary_risk: str = Field(..., description="Primary agricultural risk")
    upazila_count: int = Field(..., description="Total Upazilas in this District")


class DivisionSummary(BaseModel):
    """Administrative Division representation."""
    model_config = ConfigDict(protected_namespaces=())

    division_id: str = Field(..., description="Division code (e.g. DIV-10)")
    name_en: str = Field(..., description="Division name in English")
    name_bn: str = Field(..., description="Division name in Bengali")
    district_count: int = Field(..., description="Total Districts in this Division")
    upazila_count: int = Field(..., description="Total Upazilas in this Division")
