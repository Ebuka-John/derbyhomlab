"""Grit-bin proximity business logic (no FastAPI imports).

Preferred path: server-side CQL DWITHIN (spatial index on GeoServer).
Fallback: fetch the layer and pick nearest with planar Euclidean distance —
live installs sometimes disable spatial predicates or return empty filters.
"""

from __future__ import annotations

import logging

import httpx

from src.core.settings import Settings
from src.models.domain.geometry import Point27700
from src.models.domain.gritbin import GritBinMatch
from src.repositories.gritbin_repository import GritBinRepository
from src.utils.exceptions import (
    GeoServerUnreachableError,
    NoGritBinNearbyError,
    UnexpectedSchemaError,
)
from src.utils.geospatial import nearest_from_features

logger = logging.getLogger(__name__)


class GritBinService:
    """Finds the nearest grit bin within a radius (DWITHIN + Euclidean fallback)."""

    def __init__(
        self,
        settings: Settings,
        client: httpx.AsyncClient | None = None,
        *,
        repository: GritBinRepository | None = None,
    ) -> None:
        self._settings = settings
        self._client = client
        self._owns_client = client is None and repository is None
        self._repository = repository

    async def __aenter__(self) -> GritBinService:
        if self._repository is None:
            if self._client is None:
                self._client = httpx.AsyncClient(
                    timeout=self._settings.http_timeout_seconds
                )
            self._repository = GritBinRepository(self._settings, self._client)
        return self

    async def __aexit__(self, *exc: object) -> None:
        if self._owns_client and self._client is not None:
            await self._client.aclose()

    def _repo(self) -> GritBinRepository:
        if self._repository is None:
            if self._client is None:
                raise RuntimeError(
                    "GritBinService requires an httpx client or repository."
                )
            self._repository = GritBinRepository(self._settings, self._client)
        return self._repository

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
        repo = self._repo()

        features: list | None = None
        try:
            # Happy path: GeoServer filters with its spatial index
            features = await repo.query_dwithin(origin, radius_meters=radius)
            logger.info("DWITHIN returned %d feature(s)", len(features))
        except (GeoServerUnreachableError, UnexpectedSchemaError) as exc:
            # XML ExceptionReport / disabled spatial ops → download and measure
            logger.warning(
                "DWITHIN failed (%s); falling back to full fetch + Euclidean distance",
                exc,
            )
            features = await repo.fetch_all()

        if not features:
            # Empty DWITHIN is not always "no bins" — CRS mismatches can zero it out
            logger.info("DWITHIN empty; attempting full-layer Euclidean fallback")
            try:
                features = await repo.fetch_all()
            except (GeoServerUnreachableError, UnexpectedSchemaError):
                raise NoGritBinNearbyError(radius) from None

        return nearest_from_features(features, origin, radius_meters=radius)
