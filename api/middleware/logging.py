"""Structured Logging & Correlation ID Middleware for FastAPI."""

import time
import uuid
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from api.logging_config import correlation_id_ctx, get_structured_logger

logger = get_structured_logger("ritucast.api.access")


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Intercepts requests to track correlation IDs, record duration, and log JSON summaries."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Extract or generate correlation ID
        incoming_cid = request.headers.get("X-Correlation-ID") or request.headers.get("X-Request-ID")
        correlation_id = incoming_cid if incoming_cid else f"req_{uuid.uuid4().hex[:12]}"

        # Bind to contextvar for downstream logger invocations
        token = correlation_id_ctx.set(correlation_id)

        start_time = time.perf_counter()
        client_ip = request.client.host if request.client else "unknown"

        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

            # Invert correlation ID into response headers
            response.headers["X-Correlation-ID"] = correlation_id

            # Skip health probes from info log flooding to prevent log bloat
            if request.url.path not in ("/health", "/api/v1/health"):
                logger.info(
                    f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)",
                    extra={
                        "correlation_id": correlation_id,
                        "method": request.method,
                        "path": request.url.path,
                        "http_status": response.status_code,
                        "duration_ms": duration_ms,
                        "client_ip": client_ip,
                    },
                )
            return response

        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
            logger.error(
                f"Unhandled error processing {request.method} {request.url.path}: {exc}",
                exc_info=True,
                extra={
                    "correlation_id": correlation_id,
                    "method": request.method,
                    "path": request.url.path,
                    "http_status": 500,
                    "duration_ms": duration_ms,
                    "client_ip": client_ip,
                },
            )
            raise exc
        finally:
            correlation_id_ctx.reset(token)
