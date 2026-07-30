from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional,Literal,List


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


class NoteOut(BaseModel):
    id: int
    shift_id: int
    author_id: int
    type: str
    content: str
    acknowledged: bool
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ShiftOut(BaseModel):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str
    opened_by: int
    closed_by: Optional[int] = None
    notes: List[NoteOut] = []

    class Config:
        from_attributes = True