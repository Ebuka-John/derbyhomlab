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
