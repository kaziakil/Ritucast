"""
Ritucast Master Pipeline Orchestrator & CLI Runner.
"""

import argparse
import json
import logging
import os
import sys
from typing import List, Dict, Any

from pipelines.common.models import DatasetIngestSummary, PublishedArtifact
from pipelines.common.provenance import ProvenanceManager
from pipelines.ingestion.nasa_power import NasaPowerAdapter
from pipelines.ingestion.open_meteo import OpenMeteoAdapter
from pipelines.ingestion.gpm_imerg import GpmImergAdapter
from pipelines.ingestion.sentinel1_sar import Sentinel1SarAdapter
from pipelines.ingestion.smap_soil_moisture import SmapSoilMoistureAdapter
from pipelines.ingestion.administrative import AdministrativeBoundaryLoader
from pipelines.ingestion.agronomic_reference import AgronomicReferenceLoader
from pipelines.ingestion.hydrology_ffwc import BwdbHydrologyAdapter
from pipelines.validation.schema_validator import (
    validate_record,
    MeteorologyDailySchema,
    ForecastHourlySchema,
    CatchmentRainfallSchema,
    Sentinel1MetadataSchema,
    SoilMoistureDailySchema,
    HydrologyReadingSchema,
)
from pipelines.validation.semantic_validator import SemanticValidator
from pipelines.validation.quality_reporter import QualityReporter
from pipelines.processing.spatial import SpatialProcessor
from pipelines.processing.temporal import TemporalProcessor
from pipelines.processing.feature_prep import FeaturePreparer

logger = logging.getLogger("ritucast.orchestrator")

def setup_logging(level: str = "INFO"):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

class PipelineOrchestrator:
    """Coordinates ingestion, validation, processing, feature prep, and provenance."""

    def __init__(
        self,
        output_dir: str = "data/processed",
        use_sample: bool = True,
        dry_run: bool = False,
    ):
        self.output_dir = output_dir
        self.use_sample = use_sample
        self.dry_run = dry_run
        self.reporter = QualityReporter()
        self.provenance = ProvenanceManager(output_dir=os.path.join(output_dir, "manifests"))
        self.feature_prep = FeaturePreparer(output_dir=output_dir)

    def run(
        self,
        datasets: List[str],
        upazila_scope: str = "pilot",
        start_date: str = "2026-03-01",
        end_date: str = "2026-03-05",
    ) -> Dict[str, Any]:
        """Executes selected pipeline stages."""
        logger.info(f"Starting Ritucast Pipeline (use_sample={self.use_sample}, dry_run={self.dry_run})")
        datasets_summary: List[DatasetIngestSummary] = []
        published_artifacts: List[PublishedArtifact] = []

        # 1. Load Pilot Zones
        pilot_zones_path = "configs/datasets/pilot_zones.json"
        if os.path.exists(pilot_zones_path):
            with open(pilot_zones_path, "r", encoding="utf-8") as f:
                pilot_cfg = json.load(f)
            pilot_list = pilot_cfg.get("pilot_zones", [])
        else:
            pilot_list = [
                {"upazila_id": "BD-50-20-30", "upazila_name": "Godagari", "centroid": {"longitude": 88.33, "latitude": 24.47}},
                {"upazila_id": "BD-60-90-86", "upazila_name": "Sunamganj Sadar", "centroid": {"longitude": 91.40, "latitude": 25.07}},
            ]

        # Target pilot upazilas
        if upazila_scope == "pilot":
            target_upazilas = pilot_list
        else:
            target_upazilas = [p for p in pilot_list if p.get("upazila_id") == upazila_scope]
            if not target_upazilas:
                target_upazilas = [{"upazila_id": upazila_scope, "centroid": {"longitude": 88.33, "latitude": 24.47}}]

        # 2. Ingest & Validate NASA POWER
        if "nasa_power" in datasets or "all" in datasets:
            logger.info("Executing NASA POWER Agrometeorology stage...")
            adapter = NasaPowerAdapter()
            raw_payload = adapter.load_sample() if self.use_sample else adapter.fetch_live(88.33, 24.47, start_date, end_date)
            sha = adapter.compute_sha256(raw_payload)

            all_records = []
            for u in target_upazilas:
                recs = adapter.parse_records(raw_payload, u["upazila_id"])
                all_records.extend(recs)

            valid_recs, rej_recs, errors = [], [], []
            for r in all_records:
                try:
                    validate_record(MeteorologyDailySchema, r)
                    ok, s_errs = SemanticValidator.validate_meteorology(r)
                    if ok:
                        valid_recs.append(r)
                    else:
                        rej_recs.append(r)
                        errors.extend(s_errs)
                except Exception as err:
                    rej_recs.append(r)
                    errors.append(str(err))

            self.reporter.record_outcome("NASA POWER", len(all_records), len(valid_recs), len(rej_recs), errors=errors)
            datasets_summary.append(
                DatasetIngestSummary(
                    source_id="DATA-MET-01",
                    provider="NASA POWER",
                    collection="daily/point/AG",
                    endpoint=adapter.BASE_URL,
                    raw_records_count=len(all_records),
                    valid_records_count=len(valid_recs),
                    rejected_records_count=len(rej_recs),
                    sha256_checksum=sha,
                )
            )

            if valid_recs and not self.dry_run:
                artifact = self.feature_prep.prepare_meteorology_daily(valid_recs)
                published_artifacts.append(artifact)

        # 3. Ingest & Validate Open-Meteo
        if "open_meteo" in datasets or "all" in datasets:
            logger.info("Executing Open-Meteo NWP Forecast stage...")
            om_adapter = OpenMeteoAdapter()
            om_payload = om_adapter.load_sample() if self.use_sample else om_adapter.fetch_live(91.40, 25.07)
            om_sha = om_adapter.compute_sha256(om_payload)

            om_hourly = []
            for u in target_upazilas:
                h_recs = om_adapter.parse_hourly_records(om_payload, u["upazila_id"])
                om_hourly.extend(h_recs)

            valid_om, rej_om, om_errors = [], [], []
            for r in om_hourly:
                try:
                    validate_record(ForecastHourlySchema, r)
                    ok, s_errs = SemanticValidator.validate_forecast(r)
                    if ok:
                        valid_om.append(r)
                    else:
                        rej_om.append(r)
                        om_errors.extend(s_errs)
                except Exception as err:
                    rej_om.append(r)
                    om_errors.append(str(err))

            self.reporter.record_outcome("Open-Meteo", len(om_hourly), len(valid_om), len(rej_om), errors=om_errors)
            datasets_summary.append(
                DatasetIngestSummary(
                    source_id="DATA-FCST-01",
                    provider="Open-Meteo",
                    collection="forecast/ecmwf_ifs025",
                    endpoint=om_adapter.BASE_URL,
                    raw_records_count=len(om_hourly),
                    valid_records_count=len(valid_om),
                    rejected_records_count=len(rej_om),
                    sha256_checksum=om_sha,
                )
            )

            if valid_om and not self.dry_run:
                om_artifact = self.feature_prep.prepare_forecast_hourly(valid_om)
                published_artifacts.append(om_artifact)

        # 4. Ingest & Validate GPM IMERG
        if "gpm_imerg" in datasets or "all" in datasets:
            logger.info("Executing GPM IMERG Transboundary Rainfall stage...")
            gpm_adapter = GpmImergAdapter()
            gpm_payload = gpm_adapter.load_sample()
            gpm_sha = gpm_adapter.compute_sha256(gpm_payload)
            gpm_recs = gpm_adapter.parse_catchment_records(gpm_payload)

            valid_gpm, rej_gpm, gpm_errors = [], [], []
            for r in gpm_recs:
                try:
                    validate_record(CatchmentRainfallSchema, r)
                    ok, s_errs = SemanticValidator.validate_catchment_rain(r)
                    if ok:
                        valid_gpm.append(r)
                    else:
                        rej_gpm.append(r)
                        gpm_errors.extend(s_errs)
                except Exception as err:
                    rej_gpm.append(r)
                    gpm_errors.append(str(err))

            # Temporal processing: rolling rainfall windows
            if valid_gpm:
                valid_gpm = TemporalProcessor.compute_rolling_rainfall(valid_gpm)

            self.reporter.record_outcome("GPM IMERG", len(gpm_recs), len(valid_gpm), len(rej_gpm), errors=gpm_errors)
            datasets_summary.append(
                DatasetIngestSummary(
                    source_id="DATA-PCP-01",
                    provider="NASA GES DISC",
                    collection="GPM_3IMERGDF_07",
                    endpoint=gpm_adapter.CMR_SEARCH_URL,
                    raw_records_count=len(gpm_recs),
                    valid_records_count=len(valid_gpm),
                    rejected_records_count=len(rej_gpm),
                    sha256_checksum=gpm_sha,
                )
            )

            if valid_gpm and not self.dry_run:
                gpm_artifact = self.feature_prep.prepare_catchment_rainfall(valid_gpm)
                published_artifacts.append(gpm_artifact)

        # 5. Ingest & Validate BWDB River Gauges
        if "bwdb" in datasets or "all" in datasets:
            logger.info("Executing BWDB FFWC River Stage stage...")
            bwdb_adapter = BwdbHydrologyAdapter()
            bwdb_payload = bwdb_adapter.load_sample()
            bwdb_sha = bwdb_adapter.compute_sha256(bwdb_payload)
            bwdb_recs = bwdb_adapter.parse_records(bwdb_payload)

            valid_bwdb, rej_bwdb, bwdb_errors = [], [], []
            for r in bwdb_recs:
                try:
                    validate_record(HydrologyReadingSchema, r)
                    ok, s_errs = SemanticValidator.validate_hydrology(r)
                    if ok:
                        valid_bwdb.append(r)
                    else:
                        rej_bwdb.append(r)
                        bwdb_errors.extend(s_errs)
                except Exception as err:
                    rej_bwdb.append(r)
                    bwdb_errors.append(str(err))

            self.reporter.record_outcome("BWDB Hydrology", len(bwdb_recs), len(valid_bwdb), len(rej_bwdb), errors=bwdb_errors)
            datasets_summary.append(
                DatasetIngestSummary(
                    source_id="DATA-HYD-01",
                    provider="BWDB FFWC",
                    collection="river_stage_bulletins",
                    endpoint="https://ffwc.gov.bd",
                    raw_records_count=len(bwdb_recs),
                    valid_records_count=len(valid_bwdb),
                    rejected_records_count=len(rej_bwdb),
                    sha256_checksum=bwdb_sha,
                )
            )

            if valid_bwdb and not self.dry_run:
                bwdb_artifact = self.feature_prep.prepare_hydrology_river_stage(valid_bwdb)
                published_artifacts.append(bwdb_artifact)

        # Quality Report & Provenance Manifest Generation
        q_summary = self.reporter.get_summary()
        logger.info(f"Pipeline Execution Complete. Quality Status: {q_summary.status} (Checked: {q_summary.total_records_checked}, Passed: {q_summary.passed_count})")

        manifest = None
        if not self.dry_run:
            manifest = self.provenance.create_manifest(
                parameters={
                    "datasets": datasets,
                    "upazila_scope": upazila_scope,
                    "start_date": start_date,
                    "end_date": end_date,
                    "use_sample": self.use_sample,
                },
                datasets_ingested=datasets_summary,
                published_artifacts=published_artifacts,
                quality_summary=q_summary,
            )
            # Write quality report json
            q_report_path = os.path.join(self.output_dir, "quality_report.json")
            self.reporter.write_json_report(q_report_path)

        return {
            "status": q_summary.status,
            "quality_summary": q_summary.model_dump(),
            "published_artifacts": [a.model_dump() for a in published_artifacts],
            "manifest_run_id": manifest.run_id if manifest else None,
        }

def main():
    parser = argparse.ArgumentParser(description="Ritucast Data Ingestion & Processing Pipeline CLI")
    parser.add_argument("--dataset", default="all", help="Dataset to ingest (nasa_power, open_meteo, gpm_imerg, bwdb, all)")
    parser.add_argument("--upazila", default="pilot", help="Upazila scope ('pilot' or specific ID)")
    parser.add_argument("--start-date", default="2026-03-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", default="2026-03-05", help="End date (YYYY-MM-DD)")
    parser.add_argument("--use-sample", action="store_true", default=True, help="Use local sample fixtures")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Dry run validation only")
    parser.add_argument("--output-dir", default="data/processed", help="Output directory")
    parser.add_argument("--log-level", default="INFO", help="Logging level")

    args = parser.parse_args()
    setup_logging(args.log_level)

    orchestrator = PipelineOrchestrator(
        output_dir=args.output_dir,
        use_sample=args.use_sample,
        dry_run=args.dry_run,
    )

    datasets = [args.dataset] if args.dataset != "all" else ["all"]
    result = orchestrator.run(
        datasets=datasets,
        upazila_scope=args.upazila,
        start_date=args.start_date,
        end_date=args.end_date,
    )

    print(json.dumps(result, indent=2))
    if result["status"] == "FAIL":
        sys.exit(1)

if __name__ == "__main__":
    main()
