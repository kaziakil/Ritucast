"""Health and readiness probe endpoints."""

import time
import resource
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.config import settings
from api.schemas.common import HealthResponse, ReadinessResponse, DeepHealthResponse
from api.data_access.repository import AgriculturalDataRepository
from api.dependencies import get_repository
from pipelines.validation.drift_monitor import PipelineDriftMonitor

START_TIME = time.time()

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


@router.get("/health/deep", response_model=DeepHealthResponse, summary="Deep production diagnostics probe")
@router.get("/api/v1/health/deep", response_model=DeepHealthResponse, include_in_schema=False)
async def get_deep_health(repo: AgriculturalDataRepository = Depends(get_repository)):
    """Execute deep operational health check across data store, pipeline freshness, and memory."""
    uptime = round(time.time() - START_TIME, 2)
    rusage = resource.getrusage(resource.RUSAGE_SELF)
    # ru_maxrss is in bytes on macOS Darwin and kilobytes on Linux
    max_rss_mb = round(rusage.ru_maxrss / (1024.0 * 1024.0), 2) if rusage.ru_maxrss > 1000000 else round(rusage.ru_maxrss / 1024.0, 2)

    # Audit pipeline files
    pipeline_report = PipelineDriftMonitor.audit_pipeline(repo.processed_dir)
    readiness = repo.check_readiness()

    overall_status = "healthy"
    if pipeline_report.circuit_breaker_tripped:
        overall_status = "degraded" if pipeline_report.overall_status == "DEGRADED" else "unhealthy"

    deep_payload = {
        "status": overall_status,
        "version": settings.APP_VERSION,
        "uptime_seconds": uptime,
        "system_metrics": {
            "memory_max_rss_mb": max_rss_mb,
            "rate_limit_enabled": settings.ENABLE_RATE_LIMIT,
            "payload_max_bytes": settings.MAX_REQUEST_SIZE_BYTES,
        },
        "components": {
            "data_store": {
                "status": "ready" if readiness["data_store_ready"] else "unready",
                "verified_tables_count": len(readiness["verified_datasets"]),
                "missing_tables_count": len(readiness["missing_dependencies"]),
            },
            "analytics_engine": {
                "status": "ready",
                "fao56_penman_monteith": "CALIBRATED (EQN-ET0-01)",
                "soil_water_deficit": "CALIBRATED (EQN-SWD-01)",
                "haor_flood_hazard": "CALIBRATED (IDX-FLD-01)",
            },
            "geographic_resolver": {
                "status": "ready",
                "pilot_regions": ["High Barind Tract (AEZ-26)", "Haor Basin (AEZ-21)"],
                "pilot_upazilas_count": 4,
            },
        },
        "pipeline_health": pipeline_report.to_dict(),
        "governance": {
            "context_gating": "ENFORCED (DEC-17)",
            "suppression_policy": "ACTIVE (DEC-10)",
            "pii_posture": "ZERO_PII (DEC-60)",
            "hardware_budget": "<=1.5MB wire payload (DEC-09)",
        },
    }

    http_status = status.HTTP_200_OK if overall_status != "unhealthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(
        status_code=http_status,
        content=deep_payload,
    )
