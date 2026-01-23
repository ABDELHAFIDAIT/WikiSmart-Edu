from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdatePassword
from app.core.security import verify_password, get_password_hash


router = APIRouter()


@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Depends(get_current_user)) :
    return current_user



@router.put("/me/password")
def update_password(password_data: UserUpdatePassword,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)) :
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="L'ancien mot de passe est incorrect.")
    
    if len(password_data.new_password) < 8:
         raise HTTPException(status_code=400, detail="Le nouveau mot de passe doit contenir au moins 8 caractères.")
     
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Mot de passe mis à jour avec succès"}