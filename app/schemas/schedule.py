from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ScheduleBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    priority: int = 1  # 1-5, 5가 가장 높은 우선순위

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    priority: Optional[int] = None
    is_completed: Optional[bool] = None

class Schedule(ScheduleBase):
    id: int
    is_completed: bool
    is_optimized: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
def convert_to_schema(db_schedule):
    """SQLAlchemy Schedule 모델을 Pydantic Schedule 스키마로 변환"""
    return Schedule(
        id=db_schedule.id,
        title=db_schedule.title,
        description=db_schedule.description,
        start_time=db_schedule.start_time,
        end_time=db_schedule.end_time,
        priority=db_schedule.priority,
        is_completed=db_schedule.is_completed,
        is_optimized=db_schedule.is_optimized,
        user_id=db_schedule.user_id,
        created_at=db_schedule.created_at,
        updated_at=db_schedule.updated_at
    )
    
class GeneratedPlan(BaseModel):
    plan: str