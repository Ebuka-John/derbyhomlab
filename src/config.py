"""Public configuration entrypoint (re-exports from ``core.settings``)."""

from src.core.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
