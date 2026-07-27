/** FastAPI base URL for Route Handlers (server-side only). */
export function backendBaseUrl(): string {
  return process.env.BACKEND_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";
}
