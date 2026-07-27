"""Address resolution business logic (no FastAPI imports).

Tolerant field aliases cover the live Derbyshire NLPG-style schema
(BuildingName + SpatialFeature.Eastings/Northings) and generic Title/Easting
payloads used in tests / other councils.
"""

from __future__ import annotations

from typing import Any

import httpx

from src.core.settings import Settings
from src.models.domain.address import ResolvedAddress
from src.repositories.address_repository import AddressRepository
from src.utils.exceptions import TargetAddressNotFoundError, UnexpectedSchemaError
from src.utils.geospatial import ensure_bng

# Explicit single-field titles (generic / alternate APIs)
_TITLE_KEYS = (
    "Title",
    "title",
    "Address",
    "address",
    "FullAddress",
    "fullAddress",
    "AddressLine",
)

# Derbyshire NLPG-style parts — composed into a display title AND used for matching
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

# Live schema uses Eastings/Northings (plural) under SpatialFeature
_EASTING_KEYS = (
    "Easting",
    "Eastings",
    "easting",
    "X_COORDINATE",
    "x",
    "X",
    "EastingCoordinate",
)
_NORTHING_KEYS = (
    "Northing",
    "Northings",
    "northing",
    "Y_COORDINATE",
    "y",
    "Y",
    "NorthingCoordinate",
)
_LAT_KEYS = ("Latitude", "latitude", "lat", "Lat")
_LON_KEYS = ("Longitude", "longitude", "lon", "Lng", "lng", "Long")


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


def _compose_title(record: dict[str, Any]) -> str | None:
    """Human-readable label from Title field or joined address parts."""
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
    """Uppercased haystack for substring match (e.g. query ``Example Building``)."""
    chunks: list[str] = []
    title = _compose_title(record)
    if title:
        chunks.append(title)
    for key in _MATCH_PART_KEYS + _TITLE_KEYS:
        value = record.get(key)
        if value is not None and str(value).strip():
            chunks.append(str(value).strip())
    return " ".join(chunks).upper()


def _extract_point(record: dict[str, Any]):
    """Pull BNG or lat/lon from top-level or nested SpatialFeature / location."""
    nested = (
        record.get("SpatialFeature")
        or record.get("spatialFeature")
        or record.get("location")
        or record.get("Location")
        or record.get("Coordinates")
    )
    search_space: dict[str, Any] = dict(record)
    if isinstance(nested, dict):
        search_space.update(nested)  # nested keys win for Eastings/Northings

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
    """First record whose address text contains ``address`` (case-insensitive)."""
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
    """Resolves a postcode + address hint to a BNG point.

    Accepts either a shared httpx client (production DI) or owns a short-lived
    client when used as an async context manager in tests.
    """

    def __init__(
        self,
        settings: Settings,
        client: httpx.AsyncClient | None = None,
        *,
        repository: AddressRepository | None = None,
    ) -> None:
        self._settings = settings
        self._client = client
        # Only close the client if we created it ourselves
        self._owns_client = client is None and repository is None
        self._repository = repository

    async def __aenter__(self) -> AddressService:
        if self._repository is None:
            if self._client is None:
                self._client = httpx.AsyncClient(
                    timeout=self._settings.http_timeout_seconds
                )
            self._repository = AddressRepository(self._settings, self._client)
        return self

    async def __aexit__(self, *exc: object) -> None:
        if self._owns_client and self._client is not None:
            await self._client.aclose()

    def _repo(self) -> AddressRepository:
        if self._repository is None:
            if self._client is None:
                raise RuntimeError(
                    "AddressService requires an httpx client or repository."
                )
            self._repository = AddressRepository(self._settings, self._client)
        return self._repository

    async def lookup_postcode(self, postcode: str) -> list[dict[str, Any]]:
        return await self._repo().fetch_by_postcode(postcode)

    async def resolve_address(self, *, postcode: str, address: str) -> ResolvedAddress:
        """End-to-end: fetch postcode records → match hint → BNG point."""
        records = await self.lookup_postcode(postcode)
        return find_matching_address(records, address=address, postcode=postcode)
