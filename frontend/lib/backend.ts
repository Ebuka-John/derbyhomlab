/**
 * Shared FastAPI base URL for Next.js Route Handlers.
 * Kept server-side so the browser never sees BACKEND_URL.
 */
export function backendBaseUrl(): string {
  return process.env.BACKEND_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";
}
