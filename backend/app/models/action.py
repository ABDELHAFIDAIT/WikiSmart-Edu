from app.core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime
from app.models.enums import Action
from sqlalchemy.sql import func

class Action(Base) :
    __tablename__ = "actions"
    
    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(Enum(Action), nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    article_id = Column(Integer, ForeignKey("articles.id"))
    
    article = relationship("Article", back_populates="actions")