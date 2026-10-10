"""
Integration Tests for End-to-End Pipeline Orchestration.
"""

import os
import shutil
import tempfile
import pandas as pd
from pipelines.orchestrator import PipelineOrchestrator

def test_pipeline_orchestrator_e2e_run():
    # Use temporary directory for testing outputs
    test_out_dir = tempfile.mkdtemp(prefix="ritucast_test_")

    try:
        orchestrator = PipelineOrchestrator(
            output_dir=test_out_dir,
            use_sample=True,
            dry_run=False,
        )

        result = orchestrator.run(
            datasets=["all"],
            upazila_scope="pilot",
            start_date="2026-03-01",
            end_date="2026-03-05",
        )

        assert result["status"] == "PASS"
        assert result["manifest_run_id"] is not None

        # Verify Parquet files exist
        met_file = os.path.join(test_out_dir, "meteorology_daily_upazila.parquet")
        assert os.path.exists(met_file)
        df_met = pd.read_parquet(met_file)
        assert len(df_met) > 0
        assert "t2m_max_c" in df_met.columns

        fcst_file = os.path.join(test_out_dir, "forecast_hourly_pilot.parquet")
        assert os.path.exists(fcst_file)
        df_fcst = pd.read_parquet(fcst_file)
        assert len(df_fcst) > 0
        assert "rain_prob_pct" in df_fcst.columns

        rain_file = os.path.join(test_out_dir, "catchment_rainfall_daily.parquet")
        assert os.path.exists(rain_file)
        df_rain = pd.read_parquet(rain_file)
        assert len(df_rain) > 0
        assert "rain_cum_48h_mm" in df_rain.columns

        hyd_file = os.path.join(test_out_dir, "hydrology_river_stage.parquet")
        assert os.path.exists(hyd_file)
        df_hyd = pd.read_parquet(hyd_file)
        assert len(df_hyd) > 0

        # Verify manifest was written
        manifests_dir = os.path.join(test_out_dir, "manifests")
        assert os.path.exists(manifests_dir)
        manifest_files = [f for f in os.listdir(manifests_dir) if f.endswith(".json")]
        assert len(manifest_files) == 1

        # Verify quality report
        q_rep = os.path.join(test_out_dir, "quality_report.json")
        assert os.path.exists(q_rep)

    finally:
        shutil.rmtree(test_out_dir, ignore_errors=True)
