"""Shared fixtures for API integration tests."""

import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.data_access.repository import AgriculturalDataRepository
from api.dependencies import get_repository


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Session-scoped TestClient instance."""
    return TestClient(app)


@pytest.fixture(scope="session")
def repo() -> AgriculturalDataRepository:
    """Session-scoped repository instance."""
    return get_repository()
