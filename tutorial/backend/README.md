# Backend lab (FastAPI) — type-along

Work in your **lab** PyCharm project. For every file, open the same path in the
**reference** window (`readytosubmit`) and type it into the lab.

**Rule:** finish a lesson → run its **Checkpoint** → only then start the next
lesson. Do not batch-type steps 1–8 and hope step 9 will reveal every mistake.

## Order

| Step | Lesson | You create |
|-----:|--------|------------|
| 1 | [01-requirements-env.md](./01-requirements-env.md) | `requirements*.txt`, `.env*` |
| 2 | [02-packages.md](./02-packages.md) | `src/` package tree + `__init__.py` |
| 3 | [03-config.md](./03-config.md) | settings, logging, `config.py` |
| 4 | [04-errors-utils.md](./04-errors-utils.md) | exceptions, postcode |
| 5 | [05-models.md](./05-models.md) | domain + DTO + geospatial |
| 6 | [06-repositories.md](./06-repositories.md) | Address + grit-bin HTTP |
| 7 | [07-services.md](./07-services.md) | Address + grit-bin business logic |
| 8 | [08-api-app.md](./08-api-app.md) | deps, routers, `app.py`, `main.py` |
| 9 | [09-run.md](./09-run.md) | Run uvicorn + hit `/docs` |

```text
settings + exceptions + postcode
        ↓
   domain + geospatial + DTOs
        ↓
    repositories
        ↓
      services
        ↓
   routers + app
```

## PyCharm habits

- New package: right-click parent → `New → Python Package` (creates `__init__.py`).
- New module: `New → Python File`.
- After the last file in a lesson: run the Checkpoint in the Terminal before
  clicking Next.
- Run configs later: `uvicorn` module or a Shell Script configuration.

## Deeper reading (`main`)

- [00-backend-design.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/backend/00-backend-design.md)
- [00-python-fastapi-basics.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/backend/00-python-fastapi-basics.md)
- Full numbered lessons under [tutorial/backend/ (main)](https://github.com/Ebuka-John/derbyhomlab/tree/main/tutorial/backend) (embedded code on `main`; **your** code comes from this branch’s `src/`)
- Design patterns (panel): [lfdocs/copilotdocs.md](../lfdocs/copilotdocs.md) § Design patterns

Start → [01-requirements-env.md](./01-requirements-env.md)

---

| Previous | Next |
|:---------|-----:|
| ← [Overview](../02-overview.md) | [Requirements & env](./01-requirements-env.md) → |
