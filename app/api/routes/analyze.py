from fastapi import APIRouter

from app.analyzers.risk_engine import analyze_content
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse

router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    analysis = analyze_content(request.content)

    return AnalyzeResponse(
        score=analysis.score,
        label=analysis.label,
        reasons=analysis.reasons,
        breakdown=analysis.breakdown,
    )
