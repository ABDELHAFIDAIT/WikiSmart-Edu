from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.models.enums import Role
from app.core.security import get_password_hash

def init_db(db: Session):
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER_EMAIL).first()
    
    if not user:
        print(f"Création de l'utilisateur Admin : {settings.FIRST_SUPERUSER_EMAIL}")
        
        admin = User(
            email=settings.FIRST_SUPERUSER_EMAIL,
            username=settings.FIRST_SUPERUSER_USERNAME,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            role=Role.ADMIN,
            is_active=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("Admin créé avec succès !")
    else:
        print("L'utilisateur Admin existe déjà.")