"""HTTP request/response DTOs for grit-bin endpoints.

DTOs are the API contract (OpenAPI / JSON). Domain objects stay in models/domain.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class NearestGritBinResponse(BaseModel):
    """Contractual response shape for the technical exercise."""

    address: str
    postcode: str
    nearest_grit_bin_title: str
    distance_meters: float = Field(
        ...,
        description="Planar distance in metres (EPSG:27700).",
    )


class GritBinDistanceItem(BaseModel):
    """One ranked grit bin with distance from the resolved address."""

    title: str
    distance_meters: float = Field(
        ...,
        description="Planar distance in metres (EPSG:27700).",
    )


class NearestGritBinsResponse(BaseModel):
    """Nearest-N grit bins within the search radius, sorted by distance."""

    address: str
    postcode: str
    nearest_grit_bins: list[GritBinDistanceItem]


class GritBinItem(BaseModel):
    """A grit bin from the full WFS layer (no distance ranking)."""

    title: str
    easting: float
    northing: float


class GritBinsResponse(BaseModel):
    """Unfiltered dump of grit bins from GeoServer."""

    count: int
    grit_bins: list[GritBinItem]
