"""Grit-bin proximity business logic (no FastAPI imports)."""

from __future__ import annotations

import logging

import httpx

from src.core.settings import Settings
from src.models.domain.geometry import Point27700
from src.models.domain.gritbin import GritBin, GritBinMatch
from src.repositories.gritbin_repository import GritBinRepository
from src.utils.exceptions import (
    GeoServerUnreachableError,
    NoGritBinNearbyError,
    UnexpectedSchemaError,
)
from src.utils.geospatial import (
    feature_point,
    feature_title,
    nearest_from_features,
    nearest_n_from_features,
)

logger = logging.getLogger(__name__)


class GritBinService:
    """Finds nearest grit bin(s) within a radius (DWITHIN + Euclidean fallback)."""

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

    async def _candidate_features(
        self,
        origin: Point27700,
        *,
        radius: float,
    ) -> list:
        """DWITHIN first; on failure or empty result, full-layer fetch."""
        repo = self._repo()
        features: list | None = None
        try:
            features = await repo.query_dwithin(origin, radius_meters=radius)
            logger.info("DWITHIN returned %d feature(s)", len(features))
        except (GeoServerUnreachableError, UnexpectedSchemaError) as exc:
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

        return features

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
        features = await self._candidate_features(origin, radius=radius)
        return nearest_from_features(features, origin, radius_meters=radius)

    async def find_nearest_n(
        self,
        origin: Point27700,
        *,
        limit: int = 5,
        radius_meters: float | None = None,
    ) -> list[GritBinMatch]:
        """Nearest ``limit`` grit bins within radius (default: settings / 100 m)."""
        if limit < 1:
            raise ValueError("limit must be >= 1")

        radius = (
            radius_meters
            if radius_meters is not None
            else self._settings.nearest_search_radius_meters
        )
        features = await self._candidate_features(origin, radius=radius)
        return nearest_n_from_features(
            features,
            origin,
            limit=limit,
            radius_meters=radius,
        )

    async def list_all(self) -> list[GritBin]:
        """Return every grit bin from the WFS layer."""
        features = await self._repo().fetch_all()
        bins: list[GritBin] = []
        for feature in features:
            point = feature_point(feature)
            if point is None:
                continue
            bins.append(
                GritBin(
                    title=feature_title(feature),
                    point=point,
                    properties=dict(feature.get("properties") or {}),
                )
            )
        return bins
