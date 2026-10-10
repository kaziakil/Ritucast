"""Security middleware for Ritucast API service.

Implements defense-in-depth protections:
1. SecurityHeadersMiddleware: Injects OWASP-recommended HTTP security headers.
2. RequestSizeLimitMiddleware: Enforces maximum payload size limits to mitigate DoS / memory exhaustion.
3. RateLimitMiddleware: Enforces sliding-window in-memory client rate limiting.
"""

import time
from typing import Dict, List, Tuple
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from api.config import get_settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Injects OWASP and security compliance HTTP headers into all API responses."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        settings = get_settings()

        # Prevent MIME-type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking / framing
        response.headers["X-Frame-Options"] = "DENY"

        # Legacy XSS protection filter
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Control referrer information leakage
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Content Security Policy preventing unauthorized frame embedding
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"

        # Restrict dangerous browser hardware capabilities
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

        # HSTS in production or when connection is HTTPS
        if settings.ENVIRONMENT == "production" or request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Enforces maximum payload size limits to mitigate resource exhaustion / DoS."""

    def __init__(self, app, max_bytes: int = 1048576):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > self.max_bytes:
                    return JSONResponse(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        content={
                            "status": "error",
                            "code": "PAYLOAD_TOO_LARGE",
                            "message": f"Request payload exceeds maximum permitted limit of {self.max_bytes} bytes.",
                            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            "details": {"max_bytes": self.max_bytes, "received_bytes": int(content_length)},
                        },
                    )
            except ValueError:
                pass

        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """In-memory sliding-window rate limiter per client IP address."""

    def __init__(self, app, requests_per_minute: int = 60, enabled: bool = True):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.enabled = enabled
        # Maps client_ip -> list of epoch timestamps
        self._history: Dict[str, List[float]] = {}
        # Health check paths exempt from rate limiting
        self.exempt_paths = {"/health", "/ready", "/health/liveness", "/health/readiness"}

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP respecting X-Forwarded-For if present."""
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        if request.client and request.client.host:
            return request.client.host
        return "127.0.0.1"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if not self.enabled or request.url.path in self.exempt_paths:
            return await call_next(request)

        client_ip = self._get_client_ip(request)
        now = time.time()
        window_start = now - 60.0

        # Filter timestamps within sliding 60-second window
        timestamps = self._history.get(client_ip, [])
        valid_timestamps = [ts for ts in timestamps if ts > window_start]

        if len(valid_timestamps) >= self.requests_per_minute:
            retry_after = int(60.0 - (now - valid_timestamps[0])) + 1
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={
                    "Retry-After": str(max(1, retry_after)),
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(valid_timestamps[0] + 60.0)),
                },
                content={
                    "status": "error",
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": f"Rate limit of {self.requests_per_minute} requests per minute exceeded.",
                    "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "details": {"retry_after_seconds": max(1, retry_after)},
                },
            )

        valid_timestamps.append(now)
        self._history[client_ip] = valid_timestamps

        response = await call_next(request)
        remaining = max(0, self.requests_per_minute - len(valid_timestamps))
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
