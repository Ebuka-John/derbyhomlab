"""Geospatial helpers: CRS conversion, planar distance, nearest-feature selection."""

from __future__ import annotations

import math
from typing import Any, Literal

from pyproj import Transformer

from src.models.domain.geometry import Point27700, Point4326
from src.models.domain.gritbin import GritBinMatch
from src.utils.exceptions import CoordinateConversionError, NoGritBinNearbyError

CrsCode = Literal["EPSG:27700", "EPSG:4326"]

# always_xy=True keeps axis order as (x, y); without it some CRS defs swap to (lat, lon).
_to_bng = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
_to_wgs84 = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)


def lonlat_to_bng(longitude: float, latitude: float) -> Point27700:
    """Convert WGS84 lon/lat (EPSG:4326) to BNG easting/northing (EPSG:27700)."""
    try:
        easting, northing = _to_bng.transform(longitude, latitude)
    except Exception as exc:  # pragma: no cover
        raise CoordinateConversionError(str(exc)) from exc
    return Point27700(easting=float(easting), northing=float(northing))


def bng_to_lonlat(easting: float, northing: float) -> Point4326:
    """Convert BNG easting/northing (EPSG:27700) to WGS84 lon/lat (EPSG:4326)."""
    try:
        longitude, latitude = _to_wgs84.transform(easting, northing)
    except Exception as exc:  # pragma: no cover
        raise CoordinateConversionError(str(exc)) from exc
    return Point4326(longitude=float(longitude), latitude=float(latitude))


def ensure_bng(
    *,
    easting: float | None = None,
    northing: float | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
) -> Point27700:
    """Return a BNG point from easting/northing, or convert from lon/lat."""
    if easting is not None and northing is not None:
        return Point27700(easting=float(easting), northing=float(northing))

    if latitude is not None and longitude is not None:
        return lonlat_to_bng(float(longitude), float(latitude))

    raise CoordinateConversionError(
        "Need either easting/northing or latitude/longitude."
    )


def euclidean_distance_meters(a: Point27700, b: Point27700) -> float:
    """Planar Euclidean distance in metres between two BNG points."""
    return math.hypot(a.easting - b.easting, a.northing - b.northing)


def detect_crs_from_values(x: float, y: float) -> CrsCode:
    """Infer CRS from coordinate magnitude when no SRS/CRS label is present."""
    if -10.0 <= x <= 5.0 and 49.0 <= y <= 62.0:
        return "EPSG:4326"
    if 0.0 <= x <= 800_000 and -100_000 <= y <= 1_400_000:
        return "EPSG:27700"
    raise CoordinateConversionError(
        f"Unable to infer CRS for coordinates ({x}, {y})."
    )


def feature_title(feature: dict[str, Any]) -> str:
    """Best-effort display name from GeoJSON properties (or feature id)."""
    props = feature.get("properties") or {}
    for key in ("Title", "title", "NAME", "name", "Subtitle"):
        if props.get(key):
            return str(props[key]).strip()
    return str(feature.get("id") or "unknown")


def feature_point(feature: dict[str, Any]) -> Point27700 | None:
    """Extract a BNG point from GeoJSON ``geometry.coordinates``."""
    geometry = feature.get("geometry") or {}
    coords = geometry.get("coordinates")
    if (
        isinstance(coords, (list, tuple))
        and len(coords) >= 2
        and isinstance(coords[0], (int, float))
        and isinstance(coords[1], (int, float))
    ):
        return Point27700(easting=float(coords[0]), northing=float(coords[1]))
    return None


def nearest_n_from_features(
    features: list[dict[str, Any]],
    origin: Point27700,
    *,
    limit: int = 5,
    radius_meters: float | None = None,
) -> list[GritBinMatch]:
    """Sort features by BNG Euclidean distance and return the closest ``limit``."""
    if limit < 1:
        raise ValueError("limit must be >= 1")

    matches: list[GritBinMatch] = []
    for feature in features:
        point = feature_point(feature)
        if point is None:
            continue
        distance = euclidean_distance_meters(origin, point)
        if radius_meters is not None and distance > radius_meters:
            continue
        matches.append(
            GritBinMatch(
                title=feature_title(feature),
                distance_meters=distance,
                point=point,
                properties=dict(feature.get("properties") or {}),
            )
        )

    matches.sort(key=lambda m: m.distance_meters)
    selected = matches[:limit]
    if not selected:
        raise NoGritBinNearbyError(radius_meters)
    return selected


def nearest_from_features(
    features: list[dict[str, Any]],
    origin: Point27700,
    *,
    radius_meters: float,
) -> GritBinMatch:
    """Pick the closest grit bin within radius."""
    return nearest_n_from_features(
        features, origin, radius_meters=radius_meters, limit=1
    )[0]
