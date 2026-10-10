"""Haor flash flood hazard endpoint exposing Tier 2 hydrological index."""

from fastapi import APIRouter, Depends, HTTPException, Path
from api.dependencies import get_repository
from api.data_access.repository import AgriculturalDataRepository
from api.schemas.indicators import FloodHazardResponse

router = APIRouter(prefix="/api/v1/upazilas", tags=["Agronomic Indicators"])


@router.get(
    "/{upazila_id}/flood-hazard",
    response_model=FloodHazardResponse,
    summary="Calculate Tier 2 Haor Flash Flood Hazard Index (I_flood)",
    description=(
        "Computes the normalized flash flood hazard index (I_flood) combining transboundary "
        "Meghalaya catchment rainfall, Surma river stage elevation, rate of rise, and SAR inundation fraction."
    ),
)
def get_upazila_flood_hazard(
    upazila_id: str = Path(..., description="Target Upazila code (e.g. BD-60-90-89 or BD-60-90)"),
    repo: AgriculturalDataRepository = Depends(get_repository),
) -> FloodHazardResponse:
    """Fetch Haor flash flood hazard index."""
    canonical_id = repo.resolve_upazila_id(upazila_id)
    if not repo.is_pilot_upazila(canonical_id):
        raise HTTPException(
            status_code=404,
            detail=f"Upazila '{upazila_id}' not found or outside active pilot testbeds.",
        )

    result = repo.get_flood_hazard(upazila_id=canonical_id)
    if not result:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to calculate flood hazard for Upazila '{upazila_id}'.",
        )
    return FloodHazardResponse(**result)
