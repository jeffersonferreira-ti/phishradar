from fastapi import APIRouter

from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse

router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    return AnalyzeResponse(
        score=0,
        label="safe",
        reasons=["Mock response. Analysis rules are not implemented yet."],
    )
