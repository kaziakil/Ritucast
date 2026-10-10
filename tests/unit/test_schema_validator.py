"""
Unit tests for Pydantic structural schema validators.
"""

import pytest
from pipelines.common.exceptions import SchemaValidationError
from pipelines.validation.schema_validator import (
    validate_record,
    MeteorologyDailySchema,
    ForecastHourlySchema,
    CatchmentRainfallSchema,
    Sentinel1MetadataSchema,
    SoilMoistureDailySchema,
    HydrologyReadingSchema,
)

def test_meteorology_daily_valid():
    valid_rec = {
        "upazila_id": "BD-50-20-30",
        "date": "2026-03-01",
        "t2m_c": 25.4,
        "t2m_max_c": 31.8,
        "t2m_min_c": 18.2,
        "solar_rad_mj_m2": 19.85,
        "rh2m_pct": 58.4,
        "wind_speed_2m_ms": 2.1,
        "precipitation_mm": 0.0,
        "source_id": "DATA-MET-01",
    }
    obj = validate_record(MeteorologyDailySchema, valid_rec)
    assert obj.upazila_id == "BD-50-20-30"
    assert obj.t2m_max_c == 31.8

def test_meteorology_daily_tmax_less_than_tmin_fails():
    invalid_rec = {
        "upazila_id": "BD-50-20-30",
        "date": "2026-03-01",
        "t2m_max_c": 15.0,
        "t2m_min_c": 25.0,  # tmax < tmin
    }
    with pytest.raises(SchemaValidationError):
        validate_record(MeteorologyDailySchema, invalid_rec)

def test_forecast_hourly_valid():
    valid_rec = {
        "upazila_id": "BD-60-90-86",
        "valid_time_utc": "2026-03-01T06:00:00Z",
        "horizon_hours": 24,
        "temp_2m_c": 28.5,
        "rh_2m_pct": 65.0,
        "rain_prob_pct": 45.0,
        "rain_amount_mm": 2.4,
        "wind_speed_kmh": 12.0,
        "model_name": "ecmwf_ifs025",
        "source_id": "DATA-FCST-01",
    }
    obj = validate_record(ForecastHourlySchema, valid_rec)
    assert obj.horizon_hours == 24
    assert obj.model_name == "ecmwf_ifs025"

def test_catchment_rainfall_negative_fails():
    invalid_rec = {
        "catchment_id": "MEGHALAYA_ESCARP",
        "date": "2026-03-01",
        "precipitation_mm": -5.0,  # Negative rain rejected
        "quality_flag": 0,
    }
    with pytest.raises(SchemaValidationError):
        validate_record(CatchmentRainfallSchema, invalid_rec)

def test_sentinel1_metadata_valid():
    rec = {
        "product_id": "S1A_IW_GRDH_TEST",
        "sensing_time_utc": "2026-03-03T11:58:22Z",
        "polarization": "VV+VH",
        "water_extent_pct": 28.4,
        "mean_backscatter_vv_db": -16.2,
        "coverage_upazilas": ["BD-60-90-86"],
        "source_id": "DATA-SAR-01",
    }
    obj = validate_record(Sentinel1MetadataSchema, rec)
    assert obj.water_extent_pct == 28.4

def test_hydrology_reading_valid():
    rec = {
        "station_id": "BWDB-177",
        "timestamp_utc": "2026-03-01T06:00:00Z",
        "water_level_m_pwd": 7.85,
        "danger_level_m_pwd": 8.25,
        "freeboard_m": 0.40,
        "rate_of_rise_24h_m": 0.85,
        "is_above_danger": False,
        "source_id": "DATA-HYD-01",
    }
    obj = validate_record(HydrologyReadingSchema, rec)
    assert obj.is_above_danger is False
    assert obj.freeboard_m == 0.40
