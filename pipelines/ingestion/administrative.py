"""
Bangladesh Administrative Boundaries GeoJSON Loader (DATA-BND-01).
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional
from shapely.geometry import shape, Point

logger = logging.getLogger("ritucast.ingestion.administrative")

class AdministrativeBoundaryLoader:
    """Loads and indexes official Bangladesh administrative polygons in EPSG:4326."""

    def __init__(self, geojson_path: Optional[str] = None):
        self.geojson_path = geojson_path or "data/sample/bangladesh_pilot_upazilas.geojson"
        self._features_by_id: Dict[str, Dict[str, Any]] = {}
        self._geometries_by_id: Dict[str, Any] = {}
        self._load()

    def _load(self):
        """Loads and parses GeoJSON into in-memory spatial index."""
        if not os.path.exists(self.geojson_path):
            raise FileNotFoundError(f"Administrative GeoJSON not found at {self.geojson_path}")

        with open(self.geojson_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        features = data.get("features", [])
        for feat in features:
            props = feat.get("properties", {})
            u_id = props.get("upazila_id")
            if u_id:
                self._features_by_id[u_id] = props
                geom_dict = feat.get("geometry")
                if geom_dict:
                    self._geometries_by_id[u_id] = shape(geom_dict)

        logger.info(f"Loaded {len(self._features_by_id)} Upazilas from {self.geojson_path}")

    def get_upazila_ids(self) -> List[str]:
        """Returns all loaded Upazila IDs."""
        return list(self._features_by_id.keys())

    def get_properties(self, upazila_id: str) -> Optional[Dict[str, Any]]:
        """Returns metadata properties for an Upazila."""
        return self._features_by_id.get(upazila_id)

    def get_geometry(self, upazila_id: str) -> Optional[Any]:
        """Returns Shapely geometry for an Upazila."""
        return self._geometries_by_id.get(upazila_id)

    def get_centroid(self, upazila_id: str) -> Optional[Dict[str, float]]:
        """Returns centroid (longitude, latitude) of an Upazila polygon."""
        geom = self.get_geometry(upazila_id)
        if geom:
            centroid = geom.centroid
            return {"longitude": centroid.x, "latitude": centroid.y}
        return None

    def find_upazila_containing(self, longitude: float, latitude: float) -> Optional[str]:
        """Performs point-in-polygon lookup to find matching Upazila ID."""
        pt = Point(longitude, latitude)
        for u_id, geom in self._geometries_by_id.items():
            if geom.contains(pt):
                return u_id
        return None
