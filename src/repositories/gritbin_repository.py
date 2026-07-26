"""GeoServer WFS data access for grit-bin features (HTTP only)."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from src.core.settings import Settings
from src.models.domain.geometry import Point27700
from src.utils.exceptions import GeoServerUnreachableError, UnexpectedSchemaError

logger = logging.getLogger(__name__)

# Geometry column name on DCC:Gritbins (discovered via GetFeature / DescribeFeatureType).
# Do NOT use GeoServer's common default ``the_geom`` — this layer uses SP_GEOMETRY.
GEOMETRY_FIELD = "SP_GEOMETRY"


def parse_feature_collection(payload: Any) -> list[dict[str, Any]]:
    """Validate GeoJSON FeatureCollection (or detect OGC exception payloads)."""
    if not isinstance(payload, dict):
        raise UnexpectedSchemaError(
            "GeoServer",
            detail=f"Expected GeoJSON object, got {type(payload).__name__}.",
        )
    # Some servers return exception-like JSON instead of features
    if "ExceptionReport" in payload or payload.get("type") == "Exception":
        raise UnexpectedSchemaError("GeoServer", detail="Received OGC exception.")

    features = payload.get("features")
    if features is None:
        raise UnexpectedSchemaError(
            "GeoServer", detail="Missing 'features' array in GeoJSON."
        )
    if not isinstance(features, list):
        raise UnexpectedSchemaError("GeoServer", detail="'features' was not a list.")
    return features


class GritBinRepository:
    """Fetches grit-bin GeoJSON features from Derbyshire GeoServer WFS.

    Builds the GetFeature URL:
      {GEOSERVER_BASE_URL}/DCC/ows?service=WFS&version=1.0.0&request=GetFeature&...
    """

    def __init__(self, settings: Settings, client: httpx.AsyncClient) -> None:
        self._settings = settings
        self._client = client

    def _base_params(self) -> dict[str, str]:
        """Standard WFS GetFeature query string (no spatial filter yet)."""
        return {
            "service": "WFS",  # features, not WMS map images
            "version": "1.0.0",
            "request": "GetFeature",
            "typeName": self._settings.geoserver_layer,  # e.g. DCC:Gritbins
            "outputFormat": "application/json",
        }

    async def _get_features(self, params: dict[str, str]) -> list[dict[str, Any]]:
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

        # GeoServer often returns HTTP 200 with an XML ExceptionReport body
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

        return parse_feature_collection(payload)

    async def query_dwithin(
        self,
        origin: Point27700,
        *,
        radius_meters: float,
    ) -> list[dict[str, Any]]:
        """Server-side spatial filter: features within radius metres of origin.

        WKT POINT uses ``x y`` = easting northing in the layer CRS (EPSG:27700).
        """
        cql = (
            f"DWITHIN({GEOMETRY_FIELD}, "
            f"POINT({origin.easting} {origin.northing}), "
            f"{radius_meters}, meters)"
        )
        params = {**self._base_params(), "CQL_FILTER": cql}
        return await self._get_features(params)

    async def fetch_all(self) -> list[dict[str, Any]]:
        """Unfiltered GetFeature — used only when DWITHIN fails or returns empty."""
        return await self._get_features(self._base_params())
