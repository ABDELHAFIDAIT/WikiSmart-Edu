from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.article import Article
from app.models.action import Action
from app.models.enums import Action as ActionEnum
from app.services.llm.groq_client import groq_service
from app.services.llm.gemini_client import gemini_service
from app.schemas.ai import AIRequest, TranslationRequest, ActionResponse

router = APIRouter()


@router.post("/summary", response_model=ActionResponse, )
def generate_summary(request: AIRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) :
    
    article = db.query(Article).filter(
        Article.id == request.article_id,
        Article.user_id == current_user.id 
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable ou non autorisé.")
    
    try :
        summary_text = groq_service.generate_summary(article.content)
        
        new_action = Action(
            article_id=article.id,
            action_type=ActionEnum.SUMMARY,
            result=summary_text
        )
        
        db.add(new_action)
        db.commit()
        db.refresh(new_action)
        
        return ActionResponse(
            id=new_action.id,
            article_id=article.id,
            action_type="summary",
            result=new_action.result,
            created_at=str(new_action.created_at)
        )
    
    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/translate", response_model=ActionResponse)
def translate_article_content(
    request: TranslationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    article = db.query(Article).filter(
        Article.id == request.article_id,
        Article.user_id == current_user.id
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable !")

    try:

        translated_text = gemini_service.translate_article(
            text=article.content, 
            target_lang=request.target_lang
        )
        
        new_action = Action(
            article_id=article.id,
            action_type=ActionEnum.TRANSLATION,
            result=f"[{request.target_lang}] - {translated_text}"
        )
        
        db.add(new_action)
        db.commit()
        db.refresh(new_action)
        
        return ActionResponse(
            id=new_action.id,
            article_id=article.id,
            action_type="translation",
            result=new_action.result,
            created_at=str(new_action.created_at)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))