"""Address domain objects."""

from __future__ import annotations

from dataclasses import dataclass

from src.models.domain.geometry import Point27700


@dataclass(frozen=True, slots=True)
class ResolvedAddress:
    """Matched address with coordinates already normalised to EPSG:27700."""

    title: str
    postcode: str
    point: Point27700
