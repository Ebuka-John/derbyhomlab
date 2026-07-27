"""Shared pytest fixtures."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.config import Settings, get_settings


@pytest.fixture
def settings(monkeypatch: pytest.MonkeyPatch) -> Settings:
    """Deterministic settings for unit tests — no real .env required."""
    monkeypatch.setenv(
        "ADDRESS_API_BASE_URL",
        "https://example.com/DerbyshireApplicationsWebService/api/Address",
    )
    monkeypatch.setenv("ADDRESS_API_ALIAS", "test-alias")
    monkeypatch.setenv("ADDRESS_API_AUTH_TOKEN", "test-token")
    monkeypatch.setenv("GEOSERVER_BASE_URL", "https://wms.example.com/geoserver")
    monkeypatch.setenv("GEOSERVER_LAYER", "DCC:Gritbins")
    monkeypatch.setenv("NEAREST_SEARCH_RADIUS_METERS", "100")
    monkeypatch.setenv("HTTP_TIMEOUT_SECONDS", "5")

    get_settings.cache_clear()
    return Settings()


@pytest.fixture
def client(settings):
    get_settings.cache_clear()
    with TestClient(app) as test_client:
        test_client.app.state.settings = settings
        yield test_client
    get_settings.cache_clear()
