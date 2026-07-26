"""Coordinate geometry value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point27700:
    """A point in British National Grid metres (easting, northing).

    ``frozen=True`` keeps points immutable so they are safe as dict keys /
    cache values and harder to accidentally mutate mid-query.
    """

    easting: float
    northing: float


@dataclass(frozen=True, slots=True)
class Point4326:
    """A point in WGS84 degrees (longitude, latitude) — always_xy order.

    Axis order matches pyproj ``always_xy=True`` (lon, lat — not lat, lon).
    """

    longitude: float
    latitude: float
