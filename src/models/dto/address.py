"""HTTP request/response DTOs for address / meta endpoints."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class RootResponse(BaseModel):
    service: str
    docs: str
    endpoint: str
    extras: dict[str, Any] | None = None


class AddressLookupItem(BaseModel):
    """One cleaned Address Lookup row (coordinates in EPSG:27700 when present)."""

    title: str
    postcode: str | None = None
    uprn: str | None = None
    building_name: str | None = None
    building_number: str | None = None
    thoroughfare: str | None = None
    post_town: str | None = None
    easting: float | None = None
    northing: float | None = None


class AddressLookupResponse(BaseModel):
    postcode: str
    count: int
    addresses: list[AddressLookupItem] = Field(default_factory=list)
