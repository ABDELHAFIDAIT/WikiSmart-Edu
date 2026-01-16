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
from app.models.quiz import Quiz, Attempt
from app.schemas.quiz import QuizGenerated, QuizSubmission, QuizResult
from app.core.logging import logger

router = APIRouter()


@router.post("/summary", response_model=ActionResponse, )
def generate_summary(request: AIRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) :
    
    logger.info(f"Demande de résumé pour l'article ID {request.article_id}")
    
    article = db.query(Article).filter(
        Article.id == request.article_id,
        Article.user_id == current_user.id 
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article introuvable ou non autorisé.")
    
    try :
        summary_text = groq_service.generate_summary(article.content)
        
        logger.info(f"Résumé généré avec succès ({len(summary_text)} chars)")
        
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
        logger.error(f"Erreur lors du résumé : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/translate", response_model=ActionResponse)
def translate_article_content(request: TranslationRequest,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    
    logger.info(f"Demande de traduction (Article {request.article_id}) vers {request.target_lang}")
    
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
        
        logger.info("Traduction terminée")
        
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
        logger.error(f"Erreur traduction : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/quiz/generate", response_model=QuizGenerated)
def generate_quiz(request: AIRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) :
    
    logger.info(f"Génération de Quiz pour l'article ID {request.article_id}")
    
    article = db.query(Article).filter(Article.id == request.article_id).first()
    
    if not article :
        raise HTTPException(status_code=404, detail="Article Introuvable !")
    
    questions_data = gemini_service.generate_quiz(article.content)
    
    if not questions_data :
        logger.error("L'IA a renvoyé une liste de questions vide")
        raise HTTPException(status_code=500, detail="Echec de la génération du quiz !")
    
    logger.info(f"Quiz généré avec {len(questions_data)} questions")
    
    new_quiz = Quiz(
        article_id=article.id,
        details=questions_data
    )
    
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return QuizGenerated(
        quiz_id=new_quiz.id,
        article_id=article.id,
        questions=questions_data
    )




@router.post("/quiz/submit", response_model=QuizResult)
def submit_quiz(submission: QuizSubmission, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) :
    quiz = db.query(Quiz).filter(Quiz.id == submission.quiz_id).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz introuvable")
    
    questions = quiz.details
    
    if len(submission.user_answers) != len(questions):
        raise HTTPException(status_code=400, detail="Nombre de réponses incorrect")
    
    correct_count = 0
    total = len(questions)
    
    for i, question in enumerate(questions) :
        correct_idx = question.get("correct_index")
        user_choice = submission.user_answers[i]
        
        if user_choice == correct_idx:
            correct_count += 1
        
    score_percentage = (correct_count / total) * 100 if total > 0 else 0
    
    new_attempt = Attempt(
        quiz_id=quiz.id,
        score=score_percentage,
        answers=submission.user_answers
    )
    
    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)
    
    msg = "Bravo, Excellent Travail !" if score_percentage >= 70 else "Continuez vos efforts !"
    
    return QuizResult(
        attempt_id=new_attempt.id,
        score=score_percentage,
        message=msg
    )