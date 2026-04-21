from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    content: str


class AnalyzeResponse(BaseModel):
    score: int
    label: str
    reasons: list[str]
