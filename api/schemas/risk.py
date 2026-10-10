"""Schemas for physical agricultural risk assessment endpoints."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class RiskEvaluationRequest(BaseModel):
    """Agricultural hazard assessment query payload."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., max_length=50, description="Target Upazila code (e.g. BD-50-20-30)")
    crop_id: str = Field(default="boro_rice", max_length=100, description="Crop identifier")
    growth_stage: str = Field(
        ..., max_length=100, description="Active phenological growth stage (e.g. Tillering, Flowering)"
    )
    hazard_types: Optional[List[str]] = Field(
        default_factory=lambda: ["moisture_deficit", "flash_flood", "thermal_stress"],
        description="Hazard domains to evaluate",
    )


class PhysicalHazardAssessment(BaseModel):
    """Assessment of a single physical hazard domain."""
    hazard_domain: str = Field(..., description="Hazard identifier (e.g. moisture_deficit, flash_flood)")
    hazard_tier: str = Field(..., description="Categorical hazard level (LOW, MODERATE, HIGH, CRITICAL)")
    hazard_tier_bn: str = Field(..., description="Hazard level in Bengali")
    primary_metric_name: str = Field(..., description="Primary physical metric driving assessment")
    primary_metric_value: float = Field(..., description="Numerical value of primary metric")
    threshold_applied: float = Field(..., description="Agronomic critical threshold")
    action_warranted: bool = Field(..., description="True if physical threshold breached")


class RiskEvaluationResponse(BaseModel):
    """Complete physical risk assessment response."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Upazila code")
    crop_id: str = Field(..., description="Crop code")
    growth_stage: str = Field(..., description="Growth stage")
    evaluation_date: str = Field(..., description="Evaluation date (YYYY-MM-DD)")
    overall_hazard_tier: str = Field(..., description="Composite peak hazard level")
    overall_hazard_tier_bn: str = Field(..., description="Composite hazard level in Bengali")
    hazard_assessments: List[PhysicalHazardAssessment] = Field(..., description="Detailed assessments per hazard")
    scientific_disclaimer_bn: str = Field(
        default=(
            "এই মূল্যায়ন শুধুমাত্র প্রাকৃতিক পরিবেশগত ঝুঁকির নির্দেশক; "
            "এটি আর্থিক ক্ষতি বা চূড়ান্ত ফলন হ্রাসের নিশ্চয়তা দেয় না।"
        ),
        description="Mandatory scientific safeguard disclaimer (DEC-06)",
    )
    provenance: Dict[str, str] = Field(default_factory=dict, description="Model and data source versions")
