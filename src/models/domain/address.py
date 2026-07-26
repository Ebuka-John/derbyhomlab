"""Address domain objects."""

from __future__ import annotations

from dataclasses import dataclass

from src.models.domain.geometry import Point27700


@dataclass(frozen=True, slots=True)
class ResolvedAddress:
    """Address match with coordinates normalised to EPSG:27700."""

    title: str
    postcode: str
    point: Point27700
