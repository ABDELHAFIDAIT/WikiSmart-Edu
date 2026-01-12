from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User

# indique à FastAPI que pour se loguer, il faut envoyer une requête POST à /api/v1/auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# Créer une session de base de données pour une requête et la ferme ensuite
def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

# Type alias pour simplifier les signatures de fonctions
SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


# Vérifie le token JWT, le décode, et retourne l'utilisateur associé.
# Lève une erreur 401 si le token est invalide ou expiré.
async def get_current_user(token: TokenDep, db: SessionDep) :
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="La validation des informations d'identification a echoué !",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try :
        # décodage du token avec la clé secrète
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None :
            raise credentials_exception
    
    except JWTError :
        # Si le token est expiré ou malformé
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if user is None :
        raise credentials_exception
    
    return user