from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class QuizAttempt(Base) :
    __tablename__ = "quizattempts"
    
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
    details = Column(JSON, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user_id = Column(Integer, ForeignKey("users.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))

    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    article = relationship("Article", back_populates="quiz_attempts")