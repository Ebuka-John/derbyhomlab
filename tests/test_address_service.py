"""Unit tests for AddressService."""

from __future__ import annotations

import httpx
import pytest
import respx

from src.services.address_service import AddressService, find_matching_address
from src.utils.exceptions import (
    AddressApiUnreachableError,
    AddressNotFoundError,
    TargetAddressNotFoundError,
    UnexpectedSchemaError,
)

SAMPLE_ADDRESSES = [
    {
        "Title": "1 SOME STREET, ALFRETON, DE55 5PB",
        "Easting": 443000,
        "Northing": 351000,
    },
    {
        "Title": "HILLBROW, ALFRETON, DE55 5PB",
        "Easting": 443610,
        "Northing": 351790,
    },
]


def test_find_matching_address_case_insensitive() -> None:
    resolved = find_matching_address(
        SAMPLE_ADDRESSES, address="hillbrow", postcode="DE55 5PB"
    )
    assert "HILLBROW" in resolved.title.upper()
    assert resolved.point.easting == 443610.0


def test_find_matching_address_not_found() -> None:
    with pytest.raises(TargetAddressNotFoundError):
        find_matching_address(
            SAMPLE_ADDRESSES, address="DOES-NOT-EXIST", postcode="DE55 5PB"
        )


def test_find_matching_address_lat_lon_conversion() -> None:
    records = [
        {
            "Title": "HILLBROW COTTAGE",
            "Latitude": 53.062,
            "Longitude": -1.355,
        }
    ]
    resolved = find_matching_address(records, address="HILLBROW", postcode="DE55 5PB")
    assert 400_000 < resolved.point.easting < 500_000


def test_unwrap_rejects_bad_schema() -> None:
    with pytest.raises(UnexpectedSchemaError):
        find_matching_address(
            [{"Title": "X"}],
            address="X",
            postcode="DE55 5PB",
        )


@pytest.mark.asyncio
@respx.mock
async def test_lookup_postcode_success(settings) -> None:
    route = respx.get(
        "https://example.com/DerbyshireApplicationsWebService/api/Address/DE55%205PB"
    ).mock(return_value=httpx.Response(200, json=SAMPLE_ADDRESSES))

    async with AddressService(settings) as svc:
        records = await svc.lookup_postcode("DE55 5PB")

    assert route.called
    assert len(records) == 2
    request = route.calls.last.request
    assert request.headers["x-alias"] == "test-alias"
    assert request.headers["x-auth-token"] == "test-token"


@pytest.mark.asyncio
@respx.mock
async def test_lookup_postcode_empty(settings) -> None:
    respx.get(
        "https://example.com/DerbyshireApplicationsWebService/api/Address/DE55%205PB"
    ).mock(return_value=httpx.Response(200, json=[]))

    async with AddressService(settings) as svc:
        with pytest.raises(AddressNotFoundError):
            await svc.lookup_postcode("DE55 5PB")


@pytest.mark.asyncio
@respx.mock
async def test_lookup_postcode_unreachable(settings) -> None:
    respx.get(
        "https://example.com/DerbyshireApplicationsWebService/api/Address/DE55%205PB"
    ).mock(side_effect=httpx.ConnectError("connection refused"))

    async with AddressService(settings) as svc:
        with pytest.raises(AddressApiUnreachableError):
            await svc.lookup_postcode("DE55 5PB")


@pytest.mark.asyncio
@respx.mock
async def test_resolve_address_end_to_end(settings) -> None:
    respx.get(
        "https://example.com/DerbyshireApplicationsWebService/api/Address/DE55%205PB"
    ).mock(return_value=httpx.Response(200, json={"results": SAMPLE_ADDRESSES}))

    async with AddressService(settings) as svc:
        resolved = await svc.resolve_address(postcode="DE55 5PB", address="HILLBROW")

    assert resolved.point.northing == 351790.0


def test_find_matching_derbyshire_live_schema() -> None:
    records = [
        {
            "UPRN": "200004519931",
            "BuildingName": "HILLBROW",
            "ThoroughFareName": "ALFRETON ROAD",
            "PostTown": "ALFRETON",
            "DependentLocality": "TIBSHELF",
            "PostCode": "DE55 5PB",
            "SpatialFeature": {
                "Eastings": 443563,
                "Northings": 360212,
                "Longitude": -1.3502759,
                "Latitude": 53.1373085,
            },
        }
    ]
    resolved = find_matching_address(records, address="HILLBROW", postcode="DE55 5PB")
    assert resolved.point.easting == 443563.0
    assert resolved.point.northing == 360212.0
    assert "HILLBROW" in resolved.title.upper()
