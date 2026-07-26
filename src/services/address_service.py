"""Address Lookup API client.

Calls:
  GET {ADDRESS_API_BASE_URL}/{postcode}
  Headers: x-alias, x-auth-token

Derbyshire Address API (live schema) returns records with BuildingName /
ThoroughFareName / SpatialFeature.Eastings|Northings — there is no single
`Title` field. We also accept common aliases so alternate envelopes still work.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import httpx

from src.config import Settings
from src.utils.coordinates import Point27700, ensure_bng
from src.utils.errors import (
    AddressApiUnreachableError,
    AddressNotFoundError,
    TargetAddressNotFoundError,
    UnexpectedSchemaError,
)

logger = logging.getLogger(__name__)

# Explicit Title-like fields (generic / other councils)
_TITLE_KEYS = (
    "Title",
    "title",
    "Address",
    "address",
    "FullAddress",
    "fullAddress",
    "AddressLine",
)

# Derbyshire NLPG-style parts used to compose a display title AND to match
_MATCH_PART_KEYS = (
    "BuildingName",
    "SubBuildingName",
    "BuildingNumber",
    "OrganisationName",
    "DepartmentName",
    "DependentThoroughfareName",
    "ThoroughFareName",
    "DependentLocality",
    "DoubleDependentLocality",
    "PostTown",
)

_EASTING_KEYS = (
    "Easting",
    "Eastings",  # Derbyshire SpatialFeature
    "easting",
    "X_COORDINATE",
    "x",
    "X",
    "EastingCoordinate",
)
_NORTHING_KEYS = (
    "Northing",
    "Northings",  # Derbyshire SpatialFeature
    "northing",
    "Y_COORDINATE",
    "y",
    "Y",
    "NorthingCoordinate",
)
_LAT_KEYS = ("Latitude", "latitude", "lat", "Lat")
_LON_KEYS = ("Longitude", "longitude", "lon", "Lng", "lng", "Long")


@dataclass(frozen=True, slots=True)
class ResolvedAddress:
    """Address match with coordinates normalised to EPSG:27700."""

    title: str
    postcode: str
    point: Point27700


def _first_present(record: dict[str, Any], keys: tuple[str, ...]) -> Any | None:
    for key in keys:
        if key in record and record[key] is not None and record[key] != "":
            return record[key]
    return None


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _unwrap_address_list(payload: Any) -> list[dict[str, Any]]:
    """Accept list, or common envelope shapes: {results|addresses|data|Items: [...]}."""
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        for key in ("results", "Results", "addresses", "Addresses", "data", "Data", "Items", "items"):
            if key in payload and isinstance(payload[key], list):
                records = payload[key]
                break
        else:
            # Single address object
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


def _compose_title(record: dict[str, Any]) -> str | None:
    """Build a human-readable title from Derbyshire address parts (or a Title field)."""
    explicit = _first_present(record, _TITLE_KEYS)
    if explicit is not None:
        return str(explicit).strip()

    parts: list[str] = []
    for key in _MATCH_PART_KEYS:
        value = record.get(key)
        if value is not None and str(value).strip():
            parts.append(str(value).strip())

    postcode = record.get("PostCode") or record.get("Postcode") or record.get("postcode")
    if postcode and str(postcode).strip():
        parts.append(str(postcode).strip())

    return ", ".join(parts) if parts else None


def _matchable_text(record: dict[str, Any]) -> str:
    """All text we search when looking for the address query (e.g. HILLBROW)."""
    chunks: list[str] = []
    title = _compose_title(record)
    if title:
        chunks.append(title)
    for key in _MATCH_PART_KEYS + _TITLE_KEYS:
        value = record.get(key)
        if value is not None and str(value).strip():
            chunks.append(str(value).strip())
    return " ".join(chunks).upper()


def _extract_point(record: dict[str, Any]) -> Point27700:
    """Pull coordinates from a record, converting to BNG when needed.

    Derbyshire nests BNG under SpatialFeature.Eastings / SpatialFeature.Northings.
    """
    nested = (
        record.get("SpatialFeature")
        or record.get("spatialFeature")
        or record.get("location")
        or record.get("Location")
        or record.get("Coordinates")
    )
    search_space: dict[str, Any] = dict(record)
    if isinstance(nested, dict):
        search_space.update(nested)

    easting = _as_float(_first_present(search_space, _EASTING_KEYS))
    northing = _as_float(_first_present(search_space, _NORTHING_KEYS))
    latitude = _as_float(_first_present(search_space, _LAT_KEYS))
    longitude = _as_float(_first_present(search_space, _LON_KEYS))

    try:
        return ensure_bng(
            easting=easting,
            northing=northing,
            latitude=latitude,
            longitude=longitude,
        )
    except Exception as exc:
        raise UnexpectedSchemaError(
            "Address API",
            detail=f"Could not extract coordinates: {exc}",
        ) from exc


def find_matching_address(
    records: list[dict[str, Any]],
    *,
    address: str,
    postcode: str,
) -> ResolvedAddress:
    """Find the first record whose address text contains `address` (case-insensitive).

    Live Derbyshire payloads put the property name in BuildingName (e.g. HILLBROW),
    not a Title field — we match across composed title + address parts.
    """
    needle = address.strip().upper()
    if not needle:
        raise TargetAddressNotFoundError(address, postcode)

    for record in records:
        if needle not in _matchable_text(record):
            continue
        title = _compose_title(record)
        if title is None:
            continue
        point = _extract_point(record)
        return ResolvedAddress(title=title, postcode=postcode, point=point)

    raise TargetAddressNotFoundError(address, postcode)


class AddressService:
    """Thin async client around the Derbyshire Address Lookup API."""

    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self._settings = settings
        self._client = client
        self._owns_client = client is None

    async def __aenter__(self) -> AddressService:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._settings.http_timeout_seconds)
        return self

    async def __aexit__(self, *exc: object) -> None:
        if self._owns_client and self._client is not None:
            await self._client.aclose()

    async def lookup_postcode(self, postcode: str) -> list[dict[str, Any]]:
        """GET addresses for a postcode. Raises typed errors on failure."""
        # Keep space encoding as %20 (quote, not quote_plus) to match council APIs
        encoded = quote(postcode.strip(), safe="")
        url = f"{self._settings.address_api_base_url}/{encoded}"

        assert self._client is not None
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

        records = _unwrap_address_list(payload)
        if not records:
            raise AddressNotFoundError(postcode)
        return records

    async def resolve_address(self, *, postcode: str, address: str) -> ResolvedAddress:
        """End-to-end: fetch postcode addresses and match the target Title."""
        records = await self.lookup_postcode(postcode)
        return find_matching_address(records, address=address, postcode=postcode)
