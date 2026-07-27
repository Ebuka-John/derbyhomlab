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
    """400 — missing required query parameter."""

    def __init__(self, parameter: str) -> None:
        super().__init__(
            f"Missing required query parameter: '{parameter}'.",
            code="missing_parameter",
            status_code=400,
        )


class AddressApiUnreachableError(AppError):
    """502 — Address Lookup API unreachable."""

    def __init__(self, detail: str | None = None) -> None:
        message = "Address Lookup API is unreachable."
        if detail:
            message = f"{message} {detail}"
        super().__init__(
            message,
            code="address_api_unreachable",
            status_code=502,
        )


class InvalidPostcodeError(AppError):
    """400 — invalid postcode format or upstream rejection."""

    def __init__(self, postcode: str, detail: str | None = None) -> None:
        message = f"Invalid postcode '{postcode}'."
        if detail:
            message = f"{message} {detail}"
        super().__init__(
            message,
            code="invalid_postcode",
            status_code=400,
        )


class AddressNotFoundError(AppError):
    """404 — no address records for postcode."""

    def __init__(self, postcode: str) -> None:
        super().__init__(
            f"No addresses found for postcode '{postcode}'.",
            code="address_not_found",
            status_code=404,
        )


class TargetAddressNotFoundError(AppError):
    """404 — postcode OK, but address hint did not match."""

    def __init__(self, address: str, postcode: str) -> None:
        super().__init__(
            f"Address '{address}' was not found within postcode '{postcode}'.",
            code="target_address_not_found",
            status_code=404,
        )


class UnexpectedSchemaError(AppError):
    """502 — unexpected upstream JSON/XML shape."""

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
    """502 — GeoServer WFS unreachable."""

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
    """404 — no grit bin matched the search."""

    def __init__(self, radius_meters: float | None = None) -> None:
        if radius_meters is None:
            message = "No grit bins found near the address."
        else:
            message = (
                f"No grit bin found within {radius_meters:g} metres of the address."
            )
        super().__init__(
            message,
            code="no_grit_bin_nearby",
            status_code=404,
        )


class CoordinateConversionError(AppError):
    """502 — CRS conversion failed or coords missing/ambiguous."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            f"Coordinate conversion failed: {detail}",
            code="coordinate_conversion_error",
            status_code=502,
        )
