"""Common API response envelopes, error schemas, and health models."""

from typing import Generic, TypeVar, Optional, Any, Dict, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standardized top-level API response envelope."""
    model_config = ConfigDict(protected_namespaces=())

    status: str = Field(default="success", description="Status code ('success' or 'error')")
    data: Optional[T] = Field(default=None, description="Response payload")
    error: Optional[Dict[str, Any]] = Field(default=None, description="Error detail if status is error")
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 generation timestamp",
    )


class ErrorResponse(BaseModel):
    """Standardized error envelope."""
    model_config = ConfigDict(protected_namespaces=())

    status: str = Field(default="error", description="Error status string")
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error description")
    details: Optional[Any] = Field(default=None, description="Optional diagnostic details")
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 error timestamp",
    )


class HealthResponse(BaseModel):
    """Liveness probe response."""
    model_config = ConfigDict(protected_namespaces=())

    status: str = Field(default="healthy", description="Service liveness state")
    version: str = Field(..., description="API semantic version")
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Current server timestamp",
    )


class ReadinessResponse(BaseModel):
    """Readiness probe response checking data tables and analytics dependencies."""
    model_config = ConfigDict(protected_namespaces=())

    status: str = Field(default="ready", description="Service readiness state ('ready' or 'unready')")
    data_store_ready: bool = Field(..., description="True if required Phase 8 processed tables exist")
    analytics_ready: bool = Field(..., description="True if analytics engine is initialized")
    verified_datasets: List[str] = Field(default_factory=list, description="List of verified Parquet tables")
    missing_dependencies: List[str] = Field(default_factory=list, description="Missing prerequisites, if any")
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Readiness verification timestamp",
    )


class DeepHealthResponse(BaseModel):
    """Detailed production diagnostic probe response."""
    model_config = ConfigDict(protected_namespaces=())

    status: str = Field(..., description="Overall service status ('healthy', 'degraded', 'unhealthy')")
    version: str = Field(..., description="Application semantic version")
    uptime_seconds: float = Field(..., description="Uptime in seconds since process start")
    system_metrics: Dict[str, Any] = Field(..., description="Resource utilization metrics (RSS memory MB, etc.)")
    components: Dict[str, Any] = Field(..., description="Subsystem readiness and component breakdown")
    pipeline_health: Dict[str, Any] = Field(..., description="Data pipeline freshness and circuit-breaker status")
    governance: Dict[str, str] = Field(..., description="Status of active governance and safety frameworks")
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Evaluation timestamp",
    )
