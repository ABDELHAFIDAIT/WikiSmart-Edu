from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.api.deps import SessionDep
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.token import Token
from app.core.logging import logger


router = APIRouter()

@router.post("/signup", response_model=UserSchema)
async def create_user(new_user: UserCreate, db:SessionDep) :
    user = db.query(User).filter(User.email == new_user.email).first()
    
    if user :
        raise HTTPException(
            status_code=400,
            detail="Cet email est déjà utilisé !"
    )
    
    user = User(
        email=new_user.email,
        username=new_user.username,
        hashed_password=security.get_password_hash(new_user.password),
        role="user",
        is_active=True 
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/login", response_model=Token)
async def login_access_token(credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep) :
    logger.info(f"Tentative de connexion pour : {credentials.username}")
    
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not security.verify_password(credentials.password, user.hashed_password) :
        logger.warning(f"Échec connexion (mauvais credentials) : {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants Incorrectes - Username ou Password invalide !",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.is_active :
        logger.info(f"Utilisateur avec ID {user.id} n'est pas active !")
        raise HTTPException(status_code=400, detail="Utilisateur inactif")
    
    logger.info(f"Connexion réussie pour l'utilisateur ID {user.id}")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(subject=user.id, expired_delta=access_token_expires)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }