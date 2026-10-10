"""Middleware package initialization."""

from api.middleware.error_handlers import register_error_handlers

__all__ = ["register_error_handlers"]
