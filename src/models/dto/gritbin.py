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
