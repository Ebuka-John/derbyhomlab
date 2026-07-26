# Frontend Step 1 — Scaffold

## What you will do

1. Create the `frontend/` folder tree with PowerShell.
2. Create empty config files with PowerShell, then type their contents.
3. Install Node dependencies.

## Folders to create

From the **project root**, run:

```powershell
New-Item -ItemType Directory -Force -Path `
  frontend,
  frontend\app,
  frontend\app\api,
  frontend\app\api\nearest-grit-bin,
  frontend\components,
  frontend\lib,
  frontend\public | Out-Null
```

Confirm:

```powershell
Get-ChildItem -Recurse frontend -Directory | Select-Object FullName
```

The result should look like this:

```
your-project/
├── src/
└── frontend/
    ├── app/
    │   └── api/
    │       └── nearest-grit-bin/
    ├── components/
    ├── lib/
    └── public/
```

> The folder name `nearest-grit-bin` matters — Next.js turns that path into the
> URL `/api/nearest-grit-bin`. Type it exactly, with hyphens.

---

## File to create: `frontend/package.json`

### Create it in PowerShell (project root)

```powershell
New-Item -ItemType File -Force -Path frontend\package.json | Out-Null
```

Open `frontend/package.json` in your editor and **type this exactly:**

```json
{
  "name": "nearest-grit-bin-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev --port 3000",
    "build": "next build",
    "start": "next start --port 3000",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^15.3.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@types/node": "^22.13.10",
    "@types/react": "^19.0.10",
    "@types/react-dom": "^19.0.4",
    "typescript": "^5.8.2"
  }
}
```

---

## File to create: `frontend/tsconfig.json`

### Create it in PowerShell (project root)

```powershell
New-Item -ItemType File -Force -Path frontend\tsconfig.json | Out-Null
```

Open `frontend/tsconfig.json` and **type this exactly:**

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": false,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### Why `@/*`

Lets you write `import … from "@/lib/types"` instead of long relative paths.

---

## File to create: `frontend/next.config.ts`

### Create it in PowerShell (project root)

```powershell
New-Item -ItemType File -Force -Path frontend\next.config.ts | Out-Null
```

Open `frontend/next.config.ts` and **type this exactly:**

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Enables a minimal Node server image for Docker (copies .next/standalone)
  output: "standalone",
};

export default nextConfig;
```

---

## Commands to run now

```powershell
Set-Location frontend
npm install
Set-Location ..
```

## Checkpoint

```powershell
Test-Path frontend\node_modules
Test-Path frontend\package-lock.json
```

- `frontend/node_modules` exists
- No install errors

---

<!-- tutorial-nav -->

| Previous | Next |
|:---------|-----:|
| ← [Frontend lab](./README.md) | [Frontend env](./02-env.md) → |
