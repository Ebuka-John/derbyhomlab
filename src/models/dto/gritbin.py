"""HTTP request/response DTOs for grit-bin endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class NearestGritBinResponse(BaseModel):
    """Nearest grit-bin response for the technical exercise."""

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
    """Nearest-N grit bins, sorted by distance."""

    address: str
    postcode: str
    nearest_grit_bins: list[GritBinDistanceItem]


class GritBinItem(BaseModel):
    """A grit bin from the full WFS layer."""

    title: str
    easting: float
    northing: float


class GritBinsResponse(BaseModel):
    """Unfiltered dump of grit bins from GeoServer."""

    count: int
    grit_bins: list[GritBinItem]
