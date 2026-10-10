"""
Data Provenance and Run Manifest Generation.
"""

import datetime
import hashlib
import json
import os
import subprocess
import uuid
from typing import Any, Dict, List, Optional

from pipelines.common.models import (
    DatasetIngestSummary,
    PublishedArtifact,
    QualityAuditSummary,
    RunManifest,
)

class ProvenanceManager:
    """Manages execution manifests and cryptographic audit trails."""

    def __init__(self, output_dir: str = "data/processed/manifests"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def get_git_commit() -> str:
        """Retrieves current Git commit hash or fallback string."""
        try:
            res = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            return res.stdout.strip()
        except Exception:
            return "git-unavailable"

    @staticmethod
    def compute_file_sha256(filepath: str) -> str:
        """Calculates SHA-256 hash of a file on disk."""
        if not os.path.exists(filepath):
            return "file-not-found"
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    def create_manifest(
        self,
        parameters: Dict[str, Any],
        datasets_ingested: List[DatasetIngestSummary],
        published_artifacts: List[PublishedArtifact],
        quality_summary: QualityAuditSummary,
        pipeline_version: str = "0.8.0",
        target_domain: str = "Bangladesh Dual-Zone Pilot",
    ) -> RunManifest:
        """Creates and saves a validated RunManifest."""
        run_id = str(uuid.uuid4())
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        git_commit = self.get_git_commit()

        manifest = RunManifest(
            run_id=run_id,
            pipeline_version=pipeline_version,
            git_commit=git_commit,
            execution_timestamp_utc=now_utc,
            target_domain=target_domain,
            parameters=parameters,
            datasets_ingested=datasets_ingested,
            published_artifacts=published_artifacts,
            quality_report_summary=quality_summary,
        )

        manifest_path = os.path.join(self.output_dir, f"manifest_{run_id}.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest.model_dump(by_alias=True), f, indent=2)

        return manifest
