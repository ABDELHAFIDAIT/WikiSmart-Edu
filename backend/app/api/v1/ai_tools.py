from fastapi import APIRouter, HTTPException, Depends
from app.api.deps import get_current_user
from app.models.user import User
from app.services.llm.groq_client import groq_service
from app.schemas.ai import SummaryRequest, SummaryResponse


router = APIRouter()


@router.post("/summary", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest, current_user: User = Depends(get_current_user)) :
    try :
        summary_text = groq_service.generate_summary(request.text)
        
        return SummaryResponse(
            summary=summary_text,
            source="Groq-Llama3"
        )
    
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))