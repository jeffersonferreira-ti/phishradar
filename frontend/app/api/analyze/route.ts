import { NextResponse } from "next/server";
import type { AnalyzeRequest, AnalyzeResponse } from "@/types/analysis";

const BACKEND_BASE_URL =
  process.env.PHISHRADAR_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function POST(request: Request) {
  let body: AnalyzeRequest;

  try {
    body = (await request.json()) as AnalyzeRequest;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  if (typeof body.content !== "string") {
    return NextResponse.json(
      { error: "The content field is required." },
      { status: 400 },
    );
  }

  try {
    const backendResponse = await fetch(`${BACKEND_BASE_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content: body.content }),
    });

    if (!backendResponse.ok) {
      return NextResponse.json(
        { error: "Backend analysis request failed." },
        { status: backendResponse.status },
      );
    }

    const analysis = (await backendResponse.json()) as AnalyzeResponse;
    return NextResponse.json(analysis);
  } catch {
    return NextResponse.json(
      { error: "Could not reach the PhishRadar API." },
      { status: 502 },
    );
  }
}
