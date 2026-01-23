from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Any, Dict
from app.models.enums import Action as ActionEnum

class ArticleHistoryItem(BaseModel):
    id: int
    title: str
    url: Optional[str] = None
    created_at: datetime
    source_type: str  # "Wikipedia" ou "PDF"

    class Config:
        from_attributes = True


class ActionHistoryItem(BaseModel):
    id: int
    action_type: ActionEnum
    result_preview: str # On affiche juste le début du résultat
    created_at: datetime

    class Config:
        from_attributes = True
        

class QuizHistoryItem(BaseModel):
    id: int
    nb_questions: int
    created_at: datetime

    class Config:
        from_attributes = True
        

class AttemptHistoryItem(BaseModel):
    id: int
    score: float
    submitted_at: datetime
    # On pourrait ajouter 'answers' ici si on veut le détail complet

    class Config:
        from_attributes = True


class ArticleDetail(ArticleHistoryItem):
    content: str 


class ActionDetail(ActionHistoryItem):
    result: str 


class QuizDetail(QuizHistoryItem):
    details: List[Dict[str, Any]]


class AttemptDetail(AttemptHistoryItem):
    answers: List[int]
    quiz: QuizDetail