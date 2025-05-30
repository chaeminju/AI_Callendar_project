from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GoalBase(BaseModel):
    title: str
    description: str
    target_date: Optional[datetime] = None

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[datetime] = None
    ai_generated_plan: Optional[str] = None

class Goal(GoalBase):
    id: int
    ai_generated_plan: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True