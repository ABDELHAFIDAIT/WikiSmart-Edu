from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime, Float
from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Quiz(Base) :
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    details = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    article_id = Column(Integer, ForeignKey("articles.id"))

    article = relationship("Article", back_populates="quizzes")
    attempts = relationship("Attempt", back_populates="quiz", cascade="all, delete-orphan")
    


class Attempt(Base) :
    __tablename__ = "attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, nullable=False)
    answers = Column(JSON, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    
    quiz = relationship("Quiz", back_populates="attempts")