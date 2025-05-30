from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.models.goal import Goal
from app.models.schedule import Schedule
from app.schemas.goal import GoalCreate, Goal as GoalSchema, GoalUpdate
from app.core.auth import get_current_user
from app.services.ai_service import AIService
from app.schemas.schedule import Schedule as ScheduleSchema

router = APIRouter()

@router.post("/", response_model=GoalSchema)
async def create_goal(
    goal: GoalCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 새 목표 생성
    db_goal = Goal(
        title=goal.title,
        description=goal.description,
        target_date=goal.target_date,
        user_id=current_user.id
    )
    
    # 데이터베이스에 저장
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    
    return db_goal

@router.get("/", response_model=List[GoalSchema])
async def get_user_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 사용자의 모든 목표 조회 및 딕셔너리로 직접 변환
    goals = db.query(Goal).filter(Goal.user_id == current_user.id).all()
    
    # 명시적으로 모델 데이터를 딕셔너리로 변환 후 반환
    return [
        {
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "target_date": goal.target_date,
            "ai_generated_plan": goal.ai_generated_plan,
            "user_id": goal.user_id,
            "created_at": goal.created_at,
            "updated_at": goal.updated_at
        }
        for goal in goals
    ]

@router.get("/{goal_id}", response_model=GoalSchema)
async def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 특정 목표 조회
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="목표를 찾을 수 없습니다")
    
    return goal

@router.put("/{goal_id}", response_model=GoalSchema)
async def update_goal(
    goal_id: int,
    goal_update: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 업데이트할 목표 조회
    db_goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    
    if not db_goal:
        raise HTTPException(status_code=404, detail="목표를 찾을 수 없습니다")
    
    # 업데이트할 필드 설정
    update_data = goal_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_goal, key, value)
    
    # 데이터베이스에 저장
    db.commit()
    db.refresh(db_goal)
    
    return db_goal

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 삭제할 목표 조회
    db_goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    
    if not db_goal:
        raise HTTPException(status_code=404, detail="목표를 찾을 수 없습니다")
    
    # 목표 삭제
    db.delete(db_goal)
    db.commit()
    
    return None

@router.post("/{goal_id}/generate-plan", response_model=GoalSchema)
async def generate_long_term_plan(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 목표 조회
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="목표를 찾을 수 없습니다")
    
    # 사용자의 일정 조회
    schedules = db.query(Schedule).filter(
        Schedule.user_id == current_user.id
    ).all()
    
    # AI 서비스를 통한 장기 계획 생성
    plan = await AIService.generate_long_term_plan(
        goal.title, 
        goal.description, 
        schedules
    )
    
    # 생성된 계획 저장
    goal.ai_generated_plan = plan
    db.commit()
    db.refresh(goal)
    
    # 명시적으로 딕셔너리로 변환해서 반환
    return {
        "id": goal.id,
        "title": goal.title,
        "description": goal.description,
        "target_date": goal.target_date,
        "ai_generated_plan": goal.ai_generated_plan,
        "user_id": goal.user_id,
        "created_at": goal.created_at,
        "updated_at": goal.updated_at
    }

@router.get("/{goal_id}/schedules", response_model=List[ScheduleSchema])
async def get_related_schedules(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """목표와 관련된 일정을 조회합니다."""
    # 목표가 존재하는지 확인
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="목표를 찾을 수 없습니다")
    
    # 여기에서는 간단하게 사용자의 모든 일정을 반환합니다.
    # 실제로는 목표와 관련된 일정만 필터링하는 로직이 필요할 수 있습니다.
    schedules = db.query(Schedule).filter(
        Schedule.user_id == current_user.id
    ).all()
    
    return schedules