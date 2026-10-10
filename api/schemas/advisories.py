"""Response schemas for agricultural advisories and 4-tier decision support."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class Tier1ObservationSummary(BaseModel):
    """Tier 1 Empirical observations summary."""
    summary_bn: str = Field(..., description="Bengali description of sensor observations")
    rainfall_7d_total_mm: Optional[float] = Field(default=None, description="7-day cumulative rainfall (mm)")
    mean_temp_c: Optional[float] = Field(default=None, description="Mean temperature (°C)")


class Tier2IndicatorSummary(BaseModel):
    """Tier 2 Derived agronomic indicators summary."""
    summary_bn: str = Field(..., description="Bengali description of calculated indicators")
    soil_water_deficit_dt_mm: Optional[float] = Field(default=None, description="Current soil water deficit Dt (mm)")
    fao56_et0_mm_day: Optional[float] = Field(default=None, description="Reference evapotranspiration (mm/day)")
    flood_hazard_index_iflood: Optional[float] = Field(default=None, description="Haor flood hazard index (0-1)")


class Tier3PredictionSummary(BaseModel):
    """Tier 3 Probabilistic forecast summary."""
    summary_bn: str = Field(..., description="Bengali description of forecast")
    rain_probability_48h_pct: Optional[int] = Field(default=None, description="48-hour rain probability (%)")
    qpf_48h_mm: Optional[float] = Field(default=None, description="48-hour quantitative precipitation forecast (mm)")
    ensemble_spread_pct: Optional[float] = Field(default=None, description="NWP ensemble spread (%)")


class Tier4RecommendationDetail(BaseModel):
    """Tier 4 Actionable recommendation synthesized from Phase 9 rule evaluation."""
    rule_id: str = Field(..., description="Triggered rule identifier (e.g. RULE-IRR-01)")
    category: str = Field(..., description="Advisory category (e.g. IRRIGATION, FLASH_FLOOD, THERMAL_STRESS)")
    action_code: str = Field(..., description="Action directive code")
    severity: str = Field(..., description="Urgency severity (INFO, ADVISORY, WARNING, EMERGENCY)")
    headline_bn: str = Field(..., description="Plain-language Bengali headline")
    body_bn: str = Field(..., description="Operational advisory body in Bengali")
    mandatory_disclaimer_bn: str = Field(
        default="সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।",
        description="Mandatory field verification copy (DEC-10, AGENTS.md)",
    )
    action_items_bn: List[str] = Field(default_factory=list, description="Concrete action directives in Bengali")
    rationale_breakdown: Dict[str, Any] = Field(default_factory=dict, description="Scientific and economic rationale")
    confidence: Dict[str, Any] = Field(default_factory=dict, description="Confidence classification and score")
    is_suppressed: bool = Field(default=False, description="Whether advisory was suppressed due to data age or spread")
    suppression_reason: Optional[str] = Field(default=None, description="Suppression cause if suppressed")


class AdvisoryResponse(BaseModel):
    """Full 4-tier advisory response envelope."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Canonical Upazila ID")
    upazila_name_bn: str = Field(..., description="Upazila name in Bengali")
    crop_id: str = Field(..., description="Crop ID")
    crop_name_bn: str = Field(..., description="Crop name in Bengali")
    growth_stage: str = Field(..., description="Phenological growth stage")
    growth_stage_bn: str = Field(..., description="Growth stage in Bengali")
    generated_at_bst: str = Field(..., description="Generation timestamp in BST")

    tier_1_observations: Tier1ObservationSummary = Field(..., description="Empirical observations")
    tier_2_indicators: Tier2IndicatorSummary = Field(..., description="Derived physical indicators")
    tier_3_predictions: Tier3PredictionSummary = Field(..., description="Probabilistic model forecasts")
    tier_4_recommendation: Tier4RecommendationDetail = Field(..., description="Actionable recommendation")

    all_cards: List[Dict[str, Any]] = Field(default_factory=list, description="All evaluated Phase 9 cards")
    provenance: Dict[str, Any] = Field(default_factory=dict, description="Traceability provenance")


class AdvisoryEvaluateRequest(BaseModel):
    """Direct advisory evaluation request payload."""
    model_config = ConfigDict(protected_namespaces=())

    upazila_id: str = Field(..., description="Target Upazila ID (e.g. BD-50-20-30)")
    crop_name: str = Field(default="Boro Rice", description="Crop name")
    growth_stage: str = Field(..., description="Active phenological stage")
    inputs: Optional[Dict[str, Any]] = Field(default=None, description="Optional custom environmental parameters")
    data_timestamp_utc: Optional[str] = Field(default=None, description="Optional source observation timestamp")
    ensemble_spread_pct: Optional[float] = Field(default=None, description="Optional ensemble spread percentage")
    rain_prob_pct: Optional[float] = Field(default=None, description="Optional rain probability percentage")
