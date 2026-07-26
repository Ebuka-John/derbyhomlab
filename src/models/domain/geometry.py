"""Coordinate geometry value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point27700:
    """A point on the British National Grid (EPSG:27700), in metres.

    * ``easting``  — metres east of the BNG origin (larger → further east)
    * ``northing`` — metres north of the BNG origin (larger → further north)

    UK council GIS (including Derbyshire grit bins) usually publish in this CRS.
    Prefer this type for any distance / ``DWITHIN`` maths.

    ``frozen=True`` keeps points immutable so they are safe as dict keys /
    cache values and harder to accidentally mutate mid-query.
    """

    easting: float
    northing: float


@dataclass(frozen=True, slots=True)
class Point4326:
    """A GPS-style WGS84 point (EPSG:4326), in degrees.

    * ``longitude`` — east–west (x); UK values are roughly -10 to +5
    * ``latitude``  — north–south (y); UK values are roughly 49 to 62

    Axis order matches pyproj ``always_xy=True`` (lon, lat — **not** lat, lon).
    Convert to ``Point27700`` before measuring metres.
    """

    longitude: float
    latitude: float
