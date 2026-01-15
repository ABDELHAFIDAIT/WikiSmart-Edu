from pydantic import BaseModel

class SummaryRequest(BaseModel):
    article_id: int

class SummaryResponse(BaseModel):
    summary: str
    source: str = "AI-Llama3"
    article_id: int