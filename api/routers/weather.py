"""Weather feed endpoint exposing Tier 1 sensor observations and Tier 3 NWP forecasts."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from api.dependencies import get_repository
from api.data_access.repository import AgriculturalDataRepository
from api.schemas.indicators import WeatherFeedResponse

router = APIRouter(prefix="/api/v1/upazilas", tags=["Weather Observations & Forecasts"])


@router.get(
    "/{upazila_id}/weather",
    response_model=WeatherFeedResponse,
    summary="Retrieve Tier 1 observations and Tier 3 probabilistic forecasts for an Upazila",
    description=(
        "Returns empirical meteorological observations (Tier 1: NASA POWER / BMD station) "
        "and numerical weather prediction forecasts (Tier 3: ECMWF IFS / NOAA GFS) for the specified Upazila."
    ),
)
def get_upazila_weather(
    upazila_id: str = Path(..., description="Target Upazila code (e.g. BD-50-20-30 or shorthand BD-50-28)"),
    start_date: Optional[str] = Query(None, description="Start date for custom analysis window (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date for custom analysis window (YYYY-MM-DD)"),
    repo: AgriculturalDataRepository = Depends(get_repository),
) -> WeatherFeedResponse:
    """Fetch weather observation and forecast feed."""
    feed = repo.get_weather_feed(upazila_id, start_date=start_date, end_date=end_date)
    if not feed:
        raise HTTPException(
            status_code=404,
            detail=f"Upazila '{upazila_id}' not found or outside active pilot testbeds.",
        )
    return WeatherFeedResponse(**feed)
