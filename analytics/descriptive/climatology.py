"""Descriptive agroclimatology calculator for Upazila-level time series."""

from typing import Dict, List, Optional
import pandas as pd
import numpy as np

from analytics.contracts.indicator_schemas import DescriptiveAgroclimaticSummary


class ClimatologyAggregator:
    """Computes descriptive statistical summaries of meteorological variables over time."""

    @staticmethod
    def summarize_period(
        df_met: pd.DataFrame,
        upazila_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> DescriptiveAgroclimaticSummary:
        """Compute verified agroclimatic aggregates over a date range.

        Args:
            df_met: DataFrame conforming to Phase 8 meteorology_daily_upazila schema.
            upazila_id: Target Upazila identifier.
            start_date: Optional YYYY-MM-DD filter start.
            end_date: Optional YYYY-MM-DD filter end.

        Returns:
            DescriptiveAgroclimaticSummary Pydantic model.
        """
        subset = df_met[df_met["upazila_id"] == upazila_id].copy()
        if subset.empty:
            raise ValueError(f"No meteorological records found for upazila {upazila_id}")

        subset["date"] = pd.to_datetime(subset["date"])
        if start_date:
            subset = subset[subset["date"] >= pd.to_datetime(start_date)]
        if end_date:
            subset = subset[subset["date"] <= pd.to_datetime(end_date)]

        if subset.empty:
            raise ValueError(f"No records available in specified window {start_date} to {end_date}")

        subset = subset.sort_values("date")
        actual_days = len(subset)
        date_span = (subset["date"].max() - subset["date"].min()).days + 1
        completeness = min(100.0, (actual_days / max(1, date_span)) * 100.0)

        mean_t2m = float(subset["t2m_c"].mean()) if "t2m_c" in subset else float(
            (subset["t2m_max_c"].mean() + subset["t2m_min_c"].mean()) / 2.0
        )
        max_t2m = float(subset["t2m_max_c"].max())
        min_t2m = float(subset["t2m_min_c"].min())
        cum_pcp = float(subset["precipitation_mm"].sum())
        mean_srad = float(subset["solar_rad_mj_m2"].mean())
        mean_rh = float(subset["rh2m_pct"].mean())

        return DescriptiveAgroclimaticSummary(
            upazila_id=upazila_id,
            start_date=subset["date"].min().strftime("%Y-%m-%d"),
            end_date=subset["date"].max().strftime("%Y-%m-%d"),
            days_count=actual_days,
            mean_t2m_c=round(mean_t2m, 2),
            max_t2m_c=round(max_t2m, 2),
            min_t2m_c=round(min_t2m, 2),
            cumulative_precipitation_mm=round(cum_pcp, 2),
            mean_solar_rad_mj_m2=round(mean_srad, 2),
            mean_rh2m_pct=round(mean_rh, 1),
            completeness_pct=round(completeness, 1),
        )
