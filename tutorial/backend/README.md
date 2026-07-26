# Backend lab (FastAPI)

Type these files **in order**. Each step is one lesson file.

Work from your **project root** (the folder that will contain `src/`, `.env`, and
`requirements.txt`).

## New to Python or FastAPI?

Read this short primer first — classes, async, decorators, and FastAPI in plain
language:

→ **[00-python-fastapi-basics.md](./00-python-fastapi-basics.md)**

Later steps also explain concepts **inline** where they first appear.

## TYPE THESE FILES IN ORDER

| Step | Lesson file | You create |
|-----:|-------------|------------|
| 0 | [00-python-fastapi-basics.md](./00-python-fastapi-basics.md) | *(read only)* |
| 1 | [01-requirements.md](./01-requirements.md) | `requirements.txt`, `requirements-dev.txt`, venv |
| 2 | [02-env.md](./02-env.md) | `.env.example`, `.env` |
| 3 | [03-init-packages.md](./03-init-packages.md) | `src/__init__.py` (+ services/utils packages) |
| 4 | [04-config.md](./04-config.md) | `src/config.py` |
| 5 | [05-errors.md](./05-errors.md) | `src/utils/errors.py` |
| 6 | [06-coordinates.md](./06-coordinates.md) | `src/utils/coordinates.py` |
| 7 | [07-address-service.md](./07-address-service.md) | `src/services/address_service.py` |
| 8 | [08-geoserver-service.md](./08-geoserver-service.md) | `src/services/geoserver_service.py` |
| 9 | [09-app.md](./09-app.md) | `src/app.py` |
| 10 | [10-run-and-test.md](./10-run-and-test.md) | Run uvicorn + hit `/docs` |

## Before you start

1. Create an empty project folder by hand (e.g. `grit-bin-lab`) wherever you keep code.
2. Open that folder in your editor.
3. Open a terminal in that folder.

Every folder and file in this lab is created **manually** in the editor — you type
the filenames and the code yourself. Terminal commands are only used for real
actions like installing packages and starting the server.

Then open **[00-python-fastapi-basics.md](./00-python-fastapi-basics.md)** (or skip
straight to [01-requirements.md](./01-requirements.md) if you already know Python OOP).

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Environment variables](../04-environment-variables.md) | [Python / FastAPI basics](./00-python-fastapi-basics.md) → |
