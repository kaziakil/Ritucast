"""Structured JSON Logging & Sensitive Data Scrubbing for Ritucast."""

import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict
from contextvars import ContextVar

# ContextVar for async request correlation ID propagation
correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id", default="system")

# Sensitive key patterns to scrub
SENSITIVE_PATTERNS = re.compile(
    r"(password|token|secret|authorization|api[-_]?key|bearer|credentials|private)",
    re.IGNORECASE,
)


def scrub_sensitive_value(key: str, value: Any) -> Any:
    """Mask sensitive string values if their key matches sensitive patterns."""
    if SENSITIVE_PATTERNS.search(key):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {k: scrub_sensitive_value(k, v) for k, v in value.items()}
    if isinstance(value, list):
        return [scrub_sensitive_value(key, v) for v in value]
    return value


class StructuredJsonFormatter(logging.Formatter):
    """Custom logging formatter that outputs newline-delimited structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_payload: Dict[str, Any] = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", correlation_id_ctx.get()),
        }

        # Include optional metadata if present
        for attr in ["duration_ms", "http_status", "method", "path", "client_ip"]:
            if hasattr(record, attr):
                log_payload[attr] = getattr(record, attr)

        # Include traceback if an exception occurred
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_payload, ensure_ascii=False)


def get_structured_logger(name: str = "ritucast") -> logging.Logger:
    """Retrieve or configure a structured logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredJsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
