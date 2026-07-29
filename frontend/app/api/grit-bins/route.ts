import { NextResponse } from "next/server";

import { backendBaseUrl } from "@/lib/backend";
import type { ApiErrorBody, GritBinsSuccess } from "@/lib/types";

/** Server-side proxy to FastAPI (browser never calls upstream APIs). */
export async function GET() {
  const url = new URL("/api/v1/grit-bins", backendBaseUrl());

  try {
    const upstream = await fetch(url, {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store",
    });

    const payload = (await upstream.json()) as GritBinsSuccess | ApiErrorBody;
    return NextResponse.json(payload, { status: upstream.status });
  } catch {
    const body: ApiErrorBody = {
      error: {
        code: "backend_unreachable",
        message: "Could not reach the FastAPI backend. Is it running on port 8000?",
      },
    };
    return NextResponse.json(body, { status: 502 });
  }
}
