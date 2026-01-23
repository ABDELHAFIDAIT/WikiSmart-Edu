from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdatePassword
from app.core.security import verify_password, get_password_hash
from typing import Optional, List
from app.models.action import Action
from app.models.quiz import Quiz, Attempt
from app.models.article import Article
from app.schemas.history import ArticleHistoryItem, ActionHistoryItem, QuizHistoryItem, AttemptHistoryItem


router = APIRouter()


@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Depends(get_current_user)) :
    return current_user



@router.put("/me/password")
def update_password(password_data: UserUpdatePassword,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)) :
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="L'ancien mot de passe est incorrect.")
    
    if len(password_data.new_password) < 8:
         raise HTTPException(status_code=400, detail="Le nouveau mot de passe doit contenir au moins 8 caractères.")
     
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Mot de passe mis à jour avec succès"}



@router.get("/me/history/articles", response_model=List[ArticleHistoryItem])
def get_articles_history(source: str = "all", current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    query = db.query(Article).filter(Article.user_id == current_user.id)
    articles = query.order_by(Article.created_at.desc()).all()
    
    results = []
    for art in articles:
        is_wiki = art.url and art.url.startswith("http")
        art_source = "Wikipedia" if is_wiki else "PDF"
        
        if source == "wiki" and not is_wiki:
            continue
        if source == "pdf" and is_wiki:
            continue
            
        results.append(ArticleHistoryItem(
            id=art.id,
            title=art.title,
            url=art.url,
            created_at=art.created_at,
            source_type=art_source
        ))
        
    return results



@router.get("/me/history/articles/{article_id}/actions", response_model=List[ActionHistoryItem])
def get_article_actions(article_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)) :
    article = db.query(Article).filter(Article.id == article_id, Article.user_id == current_user.id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable")
        
    actions = db.query(Action).filter(Action.article_id == article_id).order_by(Action.created_at.desc()).all()
    
    return [
        ActionHistoryItem(
            id=a.id,
            action_type=a.action_type,
            result_preview=a.result[:100] + "..." if a.result else "",
            created_at=a.created_at
        ) for a in actions
    ]
    



@router.get("/me/history/articles/{article_id}/quizzes", response_model=List[QuizHistoryItem])
def get_article_quizzes(article_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id, Article.user_id == current_user.id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable")

    quizzes = db.query(Quiz).filter(Quiz.article_id == article_id).order_by(Quiz.created_at.desc()).all()
    
    return [
        QuizHistoryItem(
            id=q.id,
            nb_questions=len(q.details) if isinstance(q.details, list) else 0,
            created_at=q.created_at
        ) for q in quizzes
    ]
    
    
    
    
@router.get("/me/history/quizzes/{quiz_id}/attempts", response_model=List[AttemptHistoryItem])
def get_quiz_attempts(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).join(Article).filter(Quiz.id == quiz_id, Article.user_id == current_user.id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz introuvable ou accès refusé")

    attempts = db.query(Attempt).filter(Attempt.quiz_id == quiz_id).order_by(Attempt.submitted_at.desc()).all()
    return attempts