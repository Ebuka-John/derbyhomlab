"""Grit-bin HTTP routes — request/response only.

No upstream I/O or CRS maths here: validate params → call services → map DTO.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import provide_address_service, provide_gritbin_service
from src.models.dto.gritbin import NearestGritBinResponse
from src.services.address_service import AddressService
from src.services.gritbin_service import GritBinService
from src.utils.exceptions import MissingParameterError

router = APIRouter(tags=["gritbins"])


@router.get(
    "/nearest-grit-bin",
    response_model=NearestGritBinResponse,
    responses={
        400: {"description": "Missing or invalid parameters"},
        404: {"description": "Address or grit bin not found"},
        502: {"description": "Upstream Address API or GeoServer failure"},
    },
)
async def nearest_grit_bin(
    postcode: str | None = Query(
        default=None,
        description="UK postcode, e.g. DE55 5PB",
        examples=["DE55 5PB"],
    ),
    address: str | None = Query(
        default=None,
        description="Substring matched against address Title, e.g. HILLBROW",
        examples=["HILLBROW"],
    ),
    address_service: AddressService = Depends(provide_address_service),
    gritbin_service: GritBinService = Depends(provide_gritbin_service),
) -> NearestGritBinResponse:
    """Locate the nearest grit bin within the configured search radius."""
    # Explicit checks so we return typed AppError (400) instead of FastAPI 422
    if not postcode or not postcode.strip():
        raise MissingParameterError("postcode")
    if not address or not address.strip():
        raise MissingParameterError("address")

    # 1) postcode + hint → BNG point
    resolved = await address_service.resolve_address(
        postcode=postcode.strip(),
        address=address.strip(),
    )
    # 2) BNG point → nearest grit bin (DWITHIN / Euclidean)
    match = await gritbin_service.find_nearest(resolved.point)

    return NearestGritBinResponse(
        address=address.strip(),
        postcode=postcode.strip().upper(),
        nearest_grit_bin_title=match.title,
        distance_meters=round(match.distance_meters, 2),
    )
