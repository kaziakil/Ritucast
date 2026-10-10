"""Geographic boundaries and Upazila catalog endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from api.schemas.geo import UpazilaSummary, UpazilaDetail
from api.data_access.repository import AgriculturalDataRepository
from api.dependencies import get_repository

router = APIRouter(prefix="/api/v1/upazilas", tags=["Geographic Catalog"])


@router.get("", response_model=Dict[str, Any], summary="List authorized pilot Upazilas")
async def list_upazilas(repo: AgriculturalDataRepository = Depends(get_repository)):
    """Retrieve list of authorized pilot Upazilas in High Barind Tract and Haor Basin with centroid coordinates."""
    upazilas = repo.get_all_upazilas()
    return {
        "status": "success",
        "count": len(upazilas),
        "data": [u.model_dump() for u in upazilas],
    }


@router.get("/{upazila_id}", response_model=Dict[str, Any], summary="Get Upazila details")
async def get_upazila(upazila_id: str, repo: AgriculturalDataRepository = Depends(get_repository)):
    """Retrieve detailed metadata, area, and calibrated crops for a specific Upazila."""
    detail = repo.get_upazila_detail(upazila_id)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Upazila '{upazila_id}' not found in authorized pilot testbeds.",
        )
    return {
        "status": "success",
        "data": detail.model_dump(),
    }
