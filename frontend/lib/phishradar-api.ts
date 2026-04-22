import type { AnalyzeRequest, AnalyzeResponse } from "@/types/analysis";

export async function analyzeContent(
  request: AnalyzeRequest,
): Promise<AnalyzeResponse> {
  const response = await fetch("/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error("Analysis request failed.");
  }

  return response.json() as Promise<AnalyzeResponse>;
}
