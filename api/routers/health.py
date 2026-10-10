"""Health and readiness probe endpoints."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.config import settings
from api.schemas.common import HealthResponse, ReadinessResponse
from api.data_access.repository import AgriculturalDataRepository
from api.dependencies import get_repository

router = APIRouter(tags=["System Health & Readiness"])


@router.get("/health", response_model=HealthResponse, summary="Process liveness check")
@router.get("/api/v1/health", response_model=HealthResponse, include_in_schema=False)
async def get_health():
    """Verify that the FastAPI application process is running and accepting HTTP requests."""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
    )


@router.get("/ready", response_model=ReadinessResponse, summary="Analytical readiness check")
@router.get("/api/v1/ready", response_model=ReadinessResponse, include_in_schema=False)
async def get_readiness(repo: AgriculturalDataRepository = Depends(get_repository)):
    """Verify that required Phase 8 processed Parquet tables and analytical dependencies are ready."""
    readiness = repo.check_readiness()
    http_status = status.HTTP_200_OK if readiness["status"] == "ready" else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=http_status,
        content=readiness,
    )
