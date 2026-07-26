# Backend Step 4 — Config

## What you will do

1. Create the file below.
2. Type the code carefully (or type section by section).
3. Run the checkpoint before continuing.

## File to create: `src/config.py`

**Path:** `src/config.py`

### Purpose

Loads and validates environment variables. Builds Address API headers and the GeoServer WFS URL. Fails fast at startup if required keys are missing.

### Type this exactly

```python
"""Application configuration loaded from environment variables.

All sensitive values (API base URLs, auth headers, layer names) are read
from a `.env` file via python-dotenv / pydantic-settings. Nothing is hard-coded
so the same codebase can target local, staging, or production without edits.
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated runtime configuration.

    Missing required keys raise a clear ValidationError at startup rather than
    failing later with an opaque HTTP 500 when an external call is made.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Address Lookup API
    address_api_base_url: str = Field(..., alias="ADDRESS_API_BASE_URL")
    address_api_alias: str = Field(..., alias="ADDRESS_API_ALIAS")
    address_api_auth_token: str = Field(..., alias="ADDRESS_API_AUTH_TOKEN")

    # GeoServer WFS
    geoserver_base_url: str = Field(..., alias="GEOSERVER_BASE_URL")
    geoserver_layer: str = Field(..., alias="GEOSERVER_LAYER")

    # Tuning (optional with sensible defaults)
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
        """Normalise base URLs so path joins never produce double slashes."""
        if isinstance(value, str):
            return value.rstrip("/")
        return value

    @property
    def address_api_headers(self) -> dict[str, str]:
        """Reusable auth headers for every Address API call."""
        return {
            "x-alias": self.address_api_alias,
            "x-auth-token": self.address_api_auth_token,
            "Accept": "application/json",
        }

    @property
    def geoserver_wfs_url(self) -> str:
        """WFS GetFeature endpoint for the DCC workspace.

        GeoServer convention: {base}/DCC/ows for the DCC workspace.
        Layer name still uses the fully-qualified typeName (e.g. DCC:Gritbins).
        """
        return f"{self.geoserver_base_url}/DCC/ows"


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton — load .env once per process."""
    return Settings()
```

### How the code works

#### Concepts in this file

| Concept | Where you see it | Plain meaning |
|---------|------------------|---------------|
| **Class** | `class Settings(BaseSettings)` | A blueprint for config. One `Settings` object holds all env values. |
| **Inheritance** | `Settings(BaseSettings)` | We extend Pydantic’s `BaseSettings` so we get “read from env + validate” for free. |
| **Type hints** | `address_api_base_url: str` | Notes saying “this should be a string”. Pydantic uses them to validate. |
| **`Field(...)`** | required vs optional fields | `...` means **required**. A default like `100.0` means optional. |
| **`alias=`** | `alias="ADDRESS_API_BASE_URL"` | Env vars are UPPER_SNAKE; Python prefers `snake_case`. Alias maps them. |
| **Decorator** | `@field_validator`, `@property`, `@lru_cache` | Stickers that change how a function/method behaves. |
| **`@classmethod`** | `def strip_trailing_slash(cls, …)` | Runs on the **class**, not one instance. `cls` is like `self` for the class. |
| **`@property`** | `address_api_headers` | Lets you write `settings.address_api_headers` (no parentheses) but still run code. |
| **`@lru_cache`** | `get_settings` | Remembers the result. Second call reuses the same `Settings` object. |

#### What the code is doing

1. `Settings` reads `.env` when you create it (`Settings()`).
2. If a required key is missing, Pydantic raises a clear error at **startup** — better than a mysterious failure later.
3. `strip_trailing_slash` cleans URLs so `https://host/` + `/path` never becomes `https://host//path`.
4. The two `@property` helpers build headers and the WFS URL in **one place**, so services stay simple.
5. `get_settings()` is the public entry point: call it anywhere; the cache means you only load `.env` once.

> New to classes? See [00-python-fastapi-basics.md](./00-python-fastapi-basics.md) §§3–5.

## Checkpoint

```powershell
python -c "from src.config import get_settings; print(get_settings().geoserver_wfs_url)"
```
You should see your GeoServer base URL with `/DCC/ows` appended.

## Next

→ [05-errors.md](./05-errors.md)
