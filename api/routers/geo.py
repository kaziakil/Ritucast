"""Geographic boundaries, administrative hierarchy, and Upazila catalog endpoints."""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from api.schemas.geo import UpazilaSummary, UpazilaDetail
from api.data_access.repository import AgriculturalDataRepository
from api.dependencies import get_repository

router = APIRouter(tags=["Geographic Catalog"])


@router.get("/api/v1/upazilas", response_model=Dict[str, Any], summary="List Upazilas")
async def list_upazilas(
    all: bool = Query(False, description="Whether to include all 495 Upazilas across Bangladesh"),
    scope: str = Query("pilot", description="Scope: 'pilot' for 4 testbed Upazilas or 'all' for full national registry"),
    repo: AgriculturalDataRepository = Depends(get_repository),
):
    """Retrieve list of Upazilas. Defaults to authorized pilot Upazilas (count=4) or full registry when all=True."""
    include_all = all or scope.lower() in ("all", "national")
    upazilas = repo.get_all_upazilas(include_all=include_all)
    return {
        "status": "success",
        "count": len(upazilas),
        "data": [u.model_dump() for u in upazilas],
    }


@router.get("/api/v1/geo/hierarchy", response_model=Dict[str, Any], summary="Get complete Bangladesh administrative hierarchy")
async def get_geo_hierarchy(repo: AgriculturalDataRepository = Depends(get_repository)):
    """Retrieve full hierarchical structure: 8 Divisions -> 64 Districts -> 495 Upazilas."""
    hierarchy = repo.get_geo_hierarchy()
    return {
        "status": "success",
        "data": hierarchy,
    }


@router.get("/api/v1/geo/divisions", response_model=Dict[str, Any], summary="List all 8 administrative divisions")
async def list_divisions(repo: AgriculturalDataRepository = Depends(get_repository)):
    """Retrieve all 8 administrative divisions of Bangladesh."""
    divisions = repo.get_divisions()
    return {
        "status": "success",
        "count": len(divisions),
        "data": divisions,
    }


@router.get("/api/v1/geo/districts", response_model=Dict[str, Any], summary="List districts in Bangladesh")
async def list_districts(
    division_id: Optional[str] = Query(None, description="Filter by administrative division ID (e.g. DIV-10)"),
    repo: AgriculturalDataRepository = Depends(get_repository),
):
    """Retrieve all 64 districts or filter by parent division."""
    districts = repo.get_districts(division_id=division_id)
    return {
        "status": "success",
        "count": len(districts),
        "data": districts,
    }


@router.get("/api/v1/upazilas/{upazila_id}", response_model=Dict[str, Any], summary="Get Upazila details")
async def get_upazila(upazila_id: str, repo: AgriculturalDataRepository = Depends(get_repository)):
    """Retrieve detailed metadata, area, and calibrated crops for a specific Upazila."""
    detail = repo.get_upazila_detail(upazila_id)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Upazila '{upazila_id}' not found in authorized pilot testbeds or national administrative registry.",
        )
    return {
        "status": "success",
        "data": detail.model_dump(),
    }
