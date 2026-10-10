"""
Open-Meteo Operational Weather Forecast Ingestion Adapter (DATA-FCST-01).
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from pipelines.common.base_adapter import BaseAdapter
from pipelines.common.rate_limiter import RateLimiter

logger = logging.getLogger("ritucast.ingestion.open_meteo")

class OpenMeteoAdapter(BaseAdapter):
    """Ingests numerical weather predictions from Open-Meteo API."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    DEFAULT_MODELS = ["ecmwf_ifs025", "gfs_seamless"]
    DEFAULT_HOURLY = [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation_probability",
        "precipitation",
        "wind_speed_10m",
    ]
    DEFAULT_DAILY = [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "precipitation_probability_max",
    ]

    def __init__(
        self,
        rate_limiter: Optional[RateLimiter] = None,
        timeout_seconds: int = 20,
        max_retries: int = 3,
    ):
        limiter = rate_limiter or RateLimiter(requests_per_minute=120)
        super().__init__(
            source_id="DATA-FCST-01",
            name="Open-Meteo Operational Weather Forecasts",
            rate_limiter=limiter,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
        )

    def fetch_live(
        self,
        latitude: float,
        longitude: float,
        models: Optional[List[str]] = None,
        hourly_variables: Optional[List[str]] = None,
        daily_variables: Optional[List[str]] = None,
        forecast_days: int = 7,
    ) -> Dict[str, Any]:
        """Queries Open-Meteo forecast API for target point."""
        query_params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(hourly_variables or self.DEFAULT_HOURLY),
            "daily": ",".join(daily_variables or self.DEFAULT_DAILY),
            "models": ",".join(models or self.DEFAULT_MODELS),
            "forecast_days": forecast_days,
            "timezone": "UTC",
        }
        logger.info(f"Querying Open-Meteo at ({latitude}, {longitude}) for {forecast_days} days")
        return self._execute_http_get(self.BASE_URL, params=query_params)

    def load_sample(self, fixture_path: Optional[str] = None) -> Dict[str, Any]:
        """Loads sample synthetic Open-Meteo forecast payload from disk."""
        path = fixture_path or "data/sample/open_meteo_sample.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fixture not found at {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse_hourly_records(self, raw_payload: Dict[str, Any], upazila_id: str) -> List[Dict[str, Any]]:
        """Parses hourly time-series into normalized records."""
        hourly = raw_payload.get("hourly", {})
        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        rhs = hourly.get("relative_humidity_2m", [])
        rain_probs = hourly.get("precipitation_probability", [])
        rains = hourly.get("precipitation", [])
        winds = hourly.get("wind_speed_10m", [])

        records = []
        now_dt = datetime.utcnow()

        for idx, t_str in enumerate(times):
            # Parse ISO string
            try:
                valid_dt = datetime.fromisoformat(t_str)
                valid_iso = valid_dt.isoformat() + "Z" if not t_str.endswith("Z") else t_str
                horizon_hrs = max(0, int((valid_dt - now_dt).total_seconds() // 3600))
            except Exception:
                valid_iso = t_str
                horizon_hrs = idx

            rec = {
                "upazila_id": upazila_id,
                "valid_time_utc": valid_iso,
                "horizon_hours": horizon_hrs,
                "temp_2m_c": temps[idx] if idx < len(temps) else None,
                "rh_2m_pct": rhs[idx] if idx < len(rhs) else None,
                "rain_prob_pct": rain_probs[idx] if idx < len(rain_probs) else None,
                "rain_amount_mm": rains[idx] if idx < len(rains) else None,
                "wind_speed_kmh": winds[idx] if idx < len(winds) else None,
                "model_name": "ecmwf_ifs025",
                "source_id": self.source_id,
            }
            records.append(rec)

        return records

    def parse_daily_records(self, raw_payload: Dict[str, Any], upazila_id: str) -> List[Dict[str, Any]]:
        """Parses daily summary projections."""
        daily = raw_payload.get("daily", {})
        times = daily.get("time", [])
        t_maxs = daily.get("temperature_2m_max", [])
        t_mins = daily.get("temperature_2m_min", [])
        rain_sums = daily.get("precipitation_sum", [])
        prob_maxs = daily.get("precipitation_probability_max", [])

        records = []
        for idx, d_str in enumerate(times):
            rec = {
                "upazila_id": upazila_id,
                "date": d_str,
                "temp_max_c": t_maxs[idx] if idx < len(t_maxs) else None,
                "temp_min_c": t_mins[idx] if idx < len(t_mins) else None,
                "rain_sum_mm": rain_sums[idx] if idx < len(rain_sums) else None,
                "rain_prob_max_pct": prob_maxs[idx] if idx < len(prob_maxs) else None,
                "source_id": self.source_id,
            }
            records.append(rec)

        return records
