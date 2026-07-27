# Backend Step 5 — Typed errors

## What you will do

1. Create the empty file in your editor.
2. Open it and type the code carefully (or section by section).
3. Activate the venv and run the checkpoint before continuing.

## File to create: `src/utils/exceptions.py`

**Path:** `src/utils/exceptions.py`

### Create this file in the editor

Create `src/utils/exceptions.py` in your editor (from the project root), then type the contents below yourself.

### Purpose

Defines domain exceptions with HTTP status codes and machine-readable error codes. FastAPI will map these to consistent JSON bodies via a handler in `app.py`.

### Type this exactly

```python
"""Domain and application exception hierarchy."""

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
    """Postcode resolved, but no record matched the address parameter."""

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
| **Inheritance** | `class MissingParameterError(AppError)` | Child error **is an** `AppError`. One FastAPI handler catches them all. |
| **`super().__init__(...)`** | child constructors | Run the parent constructor so shared fields are set correctly. |
| **`raise`** | (used later in services) | Throw this error up the stack until something handles it. |

Without typed errors, every function invents its own failure message. With this hierarchy:

1. Services `raise TargetAddressNotFoundError(...)` when matching fails.
2. FastAPI’s exception handler (in `app.py`) catches **any** `AppError`.
3. The client always gets JSON like `{"error": {"code": "…", "message": "…"}}`.

HTTP status cheat sheet:

| Code | Meaning in this app |
|------|---------------------|
| 400 | Bad input (missing query parameter) |
| 404 | Not found (address / grit bin) |
| 502 | Upstream failed (Address API or GeoServer) |

> Primer: [00-python-fastapi-basics.md](./00-python-fastapi-basics.md) §§3 and 7.

## Checkpoint

```powershell
.\.venv\Scripts\Activate.ps1
python -c "from src.utils.exceptions import MissingParameterError as E; e=E('postcode'); print(e.status_code, e.code)"
```

Expected: `400 missing_parameter`

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Config](./04-config.md) | [Coordinates](./06-coordinates.md) → |
