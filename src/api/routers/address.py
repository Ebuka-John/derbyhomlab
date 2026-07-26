"""Meta / health routes (system endpoints; address router reserved for growth)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from src.models.dto.address import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness probe for Docker / load balancers."""
    return HealthResponse(status="ok")


@router.get("/")
async def root() -> dict[str, Any]:
    """Tiny discovery payload pointing at docs and the main endpoint."""
    return {
        "service": "nearest-grit-bin",
        "docs": "/docs",
        "endpoint": "/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW",
    }
