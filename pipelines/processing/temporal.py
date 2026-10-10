"""
Temporal Processing, Resampling, and Rolling Climatology Windows.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
from pipelines.common.exceptions import TemporalProcessingError

class TemporalProcessor:
    """Handles temporal resampling, rolling window accumulation, and GDD calculations."""

    @staticmethod
    def utc_to_bst(dt: datetime) -> datetime:
        """Converts UTC datetime to Bangladesh Standard Time (BST, UTC+6)."""
        return dt + timedelta(hours=6)

    @staticmethod
    def bst_to_utc(dt: datetime) -> datetime:
        """Converts Bangladesh Standard Time (BST) to UTC."""
        return dt - timedelta(hours=6)

    @staticmethod
    def compute_rolling_rainfall(
        daily_records: List[Dict[str, Any]],
        date_key: str = "date",
        rain_key: str = "precipitation_mm",
    ) -> List[Dict[str, Any]]:
        """
        Sorts records by date and computes 24h, 48h, and 7-day rolling cumulative rainfall sums.
        """
        sorted_recs = sorted(daily_records, key=lambda x: x[date_key])
        n = len(sorted_recs)

        results = []
        for i in range(n):
            rec = dict(sorted_recs[i])
            curr_rain = float(rec.get(rain_key) or 0.0)

            # 24h
            rain_24h = curr_rain

            # 48h
            prev_rain = float(sorted_recs[i - 1].get(rain_key) or 0.0) if i > 0 else 0.0
            rain_48h = curr_rain + prev_rain

            # 7-day
            start_idx = max(0, i - 6)
            rain_7d = sum(float(sorted_recs[j].get(rain_key) or 0.0) for j in range(start_idx, i + 1))

            rec["rain_24h_mm"] = round(rain_24h, 2)
            rec["rain_cum_48h_mm"] = round(rain_48h, 2)
            rec["rain_cum_7d_mm"] = round(rain_7d, 2)
            results.append(rec)

        return results

    @staticmethod
    def compute_daily_gdd(
        t_max: float,
        t_min: float,
        t_base: float = 10.0,
        t_cap: float = 35.0,
    ) -> float:
        """
        Calculates daily thermal units (Growing Degree Days, GDD) for Boro rice.
        Equation: GDD = max(0, (min(t_max, t_cap) + t_min)/2 - t_base)
        """
        effective_tmax = min(t_max, t_cap)
        mean_temp = (effective_tmax + t_min) / 2.0
        gdd = max(0.0, mean_temp - t_base)
        return round(gdd, 2)

    @staticmethod
    def find_missing_dates(
        existing_dates: List[str],
        start_date: str,
        end_date: str,
    ) -> List[str]:
        """Identifies dates missing from a continuous daily sequence."""
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

        existing_set = set(existing_dates)
        missing = []
        curr = start
        while curr <= end:
            c_str = curr.strftime("%Y-%m-%d")
            if c_str not in existing_set:
                missing.append(c_str)
            curr += timedelta(days=1)

        return missing
