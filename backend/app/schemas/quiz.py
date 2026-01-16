from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel) :
    id: int
    question: str
    options: List[str]
    correct_index: int
    
class QuizGenerated(BaseModel) :
    quiz_id: int
    article_id: int
    questions: List[Question]


class QuizSubmission(BaseModel) :
    quiz_id: int
    user_answers: List[int]
    

class QuizResult(BaseModel) :
    score: float
    message: str
    attempt_id: int