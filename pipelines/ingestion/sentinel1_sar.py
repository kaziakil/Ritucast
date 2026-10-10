"""
Copernicus Sentinel-1 C-Band SAR Ingestion Adapter (DATA-SAR-01).
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from pipelines.common.base_adapter import BaseAdapter
from pipelines.common.rate_limiter import RateLimiter

logger = logging.getLogger("ritucast.ingestion.sentinel1_sar")

class Sentinel1SarAdapter(BaseAdapter):
    """Ingests Sentinel-1 C-band SAR GRD metadata and water coverage from ESA CDSE."""

    CDSE_ODATA_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"

    def __init__(
        self,
        rate_limiter: Optional[RateLimiter] = None,
        timeout_seconds: int = 30,
        max_retries: int = 3,
    ):
        limiter = rate_limiter or RateLimiter(requests_per_minute=60)
        super().__init__(
            source_id="DATA-SAR-01",
            name="Copernicus Sentinel-1 C-Band SAR GRD",
            rate_limiter=limiter,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
        )

    def fetch_live(
        self,
        polygon_wkt: str,
        start_date: str,
        end_date: str,
    ) -> Dict[str, Any]:
        """Queries CDSE OData API for Sentinel-1 GRD IW products intersecting target geometry."""
        filter_query = (
            f"Collection/Name eq 'SENTINEL-1' and "
            f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'GRD') and "
            f"ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T23:59:59.000Z and "
            f"OData.CSC.Intersects(area=geography'SRID=4326;{polygon_wkt}')"
        )
        query_params = {
            "$filter": filter_query,
            "$top": 10,
            "$orderby": "ContentDate/Start desc",
        }
        logger.info(f"Querying CDSE for Sentinel-1 products")
        return self._execute_http_get(self.CDSE_ODATA_URL, params=query_params)

    def load_sample(self, fixture_path: Optional[str] = None) -> Dict[str, Any]:
        """Loads sample synthetic Sentinel-1 metadata payload from disk."""
        path = fixture_path or "data/sample/sentinel1_metadata_sample.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fixture not found at {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse_metadata_records(self, raw_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parses product metadata records."""
        products = raw_payload.get("products", [])
        records = []
        for p in products:
            rec = {
                "product_id": p.get("id"),
                "sensing_time_utc": p.get("sensing_time_utc"),
                "polarization": p.get("polarization", "VV+VH"),
                "water_extent_pct": float(p.get("water_extent_pct", 0.0)),
                "mean_backscatter_vv_db": float(p.get("mean_backscatter_vv_db", -15.0)),
                "coverage_upazilas": p.get("coverage_upazilas", []),
                "source_id": self.source_id,
            }
            records.append(rec)
        return records
