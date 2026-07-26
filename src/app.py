"""FastAPI application factory and ASGI app instance.

``create_app()`` is the testable entry; module-level ``app`` is what uvicorn loads
(``uvicorn src.app:app``). ``main.py`` only starts the process.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.routers import address as address_router
from src.api.routers import gritbins as gritbins_router
from src.config import get_settings
from src.core.logging import configure_logging
from src.utils.exceptions import AppError

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown: one shared httpx client for connection pooling."""
    settings = get_settings()
    async with httpx.AsyncClient(timeout=settings.http_timeout_seconds) as client:
        app.state.settings = settings
        app.state.http_client = client
        logger.info("Application started — config loaded from environment")
        yield  # app runs while we hold the client open
    logger.info("Application shutdown")


def create_app() -> FastAPI:
    """Build and return the FastAPI application (testable factory)."""
    load_dotenv()  # ensure .env is present even if cwd differs
    configure_logging()

    application = FastAPI(
        title="Nearest Grit Bin API",
        description=(
            "Finds the nearest Derbyshire County Council grit bin to a given "
            "address within a postcode, using the Address Lookup API and GeoServer WFS."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    @application.exception_handler(AppError)
    async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
        # One handler for the whole AppError hierarchy → stable JSON errors
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
        )

    application.include_router(address_router.router)  # /health, /
    application.include_router(gritbins_router.router)  # /nearest-grit-bin
    return application


# ASGI callable imported by uvicorn / TestClient
app = create_app()
