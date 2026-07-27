"""UK postcode format checks (format only — not a live delivery-point check)."""

from __future__ import annotations

import re

from src.utils.exceptions import InvalidPostcodeError

# Outward + optional space + inward (unit). Covers common UK shapes including GIR 0AA.
_UK_POSTCODE_RE = re.compile(
    r"^(GIR\s*0AA|[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})$",
    re.IGNORECASE,
)


def normalise_postcode(postcode: str) -> str:
    """Collapse internal whitespace and upper-case (``de55  5pb`` → ``DE55 5PB``)."""
    return " ".join(postcode.split()).upper()


def require_valid_uk_postcode(postcode: str) -> str:
    """Return a normalised postcode or raise ``InvalidPostcodeError``."""
    cleaned = normalise_postcode(postcode)
    if not cleaned or not _UK_POSTCODE_RE.match(cleaned):
        raise InvalidPostcodeError(postcode)
    return cleaned
