# 2 — What you are building

## Concept (30 seconds)

User enters a **postcode** + **address hint**. The backend:

1. Calls Derbyshire **Address Lookup API** → finds the address → gets coordinates.
2. Queries **GeoServer WFS** for grit bins near that point (`DWITHIN` on `SP_GEOMETRY`).
3. Returns the nearest bin title(s) and distance in **metres** (EPSG:27700).

The frontend is a thin UI. The browser only talks to Next.js; Next.js **proxies**
to FastAPI so secrets and upstream calls stay server-side.

```text
Browser → Next.js (:3000) → FastAPI (:8000) → Address API
                                          └→ GeoServer WFS
```

## Backend layers (why folders exist)

```text
Router  →  Service  →  Repository  →  External HTTP
 (HTTP)     (rules)     (HTTP only)
```

- **Routers** — query params, status codes, response models (FastAPI).
- **Services** — match address, pick nearest bin (no FastAPI imports).
- **Repositories** — talk to Address API / GeoServer only.
- **Domain / DTO** — internal shapes vs API JSON shapes.
- **core / utils** — settings, errors, CRS helpers.

## Interview fixture (for live checks later)

- Postcode `DE55 5PB`, address `HILLBROW` → grit bin **GB0199** (~49 m).  
  Use generic placeholders in code comments; use the real pair when testing.

## Deeper reading (`main`)

- [01-introduction.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/01-introduction.md), [02-architecture.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/02-architecture.md)
- [10-spatial-querying.md](https://github.com/Ebuka-John/derbyhomlab/blob/main/tutorial/10-spatial-querying.md)
- This branch: [G11_Interview_Rivision_Notes.md](../lfdocs/G11_Interview_Rivision_Notes.md), [copilotdocs.md](../lfdocs/copilotdocs.md)

## Checkpoint

Do **not** continue to the next lesson until this passes.


Sketch from memory (paper or a PyCharm scratch file):

`Browser → Next proxy → FastAPI → Address API + GeoServer → JSON back`

Then open [backend/README.md](./backend/README.md).

---

| Previous | Next |
|:---------|-----:|
| ← [PyCharm setup](./01-pycharm-setup.md) | [Backend lab](./backend/README.md) → |
