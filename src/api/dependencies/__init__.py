"""FastAPI dependency providers (settings, HTTP client, services).

Routers depend on these providers so they never construct httpx clients or
read ``app.state`` directly — keeps HTTP handlers thin and testable.
"""

from __future__ import annotations

import httpx
from fastapi import Request

from src.config import Settings, get_settings
from src.services.address_service import AddressService
from src.services.gritbin_service import GritBinService


def provide_settings() -> Settings:
    return get_settings()


def provide_http_client(request: Request) -> httpx.AsyncClient:
    # Shared client created in app lifespan (connection pooling)
    return request.app.state.http_client


def provide_address_service(
    request: Request,
) -> AddressService:
    settings: Settings = request.app.state.settings
    client: httpx.AsyncClient = request.app.state.http_client
    return AddressService(settings, client=client)


def provide_gritbin_service(
    request: Request,
) -> GritBinService:
    settings: Settings = request.app.state.settings
    client: httpx.AsyncClient = request.app.state.http_client
    return GritBinService(settings, client=client)
