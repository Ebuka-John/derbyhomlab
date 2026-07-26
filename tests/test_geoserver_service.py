"""Unit tests for GeoServerService."""

from __future__ import annotations

import httpx
import pytest
import respx

from src.services.geoserver_service import (
    GeoServerService,
    nearest_from_features,
)
from src.utils.coordinates import Point27700
from src.utils.errors import (
    GeoServerUnreachableError,
    NoGritBinNearbyError,
)


ORIGIN = Point27700(easting=443609.0, northing=351791.0)

NEAR_FEATURE = {
    "type": "Feature",
    "id": "Gritbins.1",
    "geometry": {"type": "Point", "coordinates": [443620.0, 351800.0]},
    "geometry_name": "SP_GEOMETRY",
    "properties": {"Title": "GB-NEAR", "Subtitle": "Near street"},
}

FAR_FEATURE = {
    "type": "Feature",
    "id": "Gritbins.2",
    "geometry": {"type": "Point", "coordinates": [450000.0, 360000.0]},
    "geometry_name": "SP_GEOMETRY",
    "properties": {"Title": "GB-FAR"},
}


def test_nearest_from_features_selects_closest() -> None:
    match = nearest_from_features(
        [FAR_FEATURE, NEAR_FEATURE], ORIGIN, radius_meters=100
    )
    assert match.title == "GB-NEAR"
    assert match.distance_meters < 20


def test_nearest_from_features_none_in_radius() -> None:
    with pytest.raises(NoGritBinNearbyError):
        nearest_from_features([FAR_FEATURE], ORIGIN, radius_meters=100)


@pytest.mark.asyncio
@respx.mock
async def test_dwithin_success(settings) -> None:
    route = respx.get("https://wms.example.com/geoserver/DCC/ows").mock(
        return_value=httpx.Response(
            200,
            json={"type": "FeatureCollection", "features": [NEAR_FEATURE]},
        )
    )

    async with GeoServerService(settings) as svc:
        match = await svc.find_nearest(ORIGIN, radius_meters=100)

    assert match.title == "GB-NEAR"
    assert route.called
    # Confirm DWITHIN CQL was issued
    params = str(route.calls.last.request.url)
    assert "DWITHIN" in params
    assert "SP_GEOMETRY" in params


@pytest.mark.asyncio
@respx.mock
async def test_dwithin_fallback_to_euclidean(settings) -> None:
    """When DWITHIN returns an OGC exception, fall back to full fetch."""
    calls = {"n": 0}

    def side_effect(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if "DWITHIN" in str(request.url):
            return httpx.Response(
                200,
                content=b'<?xml version="1.0"?><ServiceExceptionReport/>',
                headers={"content-type": "application/xml"},
            )
        return httpx.Response(
            200,
            json={"type": "FeatureCollection", "features": [NEAR_FEATURE, FAR_FEATURE]},
        )

    respx.get("https://wms.example.com/geoserver/DCC/ows").mock(side_effect=side_effect)

    async with GeoServerService(settings) as svc:
        match = await svc.find_nearest(ORIGIN, radius_meters=100)

    assert match.title == "GB-NEAR"
    assert calls["n"] >= 2


@pytest.mark.asyncio
@respx.mock
async def test_geoserver_unreachable(settings) -> None:
    respx.get("https://wms.example.com/geoserver/DCC/ows").mock(
        side_effect=httpx.ConnectError("down")
    )

    async with GeoServerService(settings) as svc:
        with pytest.raises(GeoServerUnreachableError):
            await svc.find_nearest(ORIGIN)


@pytest.mark.asyncio
@respx.mock
async def test_no_bin_within_radius(settings) -> None:
    respx.get("https://wms.example.com/geoserver/DCC/ows").mock(
        return_value=httpx.Response(
            200,
            json={"type": "FeatureCollection", "features": [FAR_FEATURE]},
        )
    )

    async with GeoServerService(settings) as svc:
        with pytest.raises(NoGritBinNearbyError):
            await svc.find_nearest(ORIGIN, radius_meters=100)
