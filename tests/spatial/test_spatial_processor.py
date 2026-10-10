"""
Spatial Processing and Bounding Box Unit Tests.
"""

from pipelines.processing.spatial import SpatialProcessor
from pipelines.ingestion.administrative import AdministrativeBoundaryLoader

def test_within_bangladesh_bounds():
    # Inside Rajshahi
    assert SpatialProcessor.is_within_bangladesh(88.33, 24.47) is True
    # Inside Sunamganj
    assert SpatialProcessor.is_within_bangladesh(91.40, 25.07) is True
    # Outside in Bay of Bengal
    assert SpatialProcessor.is_within_bangladesh(90.0, 18.0) is False
    # Outside in Nepal
    assert SpatialProcessor.is_within_bangladesh(85.0, 27.5) is False

def test_meghalaya_catchment_bounds():
    # Cherrapunji / Meghalaya hills
    assert SpatialProcessor.is_within_meghalaya_catchment(91.7, 25.3) is True
    # Southern Bangladesh
    assert SpatialProcessor.is_within_meghalaya_catchment(90.0, 22.0) is False

def test_polygon_centroid_calculation():
    # Simple 1x1 degree box
    coords = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]
    lon, lat = SpatialProcessor.calculate_polygon_centroid(coords)
    assert lon == 0.5
    assert lat == 0.5

def test_administrative_boundary_loader():
    loader = AdministrativeBoundaryLoader("data/sample/bangladesh_pilot_upazilas.geojson")
    upazilas = loader.get_upazila_ids()
    assert "BD-50-20-30" in upazilas  # Godagari
    assert "BD-60-90-86" in upazilas  # Sunamganj Sadar

    # Centroid check
    c = loader.get_centroid("BD-50-20-30")
    assert c is not None
    assert 88.0 <= c["longitude"] <= 89.0
    assert 24.0 <= c["latitude"] <= 25.0

    # Point in polygon
    u_match = loader.find_upazila_containing(88.30, 24.50)
    assert u_match == "BD-50-20-30"
