from datetime import datetime, timedelta, timezone
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configuration du contexte de hachage (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Fonction génèrant un token JWT crypté contenant l'identité de l'utilisateur et une date d'expiration
def create_access_token(subject: Union[str, Any], expired_delta: timedelta = None) :
    if expired_delta :
        expire = datetime.now(timezone.utc) + expired_delta
    else :
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp":expire, "sub": str(subject)}
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


# Vérifie si un mot de passe en clair correspond au hash stocké en base
def verify_password(password:str, hashed_password:str) :
    return pwd_context.verify(password, hashed_password)


# Transforme un mot de passe en clair en hash sécurisé pour le stockage
def get_password_hash(password:str) :
    return pwd_context.hash(password)