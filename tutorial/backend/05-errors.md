# Backend Step 5 — Typed errors

## What you will do

1. Create the file below.
2. Type the code carefully (or type section by section).
3. Run the checkpoint before continuing.

## File to create: `src/utils/errors.py`

**Path:** `src/utils/errors.py`

### Purpose

Defines domain exceptions with HTTP status codes and machine-readable error codes. FastAPI will map these to consistent JSON bodies.

### Type this exactly

```python
"""Domain-specific exception hierarchy for clean FastAPI error mapping.

Each exception carries a machine-readable `code` and a human-readable message
so the API can return consistent JSON error bodies without leaking stack traces.
"""

from __future__ import annotations


class AppError(Exception):
    """Base application error with HTTP status and stable error code."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "app_error",
        status_code: int = 500,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class MissingParameterError(AppError):
    def __init__(self, parameter: str) -> None:
        super().__init__(
            f"Missing required query parameter: '{parameter}'.",
            code="missing_parameter",
            status_code=400,
        )


class AddressApiUnreachableError(AppError):
    def __init__(self, detail: str | None = None) -> None:
        message = "Address Lookup API is unreachable."
        if detail:
            message = f"{message} {detail}"
        super().__init__(
            message,
            code="address_api_unreachable",
            status_code=502,
        )


class AddressNotFoundError(AppError):
    """No addresses returned for the given postcode."""

    def __init__(self, postcode: str) -> None:
        super().__init__(
            f"No addresses found for postcode '{postcode}'.",
            code="address_not_found",
            status_code=404,
        )


class TargetAddressNotFoundError(AppError):
    """Postcode resolved, but no Title matched the address parameter."""

    def __init__(self, address: str, postcode: str) -> None:
        super().__init__(
            f"Address '{address}' was not found within postcode '{postcode}'.",
            code="target_address_not_found",
            status_code=404,
        )


class UnexpectedSchemaError(AppError):
    def __init__(self, source: str, detail: str | None = None) -> None:
        message = f"Unexpected response schema from {source}."
        if detail:
            message = f"{message} {detail}"
        super().__init__(
            message,
            code="unexpected_schema",
            status_code=502,
        )


class GeoServerUnreachableError(AppError):
    def __init__(self, detail: str | None = None) -> None:
        message = "GeoServer WFS is unreachable."
        if detail:
            message = f"{message} {detail}"
        super().__init__(
            message,
            code="geoserver_unreachable",
            status_code=502,
        )


class NoGritBinNearbyError(AppError):
    def __init__(self, radius_meters: float) -> None:
        super().__init__(
            f"No grit bin found within {radius_meters:g} metres of the address.",
            code="no_grit_bin_nearby",
            status_code=404,
        )


class CoordinateConversionError(AppError):
    def __init__(self, detail: str) -> None:
        super().__init__(
            f"Coordinate conversion failed: {detail}",
            code="coordinate_conversion_error",
            status_code=502,
        )
```

### How the code works

#### Concepts in this file (OOP inheritance)

Think of errors as a **family tree**:

```
Exception          ← Python’s built-in base
   └── AppError    ← our base (adds message, code, status_code)
         ├── MissingParameterError      (400)
         ├── AddressNotFoundError       (404)
         ├── NoGritBinNearbyError       (404)
         ├── AddressApiUnreachableError (502)
         └── …
```

| Concept | Where | Plain meaning |
|---------|-------|---------------|
| **Inheritance** | `class MissingParameterError(AppError)` | Child error **is an** AppError. One FastAPI handler can catch them all. |
| **`__init__`** | constructor | Runs when you write `MissingParameterError("postcode")`. |
| **`self`** | `self.message = message` | Stores data on **this** error object. |
| **`super().__init__(...)`** | first line in child `__init__` | Call the parent constructor so shared fields are set correctly. |
| **Keyword-only args** | `*, code=..., status_code=...` | The `*` means callers must name those arguments (`code="…"`), which avoids mix-ups. |
| **`raise`** | (used later in services) | Throw this error up the call stack until something handles it. |

#### Why this design

Without typed errors, every function invents its own failure message. With this
hierarchy:

1. Services `raise TargetAddressNotFoundError(...)` when matching fails.
2. FastAPI’s exception handler (in `app.py`) catches **any** `AppError`.
3. The client always gets JSON like `{"error": {"code": "…", "message": "…"}}`.

HTTP status cheat sheet:

| Code | Meaning in this app |
|------|---------------------|
| 400 | Bad input (you forgot a parameter) |
| 404 | Not found (address / grit bin) |
| 502 | Upstream failed (Address API or GeoServer) |

> Primer: [00-python-fastapi-basics.md](./00-python-fastapi-basics.md) §§3 and 7.

## Checkpoint

```powershell
python -c "from src.utils.errors import MissingParameterError as E; e=E('postcode'); print(e.status_code, e.code)"
```
Expected: `400 missing_parameter`

## Next

→ [06-coordinates.md](./06-coordinates.md)
