"""Unit tests for coordinate conversion and distance helpers."""

import math

import pytest

from src.utils.coordinates import (
    Point27700,
    bng_to_lonlat,
    detect_crs_from_values,
    ensure_bng,
    euclidean_distance_meters,
    lonlat_to_bng,
)
from src.utils.errors import CoordinateConversionError


def test_lonlat_to_bng_roundtrip_approx() -> None:
    # Known-ish London point; round-trip should be within a metre
    lon, lat = -0.1278, 51.5074
    bng = lonlat_to_bng(lon, lat)
    back = bng_to_lonlat(bng.easting, bng.northing)
    assert abs(back.longitude - lon) < 1e-5
    assert abs(back.latitude - lat) < 1e-5


def test_ensure_bng_prefers_easting_northing() -> None:
    point = ensure_bng(easting=443609.0, northing=351791.0, latitude=53.0, longitude=-1.4)
    assert point.easting == 443609.0
    assert point.northing == 351791.0


def test_ensure_bng_converts_lat_lon() -> None:
    point = ensure_bng(latitude=53.062, longitude=-1.355)
    assert 400_000 < point.easting < 500_000
    assert 300_000 < point.northing < 400_000


def test_ensure_bng_missing_coords() -> None:
    with pytest.raises(CoordinateConversionError):
        ensure_bng()


def test_euclidean_distance() -> None:
    a = Point27700(0.0, 0.0)
    b = Point27700(3.0, 4.0)
    assert euclidean_distance_meters(a, b) == pytest.approx(5.0)


def test_detect_crs() -> None:
    assert detect_crs_from_values(-1.35, 53.06) == "EPSG:4326"
    assert detect_crs_from_values(443609.0, 351791.0) == "EPSG:27700"
    with pytest.raises(CoordinateConversionError):
        detect_crs_from_values(9_999_999.0, 9_999_999.0)


def test_distance_is_symmetric() -> None:
    a = Point27700(443609.6, 351791.4)
    b = Point27700(443679.8, 351760.8)
    assert math.isclose(
        euclidean_distance_meters(a, b),
        euclidean_distance_meters(b, a),
    )
