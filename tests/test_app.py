"""API-level tests for the FastAPI endpoint."""

from __future__ import annotations

import httpx
import pytest
import respx

from src.config import get_settings


def test_missing_postcode(client) -> None:
    response = client.get("/api/v1/nearest-grit-bin", params={"address": "Example Building"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "missing_parameter"


def test_missing_address(client) -> None:
    response = client.get("/api/v1/nearest-grit-bin", params={"postcode": "AB12 3CD"})
    assert response.status_code == 400


def test_invalid_postcode_format(client) -> None:
    response = client.get(
        "/api/v1/nearest-grit-bin",
        params={"postcode": "DE55 5PB4", "address": "Example Building"},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "invalid_postcode"


@respx.mock
def test_nearest_grit_bin_happy_path(client, settings) -> None:
    client.app.state.settings = settings

    respx.get(
        "https://example.com/DerbyshireApplicationsWebService/api/Address/AB12%203CD"
    ).mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "Title": "Example Building, ALFRETON, AB12 3CD",
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
        "/api/v1/nearest-grit-bin",
        params={"postcode": "AB12 3CD", "address": "Example Building"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["address"] == "Example Building"
    assert body["postcode"] == "AB12 3CD"
    assert body["nearest_grit_bin_title"] == "GB-TEST-001"
    assert "distance_meters" in body


@respx.mock
def test_nearest_grit_bins_limit(client, settings) -> None:
    client.app.state.settings = settings

    respx.get(
        "https://example.com/DerbyshireApplicationsWebService/api/Address/AB12%203CD"
    ).mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "Title": "Example Building, ALFRETON, AB12 3CD",
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
                        "properties": {"Title": "GB-NEAR"},
                    },
                    {
                        "type": "Feature",
                        "id": "Gritbins.2",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [443650.0, 351820.0],
                        },
                        "properties": {"Title": "GB-MID"},
                    },
                    {
                        "type": "Feature",
                        "id": "Gritbins.3",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [450000.0, 360000.0],
                        },
                        "properties": {"Title": "GB-FAR"},
                    },
                ],
            },
        )
    )

    response = client.get(
        "/api/v1/nearest-grit-bins",
        params={"postcode": "AB12 3CD", "address": "Example Building", "limit": 2},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["address"] == "Example Building"
    assert [b["title"] for b in body["nearest_grit_bins"]] == ["GB-NEAR", "GB-MID"]


@respx.mock
def test_list_grit_bins(client, settings) -> None:
    client.app.state.settings = settings
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
                        "properties": {"Title": "GB-A"},
                    },
                    {
                        "type": "Feature",
                        "id": "Gritbins.2",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [450000.0, 360000.0],
                        },
                        "properties": {"Title": "GB-B"},
                    },
                ],
            },
        )
    )

    response = client.get("/api/v1/grit-bins")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert {b["title"] for b in body["grit_bins"]} == {"GB-A", "GB-B"}


def test_health(client) -> None:
    assert client.get("/api/v1/health").json() == {"status": "ok"}


@respx.mock
def test_list_addresses_happy_path(client, settings) -> None:
    client.app.state.settings = settings

    respx.get(
        "https://example.com/DerbyshireApplicationsWebService/api/Address/AB12%203CD"
    ).mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "UPRN": "200004519931",
                    "Title": "Example Building, ALFRETON, AB12 3CD",
                    "BuildingName": "Example Building",
                    "BuildingNumber": None,
                    "ThoroughFareName": "High Street",
                    "PostTown": "ALFRETON",
                    "PostCode": "AB12 3CD",
                    "SpatialFeature": {
                        "Eastings": 443609,
                        "Northings": 351791,
                    },
                },
                {
                    "UPRN": "2",
                    "Title": "Other Place, ALFRETON, AB12 3CD",
                    "BuildingName": "Other Place",
                    "ThoroughFareName": "Low Street",
                    "PostTown": "ALFRETON",
                    "PostCode": "AB12 3CD",
                    "SpatialFeature": {
                        "Eastings": 443700,
                        "Northings": 351800,
                    },
                },
            ],
        )
    )

    response = client.get("/api/v1/addresses", params={"postcode": "AB12 3CD"})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert body["addresses"][0]["title"] == "Example Building, ALFRETON, AB12 3CD"
    assert body["addresses"][0]["easting"] == 443609.0
    assert body["addresses"][0]["northing"] == 351791.0
    assert body["addresses"][0]["uprn"] == "200004519931"
    assert body["addresses"][0]["thoroughfare"] == "High Street"


@respx.mock
def test_list_addresses_optional_filter(client, settings) -> None:
    client.app.state.settings = settings

    respx.get(
        "https://example.com/DerbyshireApplicationsWebService/api/Address/AB12%203CD"
    ).mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "Title": "Example Building, ALFRETON, AB12 3CD",
                    "BuildingName": "Example Building",
                    "PostCode": "AB12 3CD",
                    "SpatialFeature": {"Eastings": 443609, "Northings": 351791},
                },
                {
                    "Title": "Other Place, ALFRETON, AB12 3CD",
                    "BuildingName": "Other Place",
                    "PostCode": "AB12 3CD",
                    "SpatialFeature": {"Eastings": 443700, "Northings": 351800},
                },
            ],
        )
    )

    response = client.get(
        "/api/v1/addresses",
        params={"postcode": "AB12 3CD", "address": "Example Building"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["addresses"][0]["building_name"] == "Example Building"


def test_list_addresses_missing_postcode(client) -> None:
    response = client.get("/api/v1/addresses")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "missing_parameter"
