from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommunityPostCreate(BaseModel):
    title: str
    content: str
    author_id: int

class CommunityPostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author_id: int

    class Config:
        orm_mode = True

class UserScheduleOut(BaseModel):
    id: int
    date: datetime
    content: str

    class Config:
        orm_mode = True
