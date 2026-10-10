"""
BWDB FFWC River Stage Gauge Logs Ingestion Adapter (DATA-HYD-01).
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from pipelines.common.base_adapter import BaseAdapter

logger = logging.getLogger("ritucast.ingestion.hydrology")

class BwdbHydrologyAdapter(BaseAdapter):
    """Ingests observed river water levels from Bangladesh Water Development Board (BWDB) FFWC."""

    def __init__(self, timeout_seconds: int = 20):
        super().__init__(
            source_id="DATA-HYD-01",
            name="BWDB FFWC River Stage Gauge Logs",
            timeout_seconds=timeout_seconds,
        )

    def fetch_live(self, station_id: str) -> Dict[str, Any]:
        """Placeholder for live FFWC bulletin scraping or web API fetch."""
        logger.info(f"Querying FFWC gauge observations for {station_id}")
        return self.load_sample()

    def load_sample(self, fixture_path: Optional[str] = None) -> Dict[str, Any]:
        """Loads sample synthetic gauge observations from disk."""
        path = fixture_path or "data/sample/bwdb_gauge_sample.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fixture not found at {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse_records(self, raw_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parses river water level time series and computes rate of rise."""
        station_id = raw_payload.get("station_id", "BWDB-177")
        danger_level = float(raw_payload.get("danger_level_m_pwd", 8.25))
        readings = raw_payload.get("readings", [])

        records = []
        prev_wl = None

        for r in readings:
            curr_wl = float(r.get("water_level_m_pwd", 0.0))
            freeboard = danger_level - curr_wl
            rate_of_rise = (curr_wl - prev_wl) if prev_wl is not None else 0.0
            prev_wl = curr_wl

            rec = {
                "station_id": station_id,
                "timestamp_utc": r.get("timestamp_utc"),
                "water_level_m_pwd": curr_wl,
                "danger_level_m_pwd": danger_level,
                "freeboard_m": round(freeboard, 2),
                "rate_of_rise_24h_m": round(rate_of_rise, 2),
                "is_above_danger": curr_wl >= danger_level,
                "source_id": self.source_id,
            }
            records.append(rec)

        return records
