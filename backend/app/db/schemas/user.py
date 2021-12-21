from pydantic import BaseModel, EmailStr
from typing import Optional


class BaseUser(BaseModel):
    class Config:
        orm_mode = True


class User(BaseUser):
    id: int
    email: EmailStr
    username: str


class UserCreate(BaseUser):
    email: EmailStr
    password: str
    username: str


class UserUpdate(BaseUser):
    email: Optional[EmailStr]
    password: Optional[str]
    username: Optional[str]
