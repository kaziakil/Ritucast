"""
Custom exception hierarchy for Ritucast Data Pipelines.
"""

class PipelineError(Exception):
    """Base exception for all pipeline errors."""
    pass

class ConfigurationError(PipelineError):
    """Raised when pipeline or dataset configuration is invalid or missing."""
    pass

class NetworkError(PipelineError):
    """Raised when upstream API requests fail or time out."""
    pass

class RateLimitError(NetworkError):
    """Raised when upstream service returns 429 Too Many Requests."""
    pass

class SchemaValidationError(PipelineError):
    """Raised when input records violate structural Pydantic schema."""
    pass

class SemanticValidationError(PipelineError):
    """Raised when data values violate physical domain boundaries."""
    pass

class SpatialProcessingError(PipelineError):
    """Raised when geographic boundaries or coordinates fail spatial validation."""
    pass

class TemporalProcessingError(PipelineError):
    """Raised when date parsing, alignment, or time-series logic fails."""
    pass
