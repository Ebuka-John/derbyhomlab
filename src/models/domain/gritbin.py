"""Grit-bin domain objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.models.domain.geometry import Point27700


@dataclass(frozen=True, slots=True)
class GritBin:
    """A grit-bin asset located in British National Grid."""

    title: str
    point: Point27700
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class GritBinMatch:
    """Nearest grit bin relative to an origin point."""

    title: str
    distance_meters: float
    point: Point27700
    properties: dict[str, Any] = field(default_factory=dict)
