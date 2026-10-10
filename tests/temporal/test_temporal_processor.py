"""
Temporal Processing and Rolling Window Unit Tests.
"""

from datetime import datetime
from pipelines.processing.temporal import TemporalProcessor

def test_utc_to_bst_conversion():
    utc_dt = datetime(2026, 3, 1, 0, 0, 0)
    bst_dt = TemporalProcessor.utc_to_bst(utc_dt)
    assert bst_dt.hour == 6
    assert bst_dt.day == 1

def test_bst_to_utc_conversion():
    bst_dt = datetime(2026, 3, 1, 6, 0, 0)
    utc_dt = TemporalProcessor.bst_to_utc(bst_dt)
    assert utc_dt.hour == 0

def test_rolling_rainfall_calculation():
    records = [
        {"date": "2026-03-01", "precipitation_mm": 10.0},
        {"date": "2026-03-02", "precipitation_mm": 20.0},
        {"date": "2026-03-03", "precipitation_mm": 30.0},
        {"date": "2026-03-04", "precipitation_mm": 5.0},
    ]
    res = TemporalProcessor.compute_rolling_rainfall(records)
    # On 2026-03-01: 24h = 10, 48h = 10
    assert res[0]["rain_24h_mm"] == 10.0
    assert res[0]["rain_cum_48h_mm"] == 10.0

    # On 2026-03-02: 24h = 20, 48h = 10 + 20 = 30
    assert res[1]["rain_24h_mm"] == 20.0
    assert res[1]["rain_cum_48h_mm"] == 30.0

    # On 2026-03-03: 24h = 30, 48h = 20 + 30 = 50, 7d = 10 + 20 + 30 = 60
    assert res[2]["rain_cum_48h_mm"] == 50.0
    assert res[2]["rain_cum_7d_mm"] == 60.0

def test_growing_degree_days():
    # Base 10°C, Cap 35°C
    # Tmax = 30, Tmin = 20 -> Mean = 25 -> GDD = 15
    gdd1 = TemporalProcessor.compute_daily_gdd(t_max=30.0, t_min=20.0)
    assert gdd1 == 15.0

    # Cold day: Tmax = 12, Tmin = 6 -> Mean = 9 -> GDD = 0
    gdd2 = TemporalProcessor.compute_daily_gdd(t_max=12.0, t_min=6.0)
    assert gdd2 == 0.0

    # Hot day: Tmax = 42 (capped at 35), Tmin = 25 -> Mean = 30 -> GDD = 20
    gdd3 = TemporalProcessor.compute_daily_gdd(t_max=42.0, t_min=25.0)
    assert gdd3 == 20.0

def test_find_missing_dates():
    dates = ["2026-03-01", "2026-03-02", "2026-03-04"]
    missing = TemporalProcessor.find_missing_dates(dates, "2026-03-01", "2026-03-04")
    assert missing == ["2026-03-03"]
