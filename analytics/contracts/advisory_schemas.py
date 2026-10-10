"""Pydantic v2 schemas for actionable agricultural recommendation cards."""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator


class AdvisorySeverity(str, Enum):
    """Categorical advisory urgency."""
    INFO = "INFO"
    ADVISORY = "ADVISORY"
    WARNING = "WARNING"
    EMERGENCY = "EMERGENCY"


class AdvisoryStatus(str, Enum):
    """Advisory generation status."""
    ACTIVE = "ACTIVE"
    SUPPRESSED = "SUPPRESSED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class ContextGatePayload(BaseModel):
    """Contextual metadata required to gate advisory release (DEC-17)."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Target Upazila identifier (e.g. BD-50-20-30)")
    crop_name: str = Field(..., description="Active crop identifier (e.g. Boro Rice)")
    growth_stage: str = Field(..., description="Current validated phenological stage (e.g. Tillering, Flowering)")


class AdvisoryCard(BaseModel):
    """Complete actionable recommendation card conforming to 5-section anatomy (DEC-30)."""
    model_config = ConfigDict(protected_namespaces=())

    advisory_id: str = Field(..., description="Unique advisory instance ID")
    rule_id: str = Field(..., description="Underlying scientific rule ID (e.g. RULE-IRR-01)")
    upazila_id: str = Field(..., description="Target Upazila ID")
    crop_name: str = Field(..., description="Crop name")
    growth_stage: str = Field(..., description="Active phenological stage")
    timestamp_utc: str = Field(..., description="Advisory generation timestamp (ISO-8601)")
    valid_until_utc: str = Field(..., description="Advisory validity expiration timestamp")
    severity: AdvisorySeverity = Field(..., description="Advisory urgency level")
    status: AdvisoryStatus = Field(default=AdvisoryStatus.ACTIVE, description="Status (Active/Suppressed)")

    # Section 1 & 2: Headline and Plain Language Advisory (Bangla)
    headline_bn: str = Field(..., description="Plain-language Bengali headline")
    plain_language_bn: str = Field(..., description="Actionable explanation in clear rural Bengali")

    # Section 3: Concrete Action Directives
    action_items_bn: List[str] = Field(..., description="Bullet point action checklist for farmers")

    # Section 4: Mandatory Field Verification & Anti-Overconfidence Safeguard (DEC-10, AGENTS.md)
    field_verification_bn: str = Field(
        default="সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।",
        description="Mandatory ground inspection instruction preventing blind model reliance",
    )

    # Section 5: Uncertainty, Scientific Attribution & Explanations
    uncertainty_description_bn: str = Field(..., description="Explicit description of forecast spread or sensor uncertainty")
    suppression_reason: Optional[str] = Field(default=None, description="Detailed explanation if suppressed")
    supporting_indicators: Dict[str, Any] = Field(default_factory=dict, description="Supporting physical variables")
    provenance_manifest: Dict[str, str] = Field(default_factory=dict, description="Source dataset versions and models")

    @field_validator("headline_bn", "plain_language_bn")
    @classmethod
    def validate_anti_overconfidence_terms(cls, v: str) -> str:
        """Enforce strict ban on overconfident, certainty-claiming language."""
        banned_phrases = ["১০০% নিশ্চিত", "নিশ্চিত বৃষ্টি", "ফলনের নিশ্চয়তা"]
        for phrase in banned_phrases:
            if phrase in v:
                raise ValueError(f"Banned overconfident linguistic phrase detected: '{phrase}'")
        return v
