from pydantic import BaseModel

class SummaryRequest(BaseModel) :
    text: str
    
class SummaryResponse(BaseModel) :
    summary: str
    source: str = "AI-Llama3"