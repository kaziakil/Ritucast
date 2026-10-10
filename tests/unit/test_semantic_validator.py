"""
Unit tests for SemanticValidator and physical boundary checks.
"""

from pipelines.validation.semantic_validator import SemanticValidator

def test_meteorology_physical_bounds_success():
    rec = {
        "t2m_c": 28.5,
        "t2m_max_c": 34.0,
        "t2m_min_c": 22.0,
        "solar_rad_mj_m2": 22.5,
        "rh2m_pct": 65.0,
        "wind_speed_2m_ms": 3.2,
        "precipitation_mm": 12.4,
    }
    ok, errors = SemanticValidator.validate_meteorology(rec)
    assert ok is True
    assert len(errors) == 0

def test_meteorology_extreme_temperature_rejected():
    rec = {
        "t2m_c": 62.0,  # Exceeds 55°C limit
        "t2m_max_c": 65.0,
        "t2m_min_c": 20.0,
        "solar_rad_mj_m2": 20.0,
    }
    ok, errors = SemanticValidator.validate_meteorology(rec)
    assert ok is False
    assert any("out of physical bounds" in e for e in errors)

def test_meteorology_negative_rain_rejected():
    rec = {
        "t2m_c": 25.0,
        "precipitation_mm": -10.0,  # Negative rain
    }
    ok, errors = SemanticValidator.validate_meteorology(rec)
    assert ok is False
    assert any("precipitation_mm" in e for e in errors)

def test_forecast_rain_probability_out_of_bounds():
    rec = {
        "temp_2m_c": 28.0,
        "rain_prob_pct": 140.0,  # Exceeds 100%
        "rain_amount_mm": 5.0,
    }
    ok, errors = SemanticValidator.validate_forecast(rec)
    assert ok is False
    assert any("rain_prob_pct" in e for e in errors)

def test_soil_moisture_impossible_saturation():
    rec = {
        "soil_moisture_mean_m3_m3": 0.85,  # Soil porosity max ~0.60
    }
    ok, errors = SemanticValidator.validate_soil_moisture(rec)
    assert ok is False
    assert any("soil_moisture" in e for e in errors)
