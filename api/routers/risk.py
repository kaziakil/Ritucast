"""Physical hazard assessment router adhering to DEC-06 non-goals."""

from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_repository
from api.data_access.repository import AgriculturalDataRepository
from api.schemas.risk import RiskEvaluationRequest, RiskEvaluationResponse

router = APIRouter(prefix="/api/v1/risk", tags=["Physical Hazard Assessment"])


@router.post(
    "/evaluate",
    response_model=RiskEvaluationResponse,
    summary="Evaluate physical agricultural hazards without uncalibrated probabilities",
    description=(
        "Evaluates environmental hazard thresholds (soil moisture deficit, Haor flash flood, "
        "cold/heat stress) using physical observations and scientific criteria. "
        "Strictly adheres to DEC-06: does not provide uncalibrated crop failure probabilities."
    ),
)
def evaluate_risk(
    payload: RiskEvaluationRequest,
    repo: AgriculturalDataRepository = Depends(get_repository),
) -> RiskEvaluationResponse:
    """Evaluate physical agricultural hazard risks."""
    canonical_id = repo.resolve_upazila_id(payload.upazila_id)
    if not repo.is_pilot_upazila(canonical_id):
        raise HTTPException(
            status_code=404,
            detail=f"Upazila '{payload.upazila_id}' not found or outside active pilot testbeds.",
        )

    result = repo.evaluate_physical_risk(
        upazila_id=canonical_id,
        crop_id=payload.crop_id,
        growth_stage=payload.growth_stage,
        hazard_types=payload.hazard_types,
    )
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Failed to evaluate physical risk for given parameters.",
        )
    return RiskEvaluationResponse(**result)
