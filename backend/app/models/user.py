from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.models.enums import Role
from sqlalchemy.orm import relationship

class User(Base) :
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    
    role = Column(Enum(Role), default=Role.USER)
    
    is_active = Column(Boolean, default=True)
    
    articles = relationship("Article", back_populates="user")