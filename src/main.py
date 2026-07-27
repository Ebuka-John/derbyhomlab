"""Process entrypoint — starts uvicorn with the FastAPI app."""

from __future__ import annotations

import uvicorn

from src.app import app

__all__ = ["app"]


def run() -> None:
    """Block and serve the ASGI app."""
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    run()
