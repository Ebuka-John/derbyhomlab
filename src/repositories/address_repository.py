"""Address Lookup API data access (HTTP only — no business rules)."""

from __future__ import annotations

import logging
import re
from typing import Any
from urllib.parse import quote

import httpx

from src.core.settings import Settings
from src.utils.exceptions import (
    AddressApiUnreachableError,
    AddressNotFoundError,
    InvalidPostcodeError,
    UnexpectedSchemaError,
)

logger = logging.getLogger(__name__)

_RESPONSE_ERROR_XML = re.compile(
    r"<ResponseError(?:\s[^>]*)?>([^<]*)</ResponseError>",
    re.IGNORECASE,
)

# Fields that mark a real address row (vs an error-only stub).
_IDENTITY_KEYS = (
    "UPRN",
    "BuildingName",
    "Title",
    "ThoroughFareName",
    "PostCode",
    "SpatialFeature",
)


def _extract_xml_response_error(body: str) -> str | None:
    """Pull Derbyshire ``ResponseError`` text from an XML error envelope."""
    match = _RESPONSE_ERROR_XML.search(body)
    if match is None:
        return None
    message = match.group(1).strip()
    return message or None


def _raise_for_address_api_error(postcode: str, error_message: str) -> None:
    """Map upstream ResponseError strings onto typed AppErrors."""
    lowered = error_message.lower()
    if "invalid postcode" in lowered:
        raise InvalidPostcodeError(postcode, detail=error_message)
    raise AddressNotFoundError(postcode)


def unwrap_address_list(payload: Any) -> list[dict[str, Any]]:
    """Normalise Address API envelopes into a flat list of records."""
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


def _top_level_error_if_stub(record: dict[str, Any]) -> str | None:
    """Return top-level ResponseError only when the row has no address identity."""
    error = record.get("ResponseError") or record.get("responseError")
    if error is None or not str(error).strip():
        return None

    has_identity = False
    for key in _IDENTITY_KEYS:
        value = record.get(key)
        if value is None or value == "":
            continue
        if isinstance(value, dict) and not value:
            continue
        has_identity = True
        break

    if has_identity:
        return None
    return str(error).strip()


def _records_look_like_error_envelope(records: list[dict[str, Any]]) -> str | None:
    """Detect a JSON list that is only error stubs (no real addresses)."""
    if not records:
        return None
    stub_errors = [_top_level_error_if_stub(record) for record in records]
    if stub_errors and all(stub_errors):
        return stub_errors[0]
    return None


class AddressRepository:
    """Fetches raw address records from the Derbyshire Address Lookup API."""

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

        body = response.text
        content_type = response.headers.get("content-type", "")
        body_preview = body.lstrip()[:200]
        looks_like_xml = body_preview.startswith("<") or (
            "xml" in content_type.lower() and "json" not in content_type.lower()
        )

        if response.status_code == 404:
            raise AddressNotFoundError(postcode)

        if response.status_code >= 400:
            # Prefer XML ResponseError on 4xx; success JSON embeds nested ResponseError.
            if looks_like_xml:
                api_error = _extract_xml_response_error(body)
                if api_error:
                    _raise_for_address_api_error(postcode, api_error)
            raise AddressApiUnreachableError(
                f"HTTP {response.status_code}: {body[:200]}"
            )

        # Live API often returns HTTP 200 + XML ResponseError for bad postcodes.
        if looks_like_xml:
            api_error = _extract_xml_response_error(body)
            if api_error:
                _raise_for_address_api_error(postcode, api_error)
            raise UnexpectedSchemaError(
                "Address API",
                detail=f"Expected JSON address list, got XML: {body_preview[:160]}",
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise UnexpectedSchemaError(
                "Address API", detail="Response was not valid JSON."
            ) from exc

        records = unwrap_address_list(payload)
        envelope_error = _records_look_like_error_envelope(records)
        if envelope_error:
            _raise_for_address_api_error(postcode, envelope_error)
        if not records:
            raise AddressNotFoundError(postcode)
        return records
