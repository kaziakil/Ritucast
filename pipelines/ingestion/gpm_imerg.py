"""
GPM IMERG Multi-Satellite Precipitation Ingestion Adapter (DATA-PCP-01).
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from pipelines.common.base_adapter import BaseAdapter
from pipelines.common.rate_limiter import RateLimiter

logger = logging.getLogger("ritucast.ingestion.gpm_imerg")

class GpmImergAdapter(BaseAdapter):
    """Ingests multi-satellite calibrated precipitation estimates (GPM IMERG V07)."""

    CMR_SEARCH_URL = "https://cmr.earthdata.nasa.gov/search/granules.json"
    COLLECTION_EARLY = "GPM_3IMERGDE"
    COLLECTION_FINAL = "GPM_3IMERGDF"

    def __init__(
        self,
        rate_limiter: Optional[RateLimiter] = None,
        timeout_seconds: int = 30,
        max_retries: int = 3,
    ):
        limiter = rate_limiter or RateLimiter(requests_per_minute=60)
        super().__init__(
            source_id="DATA-PCP-01",
            name="GPM IMERG Multi-Satellite Precipitation (V07)",
            rate_limiter=limiter,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
        )

    def fetch_live(
        self,
        bounding_box: List[float],  # [min_lon, min_lat, max_lon, max_lat]
        start_date: str,
        end_date: str,
        is_early_run: bool = False,
    ) -> Dict[str, Any]:
        """Queries NASA CMR for GPM IMERG granules matching domain."""
        short_name = self.COLLECTION_EARLY if is_early_run else self.COLLECTION_FINAL
        query_params = {
            "short_name": short_name,
            "version": "07",
            "bounding_box": ",".join(str(c) for c in bounding_box),
            "temporal": f"{start_date}T00:00:00Z,{end_date}T23:59:59Z",
            "page_size": 50,
        }
        logger.info(f"Querying CMR for {short_name} granules")
        return self._execute_http_get(self.CMR_SEARCH_URL, params=query_params)

    def load_sample(self, fixture_path: Optional[str] = None) -> Dict[str, Any]:
        """Loads sample synthetic GPM IMERG payload from disk."""
        path = fixture_path or "data/sample/gpm_imerg_sample.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fixture not found at {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse_catchment_records(self, raw_payload: Dict[str, Any], catchment_id: str = "MEGHALAYA_ESCARP") -> List[Dict[str, Any]]:
        """Parses catchment rainfall records."""
        raw_records = raw_payload.get("records", [])
        records = []
        for r in raw_records:
            rec = {
                "catchment_id": catchment_id,
                "date": r.get("date"),
                "precipitation_mm": float(r.get("precipitation_cal_mm", 0.0)),
                "random_error_mm": float(r.get("random_error_mm", 0.0)),
                "quality_flag": int(r.get("quality_flag", 0)),
                "source_id": self.source_id,
            }
            records.append(rec)
        return records
