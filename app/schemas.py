from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional,Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class NoteCreate(BaseModel):
    type: Literal["general", "summary"] = "general"
    content: str
