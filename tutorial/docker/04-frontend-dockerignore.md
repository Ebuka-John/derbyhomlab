# Docker Step 4 — Frontend .dockerignore

## What you will do

Create `frontend/.dockerignore` in your editor, then type its
contents so local `node_modules` and build output are not sent into the frontend
image build context.

## File to create: `frontend/.dockerignore`

**Path:** `frontend/.dockerignore`

### Create this file in the editor

Create `frontend/.dockerignore` in your editor (from the project root), then type the contents below yourself.

### Purpose

The image installs its own dependencies inside the container. Copying your host
`node_modules` would slow the build and can break on OS mismatches (Windows host
vs Linux container).

### Type this exactly

```text
Dockerfile
.dockerignore
node_modules
.next
.git
.gitignore
*.md
.env*.local
npm-debug.log*
.DS_Store
```

### How the code works

- `node_modules` / `.next` — recreated inside the image; never copy from the host
- `.env*.local` — local secrets stay off the image (Compose sets `BACKEND_URL`)
- `*.md` — docs are not needed at runtime

## Checkpoint

Confirm the file sits next to `frontend/Dockerfile` and `frontend/package.json`.

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Frontend Dockerfile](./03-frontend-dockerfile.md) | [Compose](./05-compose.md) → |
