import { NextResponse } from "next/server";
import type { AnalyzeRequest, AnalyzeResponse } from "@/types/analysis";

const BACKEND_BASE_URL = process.env.PHISHRADAR_API_BASE_URL;

export async function POST(request: Request) {
  let body: AnalyzeRequest;

  try {
    body = (await request.json()) as AnalyzeRequest;
  } catch (error) {
    console.error("[api/analyze] Invalid JSON body.", { error });
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  if (typeof body.content !== "string") {
    console.error("[api/analyze] Missing or invalid content field.", {
      contentType: typeof body.content,
    });
    return NextResponse.json(
      { error: "The content field is required." },
      { status: 400 },
    );
  }

  if (!BACKEND_BASE_URL) {
    console.error("[api/analyze] Missing PHISHRADAR_API_BASE_URL.");
    return NextResponse.json(
      { error: "PHISHRADAR_API_BASE_URL is not configured." },
      { status: 500 },
    );
  }

  try {
    const backendUrl = new URL("/analyze", BACKEND_BASE_URL);
    const backendResponse = await fetch(backendUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content: body.content }),
    });

    if (!backendResponse.ok) {
      console.error("[api/analyze] Backend request failed.", {
        backendUrl: backendUrl.toString(),
        status: backendResponse.status,
        statusText: backendResponse.statusText,
      });
      return NextResponse.json(
        { error: "Backend analysis request failed." },
        { status: backendResponse.status },
      );
    }

    const analysis = (await backendResponse.json()) as AnalyzeResponse;
    return NextResponse.json(analysis);
  } catch (error) {
    console.error("[api/analyze] Could not reach backend API.", {
      error,
      backendBaseUrl: BACKEND_BASE_URL,
    });
    return NextResponse.json(
      { error: "Could not reach the PhishRadar API." },
      { status: 502 },
    );
  }
}
