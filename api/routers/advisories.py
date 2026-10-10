"""Agricultural advisories endpoint exposing 4-tier decision support and Phase 9 rules."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from api.dependencies import get_repository
from api.data_access.repository import AgriculturalDataRepository
from api.schemas.advisories import AdvisoryResponse, AdvisoryEvaluateRequest
from analytics.engine.context_gate import ContextGatingError

router = APIRouter(tags=["Actionable Advisories & Recommendations"])


@router.get(
    "/api/v1/upazilas/{upazila_id}/advisories",
    response_model=AdvisoryResponse,
    summary="Retrieve context-gated 4-tier agricultural advisory for an Upazila",
    description=(
        "Primary decision-support endpoint evaluating active Phase 9 scientific rules "
        "(irrigation postponement, moisture deficit alert, Haor early harvest, thermal stress). "
        "Strictly gated by Upazila, Crop, and Phenological Stage (DEC-17)."
    ),
)
def get_upazila_advisories(
    upazila_id: str = Path(..., description="Target Upazila code (e.g. BD-50-20-30 or shorthand BD-50-28)"),
    crop: str = Query(..., description="Active crop identifier (e.g. boro_rice, boro)"),
    stage: str = Query(..., description="Active phenological growth stage (e.g. vegetative_tillering, flowering, dough)"),
    start_date: Optional[str] = Query(None, description="Start date for custom analysis period (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date for custom analysis period (YYYY-MM-DD)"),
    repo: AgriculturalDataRepository = Depends(get_repository),
) -> AdvisoryResponse:
    """Evaluate and retrieve 4-tier agricultural decision support."""
    canonical_id = repo.resolve_upazila_id(upazila_id)
    if not repo.is_known_upazila(canonical_id):
        raise HTTPException(
            status_code=404,
            detail=f"Upazila '{upazila_id}' not found or outside active testbeds and national registry.",
        )

    if not crop.strip() or not stage.strip():
        raise ContextGatingError("Fields 'crop' and 'stage' are mandatory for advisory generation (DEC-17).")

    result = repo.evaluate_advisories(
        upazila_id=canonical_id,
        crop=crop,
        stage=stage,
        start_date=start_date,
        end_date=end_date,
    )
    if not result:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to generate advisories for Upazila '{upazila_id}'.",
        )
    return AdvisoryResponse(**result)


@router.post(
    "/api/v1/advisories/evaluate",
    response_model=AdvisoryResponse,
    summary="Evaluate custom scenario through the Phase 9 recommendation engine",
    description=(
        "Allows direct evaluation of advisory rules with custom environmental inputs, "
        "data timestamps, or ensemble spread metrics."
    ),
)
def evaluate_custom_advisories(
    payload: AdvisoryEvaluateRequest,
    repo: AgriculturalDataRepository = Depends(get_repository),
) -> AdvisoryResponse:
    """Evaluate advisory rules for a custom scenario."""
    canonical_id = repo.resolve_upazila_id(payload.upazila_id)
    if not repo.is_known_upazila(canonical_id):
        raise HTTPException(
            status_code=404,
            detail=f"Upazila '{payload.upazila_id}' not found or outside active testbeds and national registry.",
        )

    result = repo.evaluate_advisories(
        upazila_id=canonical_id,
        crop=payload.crop_name,
        stage=payload.growth_stage,
        start_date=payload.start_date,
        end_date=payload.end_date,
        custom_inputs=payload.inputs,
        data_timestamp_utc=payload.data_timestamp_utc,
        ensemble_spread_pct=payload.ensemble_spread_pct,
        rain_prob_pct=payload.rain_prob_pct,
    )
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Failed to evaluate custom advisory scenario.",
        )
    return AdvisoryResponse(**result)
