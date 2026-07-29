"""Meta / health routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from src.models.dto.address import HealthResponse

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
            "nearest": "/api/v1/nearest-grit-bin?postcode=AB12%203CD&address=Example%20Building",
            "nearest_n": (
                "/api/v1/nearest-grit-bins?postcode=AB12%203CD&address=Example%20Building&limit=5"
            ),
            "all": "/api/v1/grit-bins",
        },
    }
