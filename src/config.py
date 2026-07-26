"""Public configuration entrypoint.

Re-exports settings from ``core.settings`` so callers can use
``from src.config import Settings, get_settings``.
"""

from src.core.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
