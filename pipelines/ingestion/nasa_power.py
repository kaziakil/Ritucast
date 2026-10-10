"""
NASA POWER Daily Agrometeorology Ingestion Adapter (DATA-MET-01).
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from pipelines.common.base_adapter import BaseAdapter
from pipelines.common.rate_limiter import RateLimiter

logger = logging.getLogger("ritucast.ingestion.nasa_power")

class NasaPowerAdapter(BaseAdapter):
    """Ingests daily agroclimatology from NASA POWER API."""

    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
    COMMUNITY = "AG"
    DEFAULT_PARAMETERS = [
        "T2M",
        "T2M_MAX",
        "T2M_MIN",
        "ALLSKY_SFC_SW_DWN",
        "RH2M",
        "WS2M",
        "PRECTOTCORR",
    ]

    def __init__(
        self,
        rate_limiter: Optional[RateLimiter] = None,
        timeout_seconds: int = 30,
        max_retries: int = 3,
    ):
        # Default NASA POWER rate limit is 30 req/min
        limiter = rate_limiter or RateLimiter(requests_per_minute=30)
        super().__init__(
            source_id="DATA-MET-01",
            name="NASA POWER Daily Agrometeorology",
            rate_limiter=limiter,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
        )

    def fetch_live(
        self,
        latitude: float,
        longitude: float,
        start_date: str,  # YYYYMMDD
        end_date: str,    # YYYYMMDD
        parameters: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Queries NASA POWER point daily agrometeorology endpoint."""
        params_list = parameters or self.DEFAULT_PARAMETERS
        query_params = {
            "parameters": ",".join(params_list),
            "community": self.COMMUNITY,
            "longitude": longitude,
            "latitude": latitude,
            "start": start_date.replace("-", ""),
            "end": end_date.replace("-", ""),
            "format": "JSON",
        }
        logger.info(f"Querying NASA POWER at ({latitude}, {longitude}) from {start_date} to {end_date}")
        return self._execute_http_get(self.BASE_URL, params=query_params)

    def load_sample(self, fixture_path: Optional[str] = None) -> Dict[str, Any]:
        """Loads sample synthetic NASA POWER payload from disk."""
        path = fixture_path or "data/sample/nasa_power_sample.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fixture not found at {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse_records(self, raw_payload: Dict[str, Any], upazila_id: str) -> List[Dict[str, Any]]:
        """Transforms NASA POWER JSON structure into a normalized list of records."""
        properties = raw_payload.get("properties", {})
        parameter_data = properties.get("parameter", {})
        header = raw_payload.get("header", {})
        fill_val = header.get("fill_value", -999.0)

        # Dates present in T2M
        t2m_dict = parameter_data.get("T2M", {})
        dates = sorted(t2m_dict.keys())

        records = []
        for d_str in dates:
            # Parse YYYYMMDD to YYYY-MM-DD
            try:
                obs_date = datetime.strptime(d_str, "%Y%m%d").strftime("%Y-%m-%d")
            except ValueError:
                obs_date = d_str

            def get_val(param_name: str) -> Optional[float]:
                val = parameter_data.get(param_name, {}).get(d_str)
                if val is None or val == fill_val:
                    return None
                return float(val)

            rec = {
                "upazila_id": upazila_id,
                "date": obs_date,
                "t2m_c": get_val("T2M"),
                "t2m_max_c": get_val("T2M_MAX"),
                "t2m_min_c": get_val("T2M_MIN"),
                "solar_rad_mj_m2": get_val("ALLSKY_SFC_SW_DWN"),
                "rh2m_pct": get_val("RH2M"),
                "wind_speed_2m_ms": get_val("WS2M"),
                "precipitation_mm": get_val("PRECTOTCORR"),
                "source_id": self.source_id,
            }
            records.append(rec)

        return records
