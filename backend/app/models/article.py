from app.core.database import Base
from sqlalchemy import Integer, String, Column, ForeignKey, Text, Enum, DateTime
from app.models.enums import Action
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Article(Base) :
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, nullable=True)
    
    content = Column(Text, nullable=False)
    action_type = Column(Enum(Action), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", back_populates="articles")
    
    quiz_attempts = relationship("QuizAttempt", back_populates="article")