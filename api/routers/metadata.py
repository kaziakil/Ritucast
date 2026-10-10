"""Crops and cropping seasons metadata discovery endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from api.schemas.metadata import CropInfo, SeasonInfo
from api.data_access.repository import AgriculturalDataRepository
from api.dependencies import get_repository

router = APIRouter(prefix="/api/v1", tags=["Agricultural Metadata"])


@router.get("/crops", response_model=Dict[str, Any], summary="List calibrated crops")
async def list_crops(repo: AgriculturalDataRepository = Depends(get_repository)):
    """Retrieve list of crops calibrated in the Ritucast pilot (anchor: Boro rice)."""
    crops = repo.get_crops()
    return {
        "status": "success",
        "count": len(crops),
        "data": [c.model_dump() for c in crops],
    }


@router.get("/seasons", response_model=Dict[str, Any], summary="List cropping seasons")
async def list_seasons(repo: AgriculturalDataRepository = Depends(get_repository)):
    """Retrieve agricultural seasons recognized in Bangladesh (Boro, Aus, Aman)."""
    seasons = repo.get_seasons()
    return {
        "status": "success",
        "count": len(seasons),
        "data": [s.model_dump() for s in seasons],
    }
