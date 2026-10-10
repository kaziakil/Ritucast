"""Response schemas for system data freshness, methodology provenance, and scientific safeguards."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class DatasetProvenanceItem(BaseModel):
    """Provenance entry for an ingested environmental dataset."""
    dataset_id: str = Field(..., description="Dataset identifier (e.g. DATA-MET-01)")
    dataset_name: str = Field(..., description="Dataset formal title")
    source_agency: str = Field(..., description="Provider agency (NASA, BMD, ECMWF, BWDB)")
    spatial_coverage: str = Field(..., description="Coverage scope")
    temporal_resolution: str = Field(..., description="Time interval")
    latency_hours: float = Field(..., description="Update latency in hours")
    latest_record_bst: str = Field(..., description="Latest available record in BST")
    license: str = Field(..., description="Data usage license")
    status: str = Field(..., description="Operational status (ACTIVE, NOMINAL)")


class ModelMethodologyItem(BaseModel):
    """Methodology documentation item."""
    method_id: str = Field(..., description="Equation or rule ID (e.g. EQN-ET0-01)")
    title: str = Field(..., description="Method title")
    reference_standard: str = Field(..., description="Scientific standard (e.g. FAO-56 Paper No. 56)")
    calibration_status: str = Field(..., description="Regional calibration status")


class SystemProvenanceResponse(BaseModel):
    """Complete system provenance and freshness envelope."""
    model_config = ConfigDict(protected_namespaces=())

    system_name: str = Field(default="Ritucast Agricultural Intelligence Platform")
    version: str = Field(default="1.0.0-phase10")
    generated_at_bst: str = Field(..., description="Report generation timestamp")
    pilot_regions: List[str] = Field(..., description="Active geographic testbeds")
    datasets: List[DatasetProvenanceItem] = Field(..., description="Ingested dataset status")
    scientific_methodologies: List[ModelMethodologyItem] = Field(..., description="Scientific equations and rules")
    scientific_boundaries: Dict[str, str] = Field(..., description="Scope boundaries and non-goals (DEC-06)")
