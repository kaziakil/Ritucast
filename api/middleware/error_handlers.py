"""Standardized exception handlers returning uniform error response payloads."""

import logging
from datetime import datetime, timezone
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from analytics.engine.context_gate import ContextGatingError

logger = logging.getLogger("ritucast.api")


def register_error_handlers(app: FastAPI) -> None:
    """Register custom exception handlers on the FastAPI application."""

    @app.exception_handler(ContextGatingError)
    async def context_gating_exception_handler(request: Request, exc: ContextGatingError):
        """Handle DEC-17 contextual gating violations (missing or invalid Upazila, crop, or stage)."""
        logger.warning(f"Context gating rejection on {request.url.path}: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": "CONTEXT_GATING_FAILED",
                "message": str(exc),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "details": {
                    "rule": "DEC-17",
                    "path": request.url.path,
                },
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic request parameter and body schema validation errors."""
        errors = exc.errors()
        logger.info(f"Request validation failure on {request.url.path}: {errors}")
        first_error = errors[0] if errors else {}
        loc = " -> ".join([str(x) for x in first_error.get("loc", [])])
        msg = first_error.get("msg", "Invalid request parameter.")

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": "REQUEST_VALIDATION_ERROR",
                "message": f"Validation failed for field '{loc}': {msg}",
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "details": errors,
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle standard HTTP exceptions with consistent error envelope."""
        logger.warning(f"HTTP {exc.status_code} on {request.url.path}: {exc.detail}")
        code_map = {
            400: "BAD_REQUEST_PARAMETER",
            404: "RESOURCE_NOT_FOUND",
            413: "PAYLOAD_TOO_LARGE",
            422: "UNPROCESSABLE_ENTITY",
            429: "RATE_LIMIT_EXCEEDED",
            500: "INTERNAL_SERVER_ERROR",
        }
        code = code_map.get(exc.status_code, f"HTTP_{exc.status_code}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "code": code,
                "message": str(exc.detail),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "details": None,
            },
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle invalid argument values."""
        logger.warning(f"Bad request value on {request.url.path}: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "error",
                "code": "BAD_REQUEST_PARAMETER",
                "message": str(exc),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "details": None,
            },
        )

    @app.exception_handler(KeyError)
    async def key_error_handler(request: Request, exc: KeyError):
        """Handle missing resource identifiers."""
        logger.warning(f"Resource not found on {request.url.path}: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "error",
                "code": "RESOURCE_NOT_FOUND",
                "message": f"Resource not found: {str(exc)}",
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "details": None,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Sanitize unexpected internal exceptions to prevent leaking server details or secrets."""
        logger.error(f"Unhandled server error on {request.url.path}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred while processing the agricultural request.",
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "details": None,
            },
        )
