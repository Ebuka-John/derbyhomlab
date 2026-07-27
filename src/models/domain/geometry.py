"""Coordinate geometry value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point27700:
    """British National Grid point (EPSG:27700), in metres."""

    easting: float
    northing: float


@dataclass(frozen=True, slots=True)
class Point4326:
    """WGS84 point (EPSG:4326), in degrees (longitude, latitude)."""

    longitude: float
    latitude: float
