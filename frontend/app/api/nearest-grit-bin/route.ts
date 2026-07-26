import { NextRequest, NextResponse } from "next/server";

import type { ApiErrorBody, NearestGritBinSuccess } from "@/lib/types";

/**
 * Server-side proxy to FastAPI.
 *
 * The browser never calls Derbyshire upstreams (CORS constraint) and never
 * talks to FastAPI cross-origin either — this Route Handler keeps BACKEND_URL
 * on the server and forwards the typed JSON contract.
 */
export async function GET(request: NextRequest) {
  const postcode = request.nextUrl.searchParams.get("postcode")?.trim() ?? "";
  const address = request.nextUrl.searchParams.get("address")?.trim() ?? "";

  if (!postcode || !address) {
    const body: ApiErrorBody = {
      error: {
        code: "missing_parameter",
        message: "Both postcode and address are required.",
      },
    };
    return NextResponse.json(body, { status: 400 });
  }

  const backend = process.env.BACKEND_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";
  const url = new URL("/nearest-grit-bin", backend);
  url.searchParams.set("postcode", postcode);
  url.searchParams.set("address", address);

  try {
    const upstream = await fetch(url, {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store",
    });

    const payload = (await upstream.json()) as NearestGritBinSuccess | ApiErrorBody;
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
