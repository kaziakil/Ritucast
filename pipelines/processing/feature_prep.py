"""
Feature Preparation & Parquet Serialization for Phase 9 Analytics.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import pandas as pd
from pipelines.common.models import PublishedArtifact

logger = logging.getLogger("ritucast.processing.feature_prep")

class FeaturePreparer:
    """Transforms validated datasets into standardized columnar Parquet tables."""

    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def prepare_meteorology_daily(
        self,
        records: List[Dict[str, Any]],
        filename: str = "meteorology_daily_upazila.parquet",
    ) -> PublishedArtifact:
        """Serializes validated daily agrometeorology table."""
        filepath = os.path.join(self.output_dir, filename)
        df = pd.DataFrame(records)

        # Standard column order
        cols = [
            "upazila_id",
            "date",
            "t2m_c",
            "t2m_max_c",
            "t2m_min_c",
            "solar_rad_mj_m2",
            "rh2m_pct",
            "wind_speed_2m_ms",
            "precipitation_mm",
            "source_id",
        ]
        existing_cols = [c for c in cols if c in df.columns]
        df = df[existing_cols]

        df.to_parquet(filepath, index=False, engine="pyarrow", compression="snappy")
        logger.info(f"Published {len(df)} rows to {filepath}")

        from pipelines.common.provenance import ProvenanceManager
        checksum = ProvenanceManager.compute_file_sha256(filepath)

        return PublishedArtifact(
            file_name=filename,
            file_path=filepath,
            rows_count=len(df),
            columns_count=len(df.columns),
            sha256_checksum=checksum,
        )

    def prepare_forecast_hourly(
        self,
        records: List[Dict[str, Any]],
        filename: str = "forecast_hourly_pilot.parquet",
    ) -> PublishedArtifact:
        """Serializes validated hourly forecast table."""
        filepath = os.path.join(self.output_dir, filename)
        df = pd.DataFrame(records)

        cols = [
            "upazila_id",
            "valid_time_utc",
            "horizon_hours",
            "temp_2m_c",
            "rh_2m_pct",
            "rain_prob_pct",
            "rain_amount_mm",
            "wind_speed_kmh",
            "model_name",
            "source_id",
        ]
        existing_cols = [c for c in cols if c in df.columns]
        df = df[existing_cols]

        df.to_parquet(filepath, index=False, engine="pyarrow", compression="snappy")
        logger.info(f"Published {len(df)} rows to {filepath}")

        from pipelines.common.provenance import ProvenanceManager
        checksum = ProvenanceManager.compute_file_sha256(filepath)

        return PublishedArtifact(
            file_name=filename,
            file_path=filepath,
            rows_count=len(df),
            columns_count=len(df.columns),
            sha256_checksum=checksum,
        )

    def prepare_catchment_rainfall(
        self,
        records: List[Dict[str, Any]],
        filename: str = "catchment_rainfall_daily.parquet",
    ) -> PublishedArtifact:
        """Serializes validated transboundary catchment rainfall table."""
        filepath = os.path.join(self.output_dir, filename)
        df = pd.DataFrame(records)

        cols = [
            "catchment_id",
            "date",
            "precipitation_mm",
            "rain_24h_mm",
            "rain_cum_48h_mm",
            "rain_cum_7d_mm",
            "quality_flag",
            "source_id",
        ]
        existing_cols = [c for c in cols if c in df.columns]
        df = df[existing_cols]

        df.to_parquet(filepath, index=False, engine="pyarrow", compression="snappy")
        logger.info(f"Published {len(df)} rows to {filepath}")

        from pipelines.common.provenance import ProvenanceManager
        checksum = ProvenanceManager.compute_file_sha256(filepath)

        return PublishedArtifact(
            file_name=filename,
            file_path=filepath,
            rows_count=len(df),
            columns_count=len(df.columns),
            sha256_checksum=checksum,
        )

    def prepare_hydrology_river_stage(
        self,
        records: List[Dict[str, Any]],
        filename: str = "hydrology_river_stage.parquet",
    ) -> PublishedArtifact:
        """Serializes validated river water level records."""
        filepath = os.path.join(self.output_dir, filename)
        df = pd.DataFrame(records)

        cols = [
            "station_id",
            "timestamp_utc",
            "water_level_m_pwd",
            "danger_level_m_pwd",
            "freeboard_m",
            "rate_of_rise_24h_m",
            "is_above_danger",
            "source_id",
        ]
        existing_cols = [c for c in cols if c in df.columns]
        df = df[existing_cols]

        df.to_parquet(filepath, index=False, engine="pyarrow", compression="snappy")
        logger.info(f"Published {len(df)} rows to {filepath}")

        from pipelines.common.provenance import ProvenanceManager
        checksum = ProvenanceManager.compute_file_sha256(filepath)

        return PublishedArtifact(
            file_name=filename,
            file_path=filepath,
            rows_count=len(df),
            columns_count=len(df.columns),
            sha256_checksum=checksum,
        )
