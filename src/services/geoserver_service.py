"""GeoServer WFS client for grit-bin proximity search.

Preferred path:
  CQL_FILTER=DWITHIN(SP_GEOMETRY, POINT(easting northing), radius, meters)

Fallback path (if DWITHIN fails — some GeoServer installs disable spatial
predicates or return XML exceptions):
  1. Fetch all grit-bin features
  2. Compute planar Euclidean distance in EPSG:27700
  3. Select the nearest feature within the radius
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import httpx

from src.config import Settings
from src.utils.coordinates import Point27700, euclidean_distance_meters
from src.utils.errors import (
    GeoServerUnreachableError,
    NoGritBinNearbyError,
    UnexpectedSchemaError,
)

logger = logging.getLogger(__name__)

GEOMETRY_FIELD = "SP_GEOMETRY"


@dataclass(frozen=True, slots=True)
class GritBinMatch:
    title: str
    distance_meters: float
    point: Point27700
    properties: dict[str, Any]


def _feature_title(feature: dict[str, Any]) -> str:
    props = feature.get("properties") or {}
    for key in ("Title", "title", "NAME", "name", "Subtitle"):
        if props.get(key):
            return str(props[key]).strip()
    # Fall back to GeoJSON feature id
    return str(feature.get("id") or "unknown")


def _feature_point(feature: dict[str, Any]) -> Point27700 | None:
    geometry = feature.get("geometry") or {}
    coords = geometry.get("coordinates")
    if (
        isinstance(coords, (list, tuple))
        and len(coords) >= 2
        and isinstance(coords[0], (int, float))
        and isinstance(coords[1], (int, float))
    ):
        return Point27700(easting=float(coords[0]), northing=float(coords[1]))
    return None


def _parse_feature_collection(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        raise UnexpectedSchemaError(
            "GeoServer",
            detail=f"Expected GeoJSON object, got {type(payload).__name__}.",
        )
    # GeoServer sometimes returns OGC exception XML parsed as text; detect that
    if "ExceptionReport" in payload or payload.get("type") == "Exception":
        raise UnexpectedSchemaError("GeoServer", detail="Received OGC exception.")

    features = payload.get("features")
    if features is None:
        raise UnexpectedSchemaError(
            "GeoServer", detail="Missing 'features' array in GeoJSON."
        )
    if not isinstance(features, list):
        raise UnexpectedSchemaError(
            "GeoServer", detail="'features' was not a list."
        )
    return features


def nearest_from_features(
    features: list[dict[str, Any]],
    origin: Point27700,
    *,
    radius_meters: float,
) -> GritBinMatch:
    """Pick the closest grit bin within radius using planar distance."""
    best: GritBinMatch | None = None

    for feature in features:
        point = _feature_point(feature)
        if point is None:
            continue
        distance = euclidean_distance_meters(origin, point)
        if distance > radius_meters:
            continue
        if best is None or distance < best.distance_meters:
            best = GritBinMatch(
                title=_feature_title(feature),
                distance_meters=distance,
                point=point,
                properties=dict(feature.get("properties") or {}),
            )

    if best is None:
        raise NoGritBinNearbyError(radius_meters)
    return best


class GeoServerService:
    """Async WFS client with DWITHIN + Euclidean fallback."""

    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self._settings = settings
        self._client = client
        self._owns_client = client is None

    async def __aenter__(self) -> GeoServerService:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._settings.http_timeout_seconds)
        return self

    async def __aexit__(self, *exc: object) -> None:
        if self._owns_client and self._client is not None:
            await self._client.aclose()

    def _base_params(self) -> dict[str, str]:
        return {
            "service": "WFS",
            "version": "1.0.0",
            "request": "GetFeature",
            "typeName": self._settings.geoserver_layer,
            "outputFormat": "application/json",
        }

    async def _get_features(self, params: dict[str, str]) -> list[dict[str, Any]]:
        assert self._client is not None
        try:
            response = await self._client.get(
                self._settings.geoserver_wfs_url,
                params=params,
            )
        except httpx.RequestError as exc:
            logger.warning("GeoServer request failed: %s", exc)
            raise GeoServerUnreachableError(str(exc)) from exc

        content_type = response.headers.get("content-type", "")
        if response.status_code >= 400:
            raise GeoServerUnreachableError(f"HTTP {response.status_code}")

        # GeoServer may return 200 with an XML ExceptionReport
        body_preview = response.text[:200].lstrip()
        if "ExceptionReport" in body_preview or (
            "xml" in content_type.lower() and "json" not in content_type.lower()
        ):
            raise UnexpectedSchemaError(
                "GeoServer",
                detail=body_preview[:160],
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise UnexpectedSchemaError(
                "GeoServer", detail="Response was not valid JSON."
            ) from exc

        return _parse_feature_collection(payload)

    async def query_dwithin(
        self,
        origin: Point27700,
        *,
        radius_meters: float,
    ) -> list[dict[str, Any]]:
        """Spatial filter via CQL DWITHIN around the origin point."""
        # WKT POINT uses "x y" = easting northing in the layer CRS (EPSG:27700)
        cql = (
            f"DWITHIN({GEOMETRY_FIELD}, "
            f"POINT({origin.easting} {origin.northing}), "
            f"{radius_meters}, meters)"
        )
        params = {**self._base_params(), "CQL_FILTER": cql}
        return await self._get_features(params)

    async def fetch_all_grit_bins(self) -> list[dict[str, Any]]:
        """Unfiltered GetFeature — used only as a DWITHIN fallback."""
        return await self._get_features(self._base_params())

    async def find_nearest(
        self,
        origin: Point27700,
        *,
        radius_meters: float | None = None,
    ) -> GritBinMatch:
        """Nearest grit bin within radius; DWITHIN first, Euclidean fallback."""
        radius = (
            radius_meters
            if radius_meters is not None
            else self._settings.nearest_search_radius_meters
        )

        features: list[dict[str, Any]] | None = None
        try:
            features = await self.query_dwithin(origin, radius_meters=radius)
            logger.info("DWITHIN returned %d feature(s)", len(features))
        except (GeoServerUnreachableError, UnexpectedSchemaError) as exc:
            logger.warning(
                "DWITHIN failed (%s); falling back to full fetch + Euclidean distance",
                exc,
            )
            features = await self.fetch_all_grit_bins()

        if not features:
            # Empty DWITHIN result is not an error from GeoServer — try fallback
            # only when we used DWITHIN, so we don't miss bins if the filter is
            # overly strict / CRS-mismatched. If fallback also empty → nearby error.
            logger.info("DWITHIN empty; attempting full-layer Euclidean fallback")
            try:
                features = await self.fetch_all_grit_bins()
            except (GeoServerUnreachableError, UnexpectedSchemaError):
                raise NoGritBinNearbyError(radius) from None

        return nearest_from_features(features, origin, radius_meters=radius)
