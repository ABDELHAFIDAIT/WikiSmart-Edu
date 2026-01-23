from pydantic import BaseModel, EmailStr
from app.models.enums import Role

class UserBase(BaseModel) :
    email: EmailStr
    username: str
    is_active: bool = True
    role: str = Role.USER


class UserCreate(UserBase) :
    password: str


class UserUpdatePassword(BaseModel) :
    old_password: str
    new_password: str

class User(UserBase) :
    id : int
    model_config = {"from_attributes": True}