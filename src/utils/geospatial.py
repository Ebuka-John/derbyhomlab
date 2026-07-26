"""Geospatial helpers: CRS conversion, planar distance, nearest-feature selection.

Why British National Grid (EPSG:27700)?
--------------------------------------
Maps need a *coordinate reference system* (CRS) — a shared rule for where
"x, y" sit on Earth.

* **EPSG:4326 (WGS84)** — what phones/GPS and Google Maps use:
  ``longitude`` (east–west) and ``latitude`` (north–south) in **degrees**.
  Degrees are awkward for "how many metres apart?" maths.

* **EPSG:27700 (British National Grid / BNG)** — what UK councils typically
  publish for assets (including Derbyshire grit bins):
  ``easting`` and ``northing`` in **metres** on a flat grid covering GB.
  Example shape: easting ~440_000, northing ~360_000 for much of Derbyshire.

This module **normalises everything to BNG metres** before distance work so both
of these mean *real metres* (not degrees):

* **GeoServer ``DWITHIN``** — ask the server to return only features inside a
  metre radius. Example CQL used by this project::

      DWITHIN(SP_GEOMETRY, POINT(443563 360212), 100, meters)

  Read it as: “keep grit bins whose ``SP_GEOMETRY`` is within **100 metres** of
  this BNG point (easting 443563, northing 360212).”
  GeoServer does the spatial filter; you never download the whole county.

* **Euclidean distance in Python** — after you have candidates, measure
  yourself with school straight-line maths::

      distance = sqrt( (easting_a - easting_b)² + (northing_a - northing_b)² )

  Example: origin (443563, 360212) and bin (443600, 360250) → about **53 m**.

Mixing lon/lat degrees with BNG metres would give nonsense distances.
"""

from __future__ import annotations

import math
from typing import Any, Literal

from pyproj import Transformer

from src.models.domain.geometry import Point27700, Point4326
from src.models.domain.gritbin import GritBinMatch
from src.utils.exceptions import CoordinateConversionError, NoGritBinNearbyError

# Allowed CRS labels we recognise in this codebase.
# - EPSG:27700 → British National Grid (metres: easting, northing)
# - EPSG:4326  → WGS84 (degrees: longitude, latitude)
CrsCode = Literal["EPSG:27700", "EPSG:4326"]

# pyproj Transformers are expensive to build — create once at import time.
# always_xy=True forces axis order to (x, y) = (lon, lat) or (easting, northing).
# Without it, some CRS definitions swap to (lat, lon) and silently break maths.
_to_bng = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
_to_wgs84 = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)


def lonlat_to_bng(longitude: float, latitude: float) -> Point27700:
    """Convert WGS84 lon/lat (EPSG:4326) → BNG easting/northing (EPSG:27700).

    Use this when an address (or other source) only gives GPS-style degrees and
    you need council-grid metres for distance / ``DWITHIN``.

    Args:
        longitude: Degrees east of Greenwich (UK is typically negative-ish to
            slightly positive, e.g. about -1.5 for Derbyshire).
        latitude: Degrees north of the equator (UK ~49–60).

    Returns:
        A ``Point27700`` with easting/northing in metres.
    """
    try:
        easting, northing = _to_bng.transform(longitude, latitude)
    except Exception as exc:  # pragma: no cover
        raise CoordinateConversionError(str(exc)) from exc
    return Point27700(easting=float(easting), northing=float(northing))


def bng_to_lonlat(easting: float, northing: float) -> Point4326:
    """Convert BNG easting/northing (EPSG:27700) → WGS84 lon/lat (EPSG:4326).

    The reverse of ``lonlat_to_bng``. Useful if you must display a bin on a
    web map that expects lon/lat, after you finished distance work in BNG.
    """
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
    """Return a BNG point from whichever coordinate pair is available.

    Address APIs sometimes return Eastings/Northings already (EPSG:27700),
    sometimes only lat/lon (EPSG:4326). This helper hides that variance:

    1. Prefer explicit easting/northing (already metres on the British grid).
    2. Else convert lon/lat via ``lonlat_to_bng``.

    Keyword-only args avoid swapping axes by accident (a common GIS bug:
    passing lat where lon was expected).
    """
    if easting is not None and northing is not None:
        return Point27700(easting=float(easting), northing=float(northing))

    if latitude is not None and longitude is not None:
        return lonlat_to_bng(float(longitude), float(latitude))

    raise CoordinateConversionError(
        "Need either easting/northing or latitude/longitude."
    )


def euclidean_distance_meters(a: Point27700, b: Point27700) -> float:
    """Planar Euclidean distance in metres between two BNG points.

    Formula (school straight-line distance on a flat plane)::

        distance = sqrt( (easting_a - easting_b)² + (northing_a - northing_b)² )

    ``math.hypot(Δe, Δn)`` is the stable way to compute that.

    Why this is OK for EPSG:27700 (and not for raw lon/lat):
    - BNG units are already **metres**, so the result is metres.
    - Over short distances (e.g. ~100 m grit-bin search) treating the grid as
      flat is accurate enough for this exercise.
    - On lon/lat you would need Haversine (great-circle) maths instead, because
      degrees are not metres and Earth is curved.

    Both ``a`` and ``b`` **must** already be EPSG:27700.
    """
    return math.hypot(a.easting - b.easting, a.northing - b.northing)


def detect_crs_from_values(x: float, y: float) -> CrsCode:
    """Guess CRS when a payload gives numbers but no SRS/CRS label.

    Quick visual check:
    - Lon/lat for the UK: small numbers (lon about -10..5, lat about 49..62).
    - BNG: large metre values (easting up to ~800_000, northing up to ~1_400_000).

    If a pair looks like UK lon/lat → EPSG:4326; if it looks like grid metres →
    EPSG:27700. Otherwise raise — better than silently mis-converting.
    """
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
    """Extract a BNG Point from GeoJSON ``geometry.coordinates``.

    GeoServer naming quirk (important for Derbyshire):
    - In CQL filters the geometry column is called ``SP_GEOMETRY``.
    - In GeoJSON responses that same geometry appears as normal
      ``geometry: { type: Point, coordinates: [easting, northing] }``.

    For this grit-bin layer those coordinates are EPSG:27700 metres, so we
    store them as ``Point27700`` ready for Euclidean distance.
    """
    geometry = feature.get("geometry") or {}
    coords = geometry.get("coordinates")
    if (
        isinstance(coords, (list, tuple))
        and len(coords) >= 2
        and isinstance(coords[0], (int, float))
        and isinstance(coords[1], (int, float))
    ):
        return Point27700(easting=float(coords[0]), northing=float(coords[1]))
    return None  # skip malformed / empty geometries


def nearest_n_from_features(
    features: list[dict[str, Any]],
    origin: Point27700,
    *,
    limit: int = 5,
    radius_meters: float | None = None,
) -> list[GritBinMatch]:
    """Sort grit bins by BNG Euclidean distance and return the closest ``limit``.

    ``origin`` must be EPSG:27700 (same CRS as the grit-bin layer).

    When ``radius_meters`` is set, candidates outside that window are dropped
    (exercise-style ~100 m search). When ``None``, the full candidate set is
    ranked — used by nearest-N so a tight radius does not collapse to one bin.
    """
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
    """Pick the closest grit bin within radius (``nearest_n_from_features`` with limit=1)."""
    return nearest_n_from_features(
        features, origin, radius_meters=radius_meters, limit=1
    )[0]
