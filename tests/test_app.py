"""API-level tests for the FastAPI endpoint."""

from __future__ import annotations

import httpx
import pytest
import respx
from fastapi.testclient import TestClient

from src.app import app
from src.config import get_settings


@pytest.fixture
def client(settings):
    get_settings.cache_clear()
    with TestClient(app) as test_client:
        # Inject test settings into app state (lifespan also loads real settings;
        # override after startup for isolation).
        test_client.app.state.settings = settings
        yield test_client
    get_settings.cache_clear()


def test_missing_postcode(client) -> None:
    response = client.get("/nearest-grit-bin", params={"address": "HILLBROW"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "missing_parameter"


def test_missing_address(client) -> None:
    response = client.get("/nearest-grit-bin", params={"postcode": "DE55 5PB"})
    assert response.status_code == 400


@respx.mock
def test_nearest_grit_bin_happy_path(client, settings) -> None:
    client.app.state.settings = settings

    respx.get(
        "https://example.com/DerbyshireApplicationsWebService/api/Address/DE55%205PB"
    ).mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "Title": "HILLBROW, ALFRETON, DE55 5PB",
                    "Easting": 443609,
                    "Northing": 351791,
                }
            ],
        )
    )
    respx.get("https://wms.example.com/geoserver/DCC/ows").mock(
        return_value=httpx.Response(
            200,
            json={
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "id": "Gritbins.1",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [443620.0, 351800.0],
                        },
                        "properties": {"Title": "GB-TEST-001"},
                    }
                ],
            },
        )
    )

    response = client.get(
        "/nearest-grit-bin",
        params={"postcode": "DE55 5PB", "address": "HILLBROW"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["address"] == "HILLBROW"
    assert body["postcode"] == "DE55 5PB"
    assert body["nearest_grit_bin_title"] == "GB-TEST-001"
    assert "distance_meters" in body


def test_health(client) -> None:
    assert client.get("/health").json() == {"status": "ok"}
