"""
Common Pydantic data models for configuration, manifests, and quality audit summaries.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict

class BoundingBox(BaseModel):
    min_longitude: float
    min_latitude: float
    max_longitude: float
    max_latitude: float

class PilotZoneConfig(BaseModel):
    upazila_id: str
    upazila_name: str
    upazila_name_bn: str
    district_id: str
    district_name: str
    district_name_bn: str
    division_name: str
    division_name_bn: str
    pilot_region: str
    centroid: Dict[str, float]
    bounding_box: BoundingBox
    area_sq_km: float
    primary_hazard: str
    anchor_crops: List[str]

class DatasetIngestSummary(BaseModel):
    source_id: str
    provider: str
    collection: str
    endpoint: str
    raw_records_count: int
    valid_records_count: int
    rejected_records_count: int
    sha256_checksum: str

class PublishedArtifact(BaseModel):
    file_name: str
    file_path: str
    rows_count: int
    columns_count: int
    sha256_checksum: str

class QualityAuditSummary(BaseModel):
    total_records_checked: int
    passed_count: int
    rejected_count: int
    warnings_count: int
    status: str

class RunManifest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_url: str = Field(default="https://ritucast.org/schemas/v1/run-manifest.json", alias="$schema")
    run_id: str
    pipeline_version: str
    git_commit: str
    execution_timestamp_utc: str
    target_domain: str
    parameters: Dict[str, Any]
    datasets_ingested: List[DatasetIngestSummary]
    published_artifacts: List[PublishedArtifact]
    quality_report_summary: QualityAuditSummary
