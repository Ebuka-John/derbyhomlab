"""Address Lookup API data access (HTTP only — no business rules)."""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import quote

import httpx

from src.core.settings import Settings
from src.utils.exceptions import (
    AddressApiUnreachableError,
    AddressNotFoundError,
    UnexpectedSchemaError,
)

logger = logging.getLogger(__name__)


def unwrap_address_list(payload: Any) -> list[dict[str, Any]]:
    """Normalise varied Address API envelopes into a flat list of records.

    Live payloads may be a bare list, or wrapped under results/addresses/data/Items.
    """
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        for key in (
            "results",
            "Results",
            "addresses",
            "Addresses",
            "data",
            "Data",
            "Items",
            "items",
        ):
            if key in payload and isinstance(payload[key], list):
                records = payload[key]
                break
        else:
            # Single address object returned as the whole body
            records = [payload]
    else:
        raise UnexpectedSchemaError(
            "Address API",
            detail=f"Expected list or object, got {type(payload).__name__}.",
        )

    if not all(isinstance(item, dict) for item in records):
        raise UnexpectedSchemaError(
            "Address API",
            detail="Address list contains non-object entries.",
        )
    return records  # type: ignore[return-value]


class AddressRepository:
    """Fetches raw address records from the Derbyshire Address Lookup API.

    Matching / coordinate normalisation belongs in ``AddressService``, not here.
    """

    def __init__(self, settings: Settings, client: httpx.AsyncClient) -> None:
        self._settings = settings
        self._client = client

    async def fetch_by_postcode(self, postcode: str) -> list[dict[str, Any]]:
        """GET ``{base}/{postcode}`` with auth headers from settings."""
        # quote (not quote_plus) keeps spaces as %20 — matches council API style
        encoded = quote(postcode.strip(), safe="")
        url = f"{self._settings.address_api_base_url}/{encoded}"

        try:
            response = await self._client.get(
                url,
                headers=self._settings.address_api_headers,
            )
        except httpx.RequestError as exc:
            logger.warning("Address API request failed: %s", exc)
            raise AddressApiUnreachableError(str(exc)) from exc

        if response.status_code >= 500:
            raise AddressApiUnreachableError(f"HTTP {response.status_code}")
        if response.status_code == 404:
            raise AddressNotFoundError(postcode)
        if response.status_code >= 400:
            raise AddressApiUnreachableError(
                f"HTTP {response.status_code}: {response.text[:200]}"
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise UnexpectedSchemaError(
                "Address API", detail="Response was not valid JSON."
            ) from exc

        records = unwrap_address_list(payload)
        if not records:
            raise AddressNotFoundError(postcode)
        return records
