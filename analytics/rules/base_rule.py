"""Base class for deterministic, evidence-supported agricultural rules."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from analytics.contracts.advisory_schemas import (
    AdvisoryCard,
    AdvisorySeverity,
    AdvisoryStatus,
    ContextGatePayload,
)


class BaseAgriculturalRule(ABC):
    """Abstract base class establishing the governance and execution interface for rules."""

    RULE_ID: str
    RULE_NAME: str
    CLASSIFICATION: str  # "Evidence-Supported", "Context-Dependent"

    @abstractmethod
    def evaluate(
        self,
        context: ContextGatePayload,
        inputs: Dict[str, Any],
        timestamp_utc: str,
    ) -> Optional[AdvisoryCard]:
        """Evaluate rule conditions against physical indicators and generate advisory card if triggered."""
        pass
