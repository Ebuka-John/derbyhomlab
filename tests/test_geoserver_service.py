"""Unit tests for GritBinService."""

from __future__ import annotations

import httpx
import pytest
import respx

from src.models.domain.geometry import Point27700
from src.services.gritbin_service import GritBinService
from src.utils.exceptions import GeoServerUnreachableError, NoGritBinNearbyError
from src.utils.geospatial import nearest_from_features, nearest_n_from_features

ORIGIN = Point27700(easting=443609.0, northing=351791.0)

NEAR_FEATURE = {
    "type": "Feature",
    "id": "Gritbins.1",
    "geometry": {"type": "Point", "coordinates": [443620.0, 351800.0]},
    "geometry_name": "SP_GEOMETRY",
    "properties": {"Title": "GB-NEAR", "Subtitle": "Near street"},
}

MID_FEATURE = {
    "type": "Feature",
    "id": "Gritbins.3",
    "geometry": {"type": "Point", "coordinates": [443650.0, 351820.0]},
    "geometry_name": "SP_GEOMETRY",
    "properties": {"Title": "GB-MID"},
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


def test_nearest_n_from_features_sorts_and_limits() -> None:
    matches = nearest_n_from_features(
        [FAR_FEATURE, MID_FEATURE, NEAR_FEATURE],
        ORIGIN,
        radius_meters=100,
        limit=2,
    )
    assert [m.title for m in matches] == ["GB-NEAR", "GB-MID"]
    assert matches[0].distance_meters < matches[1].distance_meters


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

    async with GritBinService(settings) as svc:
        match = await svc.find_nearest(ORIGIN, radius_meters=100)

    assert match.title == "GB-NEAR"
    assert route.called
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

    async with GritBinService(settings) as svc:
        match = await svc.find_nearest(ORIGIN, radius_meters=100)

    assert match.title == "GB-NEAR"
    assert calls["n"] >= 2


@pytest.mark.asyncio
@respx.mock
async def test_geoserver_unreachable(settings) -> None:
    respx.get("https://wms.example.com/geoserver/DCC/ows").mock(
        side_effect=httpx.ConnectError("down")
    )

    async with GritBinService(settings) as svc:
        with pytest.raises(GeoServerUnreachableError):
            await svc.find_nearest(ORIGIN)


@pytest.mark.asyncio
@respx.mock
async def test_find_nearest_n(settings) -> None:
    respx.get("https://wms.example.com/geoserver/DCC/ows").mock(
        return_value=httpx.Response(
            200,
            json={
                "type": "FeatureCollection",
                "features": [FAR_FEATURE, MID_FEATURE, NEAR_FEATURE],
            },
        )
    )

    async with GritBinService(settings) as svc:
        matches = await svc.find_nearest_n(ORIGIN, limit=2, radius_meters=100)

    assert [m.title for m in matches] == ["GB-NEAR", "GB-MID"]


@pytest.mark.asyncio
@respx.mock
async def test_list_all(settings) -> None:
    respx.get("https://wms.example.com/geoserver/DCC/ows").mock(
        return_value=httpx.Response(
            200,
            json={
                "type": "FeatureCollection",
                "features": [NEAR_FEATURE, FAR_FEATURE],
            },
        )
    )

    async with GritBinService(settings) as svc:
        bins = await svc.list_all()

    assert len(bins) == 2
    assert {b.title for b in bins} == {"GB-NEAR", "GB-FAR"}


@pytest.mark.asyncio
@respx.mock
async def test_no_bin_within_radius(settings) -> None:
    respx.get("https://wms.example.com/geoserver/DCC/ows").mock(
        return_value=httpx.Response(
            200,
            json={"type": "FeatureCollection", "features": [FAR_FEATURE]},
        )
    )

    async with GritBinService(settings) as svc:
        with pytest.raises(NoGritBinNearbyError):
            await svc.find_nearest(ORIGIN, radius_meters=100)
