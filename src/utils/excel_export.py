"""One-shot Excel export helpers (local utility — not part of the exercise)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from openpyxl import Workbook

from src.models.domain.gritbin import GritBin

# Writable for both local venv and Docker non-root ``app`` user.
DEFAULT_EXPORT_PATH = Path(tempfile.gettempdir()) / "gritbins.xlsx"

# GeoServer DCC:Gritbins has street/town text, but no UK postcode attribute.
_POSTCODE_KEYS = ("Postcode", "postcode", "Post_Code", "POSTCODE", "PostCode")


def _prop(props: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = props.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def _address_from_properties(props: dict[str, Any]) -> str:
    """Best-effort human address from layer attributes (no postcode on this layer)."""
    subtitle = _prop(props, "Subtitle")
    if subtitle:
        return subtitle
    parts = [
        _prop(props, "Street_Name"),
        _prop(props, "Town_Name"),
        _prop(props, "Area_Name"),
    ]
    return ", ".join(p for p in parts if p)


def _postcode_from_properties(props: dict[str, Any]) -> str:
    """Postcode if present on the feature; DCC:Gritbins currently has none."""
    return _prop(props, *_POSTCODE_KEYS)


def write_grit_bins_excel(bins: list[GritBin], path: Path) -> Path:
    """Write grit bins to ``.xlsx`` (title, address fields, BNG coords).

    ``address`` comes from ``Subtitle`` / street+town. ``postcode`` is blank for
    this Derbyshire layer (attribute not published on WFS).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "gritbins"
    sheet.append(
        [
            "title",
            "address",
            "postcode",
            "street_name",
            "town_name",
            "area_name",
            "location_description",
            "easting",
            "northing",
            "usrn",
        ]
    )
    for grit_bin in bins:
        props = grit_bin.properties or {}
        sheet.append(
            [
                grit_bin.title,
                _address_from_properties(props),
                _postcode_from_properties(props),
                _prop(props, "Street_Name"),
                _prop(props, "Town_Name"),
                _prop(props, "Area_Name"),
                _prop(props, "Location_Description"),
                grit_bin.point.easting,
                grit_bin.point.northing,
                _prop(props, "USRN"),
            ]
        )
    workbook.save(path)
    return path.resolve()
