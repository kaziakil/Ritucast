"""
Spatial Processing and Zonal Geometry Operations in EPSG:4326.
"""

from typing import List, Dict, Any, Optional, Tuple
from shapely.geometry import Point, Polygon, shape, box
from pipelines.common.exceptions import SpatialProcessingError

BANGLADESH_BBOX = {
    "min_lon": 88.0,
    "min_lat": 20.5,
    "max_lon": 92.8,
    "max_lat": 26.7,
}

MEGHALAYA_CATCHMENT_BBOX = {
    "min_lon": 90.0,
    "min_lat": 25.0,
    "max_lon": 92.8,
    "max_lat": 26.2,
}

class SpatialProcessor:
    """Handles spatial domain validation, coordinate clipping, and polygon aggregations."""

    @staticmethod
    def is_within_bangladesh(longitude: float, latitude: float) -> bool:
        """Verifies if coordinate falls inside Bangladesh geographic bounding box."""
        return (
            BANGLADESH_BBOX["min_lon"] <= longitude <= BANGLADESH_BBOX["max_lon"]
            and BANGLADESH_BBOX["min_lat"] <= latitude <= BANGLADESH_BBOX["max_lat"]
        )

    @staticmethod
    def is_within_meghalaya_catchment(longitude: float, latitude: float) -> bool:
        """Verifies if coordinate falls inside Meghalaya upstream transboundary catchment."""
        return (
            MEGHALAYA_CATCHMENT_BBOX["min_lon"] <= longitude <= MEGHALAYA_CATCHMENT_BBOX["max_lon"]
            and MEGHALAYA_CATCHMENT_BBOX["min_lat"] <= latitude <= MEGHALAYA_CATCHMENT_BBOX["max_lat"]
        )

    @staticmethod
    def calculate_polygon_centroid(coords: List[List[float]]) -> Tuple[float, float]:
        """Calculates (longitude, latitude) centroid for a closed ring of coordinates."""
        try:
            poly = Polygon(coords)
            c = poly.centroid
            return (round(c.x, 4), round(c.y, 4))
        except Exception as err:
            raise SpatialProcessingError(f"Failed to calculate centroid: {err}") from err

    @staticmethod
    def aggregate_points_to_polygon(
        points: List[Dict[str, Any]],
        polygon_geom: Polygon,
        value_field: str,
    ) -> Optional[float]:
        """Computes mean value of points that fall within polygon geometry."""
        matching_values = []
        for pt in points:
            lon = pt.get("longitude")
            lat = pt.get("latitude")
            val = pt.get(value_field)
            if lon is not None and lat is not None and val is not None:
                p_geom = Point(lon, lat)
                if polygon_geom.contains(p_geom):
                    matching_values.append(val)

        if not matching_values:
            return None
        return sum(matching_values) / len(matching_values)
