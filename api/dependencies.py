"""Dependency injection providers for FastAPI routers."""

from functools import lru_cache
from api.data_access.repository import AgriculturalDataRepository
from analytics.engine.advisory_engine import AgriculturalRecommendationEngine


@lru_cache()
def get_repository() -> AgriculturalDataRepository:
    """Return cached singleton instance of AgriculturalDataRepository."""
    return AgriculturalDataRepository()


@lru_cache()
def get_recommendation_engine() -> AgriculturalRecommendationEngine:
    """Return cached singleton instance of AgriculturalRecommendationEngine."""
    return AgriculturalRecommendationEngine()
