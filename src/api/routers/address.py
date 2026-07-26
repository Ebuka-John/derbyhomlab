"""Meta / health routes (address domain boundary for future address endpoints)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from src.models.dto.address import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/")
async def root() -> dict[str, Any]:
    return {
        "service": "nearest-grit-bin",
        "docs": "/docs",
        "endpoint": "/nearest-grit-bin?postcode=DE55%205PB&address=HILLBROW",
    }
