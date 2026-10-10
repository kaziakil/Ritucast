"""
Pytest configuration and shared fixtures for Ritucast tests.
"""

import json
import os
import pytest

@pytest.fixture
def sample_nasa_power():
    path = "data/sample/nasa_power_sample.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def sample_open_meteo():
    path = "data/sample/open_meteo_sample.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def sample_gpm_imerg():
    path = "data/sample/gpm_imerg_sample.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def sample_bwdb_gauge():
    path = "data/sample/bwdb_gauge_sample.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def sample_upazilas_geojson():
    path = "data/sample/bangladesh_pilot_upazilas.geojson"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def sample_brri_phenology():
    path = "data/sample/brri_phenology_boro.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
