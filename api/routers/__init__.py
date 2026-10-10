"""Routers package exporting all modular API routers."""

from api.routers.health import router as health_router
from api.routers.geo import router as geo_router
from api.routers.metadata import router as metadata_router
from api.routers.weather import router as weather_router
from api.routers.water_balance import router as water_balance_router
from api.routers.flood_hazard import router as flood_hazard_router
from api.routers.advisories import router as advisories_router
from api.routers.risk import router as risk_router
from api.routers.provenance import router as provenance_router

__all__ = [
    "health_router",
    "geo_router",
    "metadata_router",
    "weather_router",
    "water_balance_router",
    "flood_hazard_router",
    "advisories_router",
    "risk_router",
    "provenance_router",
]
