"""Analytics contracts and Pydantic v2 schemas."""

from analytics.contracts.indicator_schemas import (
    DescriptiveAgroclimaticSummary,
    ReferenceET0Result,
    CropWaterDemandResult,
    SoilWaterDeficitResult,
    HaorFloodIndexResult,
    ThermalStressResult,
)
from analytics.contracts.advisory_schemas import (
    AdvisoryCard,
    AdvisorySeverity,
    AdvisoryStatus,
    ContextGatePayload,
)

__all__ = [
    "DescriptiveAgroclimaticSummary",
    "ReferenceET0Result",
    "CropWaterDemandResult",
    "SoilWaterDeficitResult",
    "HaorFloodIndexResult",
    "ThermalStressResult",
    "AdvisoryCard",
    "AdvisorySeverity",
    "AdvisoryStatus",
    "ContextGatePayload",
]
