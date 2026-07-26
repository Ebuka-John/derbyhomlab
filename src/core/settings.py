"""Validated runtime settings loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    Missing required keys raise ValidationError at startup rather than failing
    later with an opaque HTTP 500 when an upstream call is made.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # tolerate unknown env keys without crashing
    )

    # --- Address Lookup API (credentialed; never hard-code tokens) ---
    address_api_base_url: str = Field(..., alias="ADDRESS_API_BASE_URL")
    address_api_alias: str = Field(..., alias="ADDRESS_API_ALIAS")
    address_api_auth_token: str = Field(..., alias="ADDRESS_API_AUTH_TOKEN")

    # --- GeoServer (public WFS host; layer name is configurable) ---
    geoserver_base_url: str = Field(..., alias="GEOSERVER_BASE_URL")
    geoserver_layer: str = Field(..., alias="GEOSERVER_LAYER")

    # Optional tuning — interview brief uses ~100 m
    nearest_search_radius_meters: float = Field(
        100.0, alias="NEAREST_SEARCH_RADIUS_METERS"
    )
    http_timeout_seconds: float = Field(30.0, alias="HTTP_TIMEOUT_SECONDS")

    @field_validator(
        "address_api_base_url",
        "geoserver_base_url",
        mode="before",
    )
    @classmethod
    def strip_trailing_slash(cls, value: str) -> str:
        # Prevent double-slash bugs when we append path segments later
        if isinstance(value, str):
            return value.rstrip("/")
        return value

    @property
    def address_api_headers(self) -> dict[str, str]:
        """Auth headers required by Derbyshire Address Lookup API."""
        return {
            "x-alias": self.address_api_alias,
            "x-auth-token": self.address_api_auth_token,
            "Accept": "application/json",
        }

    @property
    def geoserver_wfs_url(self) -> str:
        """WFS GetFeature endpoint for the DCC workspace.

        Hostname may say ``wms.`` but we call **WFS** (features), not WMS (tiles).
        Path ``/DCC/ows`` is the DCC workspace OWS entry point.
        """
        return f"{self.geoserver_base_url}/DCC/ows"


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton — load .env once per process."""
    return Settings()
