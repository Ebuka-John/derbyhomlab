"""FastAPI application entrypoint.

Exposes:
  GET /nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW

Environment variables are loaded via pydantic-settings (python-dotenv under the
hood) when Settings is first instantiated — see src/config.py.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.config import Settings, get_settings
from src.services.address_service import AddressService
from src.services.geoserver_service import GeoServerService
from src.utils.errors import AppError, MissingParameterError

# Ensure .env is loaded before Settings validation (works even if cwd differs).
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


class NearestGritBinResponse(BaseModel):
    """Contractual response shape for the technical exercise."""

    address: str
    postcode: str
    nearest_grit_bin_title: str
    distance_meters: float = Field(
        ...,
        description="Planar distance in metres (EPSG:27700).",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Share one httpx client across requests for connection pooling."""
    settings = get_settings()
    async with httpx.AsyncClient(timeout=settings.http_timeout_seconds) as client:
        app.state.settings = settings
        app.state.http_client = client
        logger.info("Application started — config loaded from environment")
        yield
    logger.info("Application shutdown")


app = FastAPI(
    title="Nearest Grit Bin API",
    description=(
        "Finds the nearest Derbyshire County Council grit bin to a given "
        "address within a postcode, using the Address Lookup API and GeoServer WFS."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(AppError)
async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    """Map domain errors to consistent JSON bodies."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
    "/nearest-grit-bin",
    response_model=NearestGritBinResponse,
    responses={
        400: {"description": "Missing or invalid parameters"},
        404: {"description": "Address or grit bin not found"},
        502: {"description": "Upstream Address API or GeoServer failure"},
    },
)
async def nearest_grit_bin(
    request: Request,
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
) -> NearestGritBinResponse:
    """Locate the nearest grit bin within the configured search radius."""
    if not postcode or not postcode.strip():
        raise MissingParameterError("postcode")
    if not address or not address.strip():
        raise MissingParameterError("address")

    settings: Settings = request.app.state.settings
    client: httpx.AsyncClient = request.app.state.http_client

    address_svc = AddressService(settings, client=client)
    geoserver_svc = GeoServerService(settings, client=client)

    resolved = await address_svc.resolve_address(
        postcode=postcode.strip(),
        address=address.strip(),
    )
    match = await geoserver_svc.find_nearest(resolved.point)

    return NearestGritBinResponse(
        address=address.strip(),
        postcode=postcode.strip().upper(),
        nearest_grit_bin_title=match.title,
        distance_meters=round(match.distance_meters, 2),
    )


@app.get("/")
async def root() -> dict[str, Any]:
    return {
        "service": "nearest-grit-bin",
        "docs": "/docs",
        "endpoint": "/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW",
    }
