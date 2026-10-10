"""Water balance endpoint exposing Tier 2 FAO-56 Penman-Monteith indicators."""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from api.dependencies import get_repository
from api.data_access.repository import AgriculturalDataRepository
from api.schemas.indicators import WaterBalanceResponse
from analytics.engine.context_gate import ContextGatingError

router = APIRouter(prefix="/api/v1/upazilas", tags=["Agronomic Indicators"])


@router.get(
    "/{upazila_id}/water-balance",
    response_model=WaterBalanceResponse,
    summary="Calculate Tier 2 FAO-56 Reference ET0 and Root-Zone Water Deficit",
    description=(
        "Calculates Penman-Monteith ET0, calibrated crop evapotranspiration (ETc), and "
        "daily root-zone water depletion (Dt) with AWD thresholds for the given Upazila, crop, and stage."
    ),
)
def get_upazila_water_balance(
    upazila_id: str = Path(..., description="Target Upazila code (e.g. BD-50-20-30 or BD-50-28)"),
    crop: str = Query(..., description="Crop identifier (e.g. boro_rice)"),
    stage: str = Query(..., description="Phenological growth stage (e.g. vegetative_tillering, flowering)"),
    repo: AgriculturalDataRepository = Depends(get_repository),
) -> WaterBalanceResponse:
    """Fetch root-zone water balance indicators."""
    canonical_id = repo.resolve_upazila_id(upazila_id)
    if not repo.is_pilot_upazila(canonical_id):
        raise HTTPException(
            status_code=404,
            detail=f"Upazila '{upazila_id}' not found or outside active pilot testbeds.",
        )

    if not crop.strip() or not stage.strip():
        raise ContextGatingError("Both 'crop' and 'stage' query parameters are mandatory for water balance calculation.")

    result = repo.get_water_balance(upazila_id=canonical_id, crop=crop, stage=stage)
    if not result:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to calculate water balance for Upazila '{upazila_id}'.",
        )
    return WaterBalanceResponse(**result)
