"""Main entrypoint for Ritucast Agricultural Intelligence Backend API Service."""

import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import get_settings
from api.middleware import (
    register_error_handlers,
    SecurityHeadersMiddleware,
    RequestSizeLimitMiddleware,
    RateLimitMiddleware,
    StructuredLoggingMiddleware,
)
from api.routers import (
    health_router,
    geo_router,
    metadata_router,
    weather_router,
    water_balance_router,
    flood_hazard_router,
    advisories_router,
    risk_router,
    provenance_router,
)


def create_app() -> FastAPI:
    """Application factory for Ritucast API service."""
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_V1_STR,
        description=(
            "Evidence-based agricultural intelligence and decision-support API for Bangladesh. "
            "Exposes validated observations (Tier 1), physical indicators (Tier 2), "
            "probabilistic forecasts (Tier 3), and actionable agronomic recommendations (Tier 4) "
            "for pilot testbeds in High Barind Tract (Rajshahi) and Haor Basin (Sylhet)."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # Structured Logging & Correlation Tracking Middleware
    app.add_middleware(StructuredLoggingMiddleware)

    # Security Headers Middleware (OWASP defensive headers)
    app.add_middleware(SecurityHeadersMiddleware)

    # Request Size Limit Middleware (DoS / memory exhaustion prevention)
    app.add_middleware(
        RequestSizeLimitMiddleware,
        max_bytes=settings.MAX_REQUEST_SIZE_BYTES,
    )

    # Rate Limiting Middleware (Sliding window client rate control)
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=settings.RATE_LIMIT_PER_MINUTE,
        enabled=settings.ENABLE_RATE_LIMIT,
    )

    # Register centralized exception handlers
    register_error_handlers(app)

    # Register modular routers
    app.include_router(health_router)
    app.include_router(geo_router)
    app.include_router(metadata_router)
    app.include_router(weather_router)
    app.include_router(water_balance_router)
    app.include_router(flood_hazard_router)
    app.include_router(advisories_router)
    app.include_router(risk_router)
    app.include_router(provenance_router)

    return app


app = create_app()


def export_openapi_json(output_path: str = "docs/backend/openapi.json") -> None:
    """Generate and write OpenAPI 3.0 schema to documentation directory."""
    openapi_schema = app.openapi()
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    print(f"OpenAPI schema exported to {output_path}")


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
