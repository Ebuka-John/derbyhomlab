"""Process entrypoint — starts uvicorn with the FastAPI app.

Prefer:
  uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

Or:
  python -m src.main
"""

from __future__ import annotations

import uvicorn

from src.app import app

__all__ = ["app"]


def run() -> None:
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    run()
