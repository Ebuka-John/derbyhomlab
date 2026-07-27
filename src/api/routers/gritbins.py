"""Grit-bin HTTP routes — request/response only.

No upstream I/O or CRS maths here: validate params → call services → map DTO.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse

from src.api.dependencies import provide_address_service, provide_gritbin_service
from src.models.dto.gritbin import (
    GritBinDistanceItem,
    GritBinItem,
    GritBinsResponse,
    NearestGritBinResponse,
    NearestGritBinsResponse,
)
from src.services.address_service import AddressService
from src.services.gritbin_service import GritBinService
from src.utils.excel_export import DEFAULT_EXPORT_PATH, write_grit_bins_excel
from src.utils.exceptions import ExportAlreadyExistsError, MissingParameterError

router = APIRouter(tags=["gritbins"])


def _require_postcode_address(
    postcode: str | None, address: str | None
) -> tuple[str, str]:
    """Explicit checks so we return typed AppError (400) instead of FastAPI 422."""
    if not postcode or not postcode.strip():
        raise MissingParameterError("postcode")
    if not address or not address.strip():
        raise MissingParameterError("address")
    return postcode.strip(), address.strip()


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
    postcode_clean, address_clean = _require_postcode_address(postcode, address)

    # 1) postcode + hint → BNG point
    resolved = await address_service.resolve_address(
        postcode=postcode_clean,
        address=address_clean,
    )
    # 2) BNG point → nearest grit bin (DWITHIN / Euclidean)
    match = await gritbin_service.find_nearest(resolved.point)

    return NearestGritBinResponse(
        address=address_clean,
        postcode=postcode_clean.upper(),
        nearest_grit_bin_title=match.title,
        distance_meters=round(match.distance_meters, 2),
    )


@router.get(
    "/nearest-grit-bins",
    response_model=NearestGritBinsResponse,
    responses={
        400: {"description": "Missing or invalid parameters"},
        404: {"description": "Address or grit bin not found"},
        502: {"description": "Upstream Address API or GeoServer failure"},
    },
)
async def nearest_grit_bins(
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
    limit: int = Query(
        default=5,
        ge=1,
        le=50,
        description="How many nearest grit bins to return (sorted by distance).",
    ),
    address_service: AddressService = Depends(provide_address_service),
    gritbin_service: GritBinService = Depends(provide_gritbin_service),
) -> NearestGritBinsResponse:
    """Locate the nearest N grit bins within the configured search radius."""
    postcode_clean, address_clean = _require_postcode_address(postcode, address)

    resolved = await address_service.resolve_address(
        postcode=postcode_clean,
        address=address_clean,
    )
    matches = await gritbin_service.find_nearest_n(resolved.point, limit=limit)

    return NearestGritBinsResponse(
        address=address_clean,
        postcode=postcode_clean.upper(),
        nearest_grit_bins=[
            GritBinDistanceItem(
                title=m.title,
                distance_meters=round(m.distance_meters, 2),
            )
            for m in matches
        ],
    )


@router.get(
    "/grit-bins",
    response_model=GritBinsResponse,
    responses={
        502: {"description": "Upstream GeoServer failure"},
    },
)
async def list_grit_bins(
    gritbin_service: GritBinService = Depends(provide_gritbin_service),
) -> GritBinsResponse:
    """Return every grit bin from the Derbyshire WFS layer (unfiltered)."""
    bins = await gritbin_service.list_all()
    items = [
        GritBinItem(
            title=b.title,
            easting=b.point.easting,
            northing=b.point.northing,
        )
        for b in bins
    ]
    return GritBinsResponse(count=len(items), grit_bins=items)


@router.post(
    "/grit-bins/export-excel",
    responses={
        200: {"description": "Excel file written and returned as download"},
        409: {"description": "Export already exists (one-shot guard)"},
        502: {"description": "Upstream GeoServer failure"},
    },
    tags=["utility"],
    summary="One-shot: save all grit bins to Excel (not part of assessment)",
)
async def export_grit_bins_excel(
    force: bool = Query(
        default=False,
        description="Overwrite the temp gritbins.xlsx if it already exists.",
    ),
    gritbin_service: GritBinService = Depends(provide_gritbin_service),
) -> FileResponse:
    """Fetch the full WFS layer once and write a temp ``gritbins.xlsx``.

    Local helper only — not used by the Next.js UI or the Derbyshire exercise
    contract. File is written under the process temp dir (works in Docker).
    By default refuses to run again if the file already exists
    (pass ``force=true`` to overwrite). The response body is the Excel download.
    """
    path = Path(DEFAULT_EXPORT_PATH)
    if path.exists() and not force:
        raise ExportAlreadyExistsError(str(path.resolve()))

    bins = await gritbin_service.list_all()
    saved = write_grit_bins_excel(bins, path)
    return FileResponse(
        path=saved,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        filename="gritbins.xlsx",
        headers={"X-Export-Count": str(len(bins)), "X-Export-Path": str(saved)},
    )
