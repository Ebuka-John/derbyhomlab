"""Coordinate geometry value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point27700:
    """A point in British National Grid metres (easting, northing)."""

    easting: float
    northing: float


@dataclass(frozen=True, slots=True)
class Point4326:
    """A point in WGS84 degrees (longitude, latitude) — always_xy order."""

    longitude: float
    latitude: float
