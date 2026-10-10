"""Schemas package exporting Pydantic v2 data models for Ritucast API v1."""

from api.schemas.common import ApiResponse, ErrorResponse, HealthResponse, ReadinessResponse
from api.schemas.geo import CentroidCoord, UpazilaSummary, UpazilaDetail
from api.schemas.metadata import CropInfo, SeasonInfo
from api.schemas.indicators import (
    WeatherDailyObservation,
    WeatherDailyForecast,
    WeatherFeedResponse,
    WaterBalanceIndicators,
    WaterBalanceResponse,
    FloodHazardIndicators,
    FloodHazardResponse,
)
from api.schemas.advisories import (
    Tier1ObservationSummary,
    Tier2IndicatorSummary,
    Tier3PredictionSummary,
    Tier4RecommendationDetail,
    AdvisoryResponse,
    AdvisoryEvaluateRequest,
)
from api.schemas.risk import (
    RiskEvaluationRequest,
    RiskEvaluationResponse,
    PhysicalHazardAssessment,
)
from api.schemas.provenance import (
    DatasetProvenanceItem,
    ModelMethodologyItem,
    SystemProvenanceResponse,
)

__all__ = [
    "ApiResponse",
    "ErrorResponse",
    "HealthResponse",
    "ReadinessResponse",
    "CentroidCoord",
    "UpazilaSummary",
    "UpazilaDetail",
    "CropInfo",
    "SeasonInfo",
    "WeatherDailyObservation",
    "WeatherDailyForecast",
    "WeatherFeedResponse",
    "WaterBalanceIndicators",
    "WaterBalanceResponse",
    "FloodHazardIndicators",
    "FloodHazardResponse",
    "Tier1ObservationSummary",
    "Tier2IndicatorSummary",
    "Tier3PredictionSummary",
    "Tier4RecommendationDetail",
    "AdvisoryResponse",
    "AdvisoryEvaluateRequest",
    "RiskEvaluationRequest",
    "RiskEvaluationResponse",
    "PhysicalHazardAssessment",
    "DatasetProvenanceItem",
    "ModelMethodologyItem",
    "SystemProvenanceResponse",
]
