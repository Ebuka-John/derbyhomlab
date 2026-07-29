"""Meta / health / address-lookup routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import provide_address_service
from src.models.dto.address import (
    AddressLookupResponse,
    HealthResponse,
)
from src.services.address_service import AddressService
from src.utils.exceptions import MissingParameterError
from src.utils.postcode import require_valid_uk_postcode

router = APIRouter(prefix="/api/v1", tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness probe for Docker / load balancers."""
    return HealthResponse(status="ok")


@router.get("/")
async def root() -> dict[str, Any]:
    """Tiny discovery payload pointing at docs and the main endpoints."""
    return {
        "service": "nearest-grit-bin",
        "docs": "/docs",
        "endpoints": {
            "addresses": "/api/v1/addresses?postcode=AB12%203CD",
            "nearest": "/api/v1/nearest-grit-bin?postcode=AB12%203CD&address=Example%20Building",
            "nearest_n": (
                "/api/v1/nearest-grit-bins?postcode=AB12%203CD&address=Example%20Building&limit=5"
            ),
            "all": "/api/v1/grit-bins",
        },
    }


@router.get(
    "/addresses",
    response_model=AddressLookupResponse,
    responses={
        400: {"description": "Missing or invalid parameters"},
        404: {"description": "Postcode or address not found"},
        502: {"description": "Upstream Address API failure"},
    },
)
async def list_addresses(
    postcode: str | None = Query(
        default=None,
        description="UK postcode, e.g. AB12 3CD",
        examples=["AB12 3CD"],
    ),
    address: str | None = Query(
        default=None,
        description="Optional substring filter against address Title / parts",
        examples=["Example Building"],
    ),
    address_service: AddressService = Depends(provide_address_service),
) -> AddressLookupResponse:
    """Inspect Address Lookup results (title, easting, northing, UPRN, …)."""
    if not postcode or not postcode.strip():
        raise MissingParameterError("postcode")

    postcode_clean = require_valid_uk_postcode(postcode)
    address_clean = address.strip() if address and address.strip() else None
    items = await address_service.list_addresses(
        postcode=postcode_clean,
        address=address_clean,
    )
    return AddressLookupResponse(
        postcode=postcode_clean,
        count=len(items),
        addresses=items,
    )
