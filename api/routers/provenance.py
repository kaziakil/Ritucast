"""System provenance and data freshness router."""

from fastapi import APIRouter, Depends
from api.dependencies import get_repository
from api.data_access.repository import AgriculturalDataRepository
from api.schemas.provenance import SystemProvenanceResponse

router = APIRouter(prefix="/api/v1", tags=["Data Freshness & Provenance"])


@router.get(
    "/provenance",
    response_model=SystemProvenanceResponse,
    summary="Retrieve system data freshness, methodology inventory, and scientific safeguards",
    description=(
        "Exposes dataset update timestamps, source agency attributions, equations, "
        "and scientific non-goal boundary declarations (DEC-06)."
    ),
)
def get_provenance(
    repo: AgriculturalDataRepository = Depends(get_repository),
) -> SystemProvenanceResponse:
    """Fetch system provenance and freshness metadata."""
    return SystemProvenanceResponse(**repo.get_system_provenance())
