from fastapi import APIRouter, HTTPException, Depends
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.article import Article
from app.models.enums import Action
from app.services.llm.groq_client import groq_service
from app.schemas.ai import SummaryRequest, SummaryResponse
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/summary", response_model=SummaryResponse, )
def generate_summary(request: SummaryRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) :
    
    article = db.query(Article).filter(
        Article.id == request.article_id,
        Article.user_id == current_user.id 
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable ou non autorisé.")
    
    try :
        if article.summary:
            print("Résumé déjà existant récupéré depuis la DB !")
            return SummaryResponse(summary=article.summary, article_id=article.id)
        
        summary_text = groq_service.generate_summary(article.content)
        
        article.summary = summary_text
        article.action_type = Action.SUMMARY
        
        db.commit()
        db.refresh(article)
        
        return SummaryResponse(
            summary=article.summary,
            source="Groq-Llama3",
            article_id=article.id
        )
    
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))