"""HTTP request/response DTOs for address / meta endpoints."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class RootResponse(BaseModel):
    service: str
    docs: str
    endpoint: str
    extras: dict[str, Any] | None = None
