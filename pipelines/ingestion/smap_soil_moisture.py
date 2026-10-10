"""
SMAP Enhanced L3 9km Radiometer Soil Moisture Ingestion Adapter (DATA-SMC-01).
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from pipelines.common.base_adapter import BaseAdapter
from pipelines.common.rate_limiter import RateLimiter

logger = logging.getLogger("ritucast.ingestion.smap")

class SmapSoilMoistureAdapter(BaseAdapter):
    """Ingests SMAP Enhanced L3 9km volumetric soil moisture observations (SPL3SMP_E)."""

    def __init__(
        self,
        rate_limiter: Optional[RateLimiter] = None,
        timeout_seconds: int = 30,
        max_retries: int = 3,
    ):
        limiter = rate_limiter or RateLimiter(requests_per_minute=60)
        super().__init__(
            source_id="DATA-SMC-01",
            name="SMAP Enhanced L3 9km Radiometer Soil Moisture",
            rate_limiter=limiter,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
        )

    def fetch_live(self, bounding_box: List[float], date_str: str) -> Dict[str, Any]:
        """Placeholder for CMR granule search or Earthdata cloud fetch."""
        logger.info(f"Querying SMAP observations for {date_str}")
        return self.load_sample()

    def load_sample(self, fixture_path: Optional[str] = None) -> Dict[str, Any]:
        """Loads sample synthetic SMAP payload from disk."""
        path = fixture_path or "data/sample/smap_sample.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fixture not found at {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse_records(self, raw_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parses daily volumetric soil moisture records."""
        upazila_id = raw_payload.get("upazila_id", "BD-50-20-30")
        raw_records = raw_payload.get("records", [])
        records = []
        for r in raw_records:
            # Average AM and PM passes if available
            am_val = r.get("soil_moisture_am_m3_m3")
            pm_val = r.get("soil_moisture_pm_m3_m3")
            valid_vals = [v for v in [am_val, pm_val] if v is not None and v > 0]
            mean_sm = sum(valid_vals) / len(valid_vals) if valid_vals else None

            rec = {
                "upazila_id": upazila_id,
                "date": r.get("date"),
                "soil_moisture_am": am_val,
                "soil_moisture_pm": pm_val,
                "soil_moisture_mean_m3_m3": mean_sm,
                "quality_flag": r.get("retrieval_qual_flag", 0),
                "source_id": self.source_id,
            }
            records.append(rec)
        return records
