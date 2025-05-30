from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime, timedelta 

from app.db.database import get_db
from app.models.user import User
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, Schedule as ScheduleSchema, ScheduleUpdate
from app.core.auth import get_current_user
from app.services.ai_service import AIService
from app.schemas.schedule import ScheduleCreate, Schedule as ScheduleSchema, ScheduleUpdate, convert_to_schema
from app.schemas import schedule as schemas
from pydantic import BaseModel

router = APIRouter()

@router.post("/", response_model=ScheduleSchema)
async def create_schedule(
    schedule: ScheduleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 새 일정 생성
    db_schedule = Schedule(
        title=schedule.title,
        description=schedule.description,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        priority=schedule.priority,
        user_id=current_user.id
    )
    
    # 데이터베이스에 저장
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    
    return convert_to_schema(db_schedule)

@router.get("/", response_model=List[ScheduleSchema])
async def get_user_schedules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    schedules = db.query(Schedule).filter(Schedule.user_id == current_user.id).all()
    
    # 수정된 반환부
    return [convert_to_schema(schedule) for schedule in schedules]

@router.get("/{schedule_id}", response_model=ScheduleSchema)
async def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 특정 일정 조회
    schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id,
        Schedule.user_id == current_user.id
    ).first()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다")
    
    return schedule

@router.put("/{schedule_id}", response_model=ScheduleSchema)
async def update_schedule(
    schedule_id: int,
    schedule_update: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 업데이트할 일정 조회
    db_schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id,
        Schedule.user_id == current_user.id
    ).first()
    
    if not db_schedule:
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다")
    
    # 업데이트할 필드 설정
    update_data = schedule_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_schedule, key, value)
    
    # 데이터베이스에 저장
    db.commit()
    db.refresh(db_schedule)
    
    return convert_to_schema(db_schedule)

@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 삭제할 일정 조회
    db_schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id,
        Schedule.user_id == current_user.id
    ).first()
    
    if not db_schedule:
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다")
    
    # 일정 삭제
    db.delete(db_schedule)
    db.commit()
    
    return None

@router.post("/optimize", response_model=List[ScheduleSchema])
async def optimize_schedules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 사용자의 미완료된 일정 조회
    schedules = db.query(Schedule).filter(
        Schedule.user_id == current_user.id,
        Schedule.is_completed == False
    ).all()
    
    if not schedules:
        raise HTTPException(status_code=404, detail="최적화할 일정이 없습니다")
    
    try:
        # AI 서비스를 통한 일정 최적화
        optimization_result = await AIService.optimize_schedule(schedules)
        
        # 결과가 빈 문자열이거나 None이면 빈 배열로 처리
        if not optimization_result or optimization_result.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="AI 최적화 결과가 없습니다. 다시 시도해주세요."
            )
            
        # AI 반환 결과 파싱
        optimized_data = json.loads(optimization_result)
        
        if not optimized_data:  # 빈 배열이면
            raise HTTPException(
                status_code=400,
                detail="AI가 일정을 최적화할 수 없습니다. API 할당량을 초과했거나 다른 문제가 발생했습니다."
            )
            
        try:    
            # AI 반환 결과 파싱
            optimized_data = json.loads(optimization_result)
            
            # 각 일정 업데이트
            updated_schedules = []
            for opt_item in optimized_data:
                schedule_id = opt_item["id"]
                schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
                
                if schedule:
                    # 최적화된 시간 정보로 일정 업데이트
                    schedule.start_time = datetime.strptime(opt_item["optimized_start_time"], "%Y-%m-%d %H:%M")
                    schedule.end_time = datetime.strptime(opt_item["optimized_end_time"], "%Y-%m-%d %H:%M")
                    schedule.is_optimized = True
                    db.commit()
                    db.refresh(schedule)
                    # SQLAlchemy 모델을 딕셔너리로 변환
                    updated_schedules.append({
                        "id": schedule.id,
                        "title": schedule.title,
                        "description": schedule.description,
                        "start_time": schedule.start_time,
                        "end_time": schedule.end_time,
                        "priority": schedule.priority,
                        "is_completed": schedule.is_completed,
                        "is_optimized": schedule.is_optimized,
                        "user_id": schedule.user_id,
                        "created_at": schedule.created_at,
                        "updated_at": schedule.updated_at
                    })
            
            return updated_schedules
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}, 원본 텍스트: {optimization_result}")
            raise HTTPException(
                status_code=400,
                detail=f"AI 응답을 JSON으로 파싱할 수 없습니다. 다시 시도해주세요."
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"예외 발생: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"일정 최적화 중 오류가 발생했습니다: {str(e)}"
        )



class GeneratedPlan(BaseModel):
    plan: str
    
@router.post("/generate-plan", response_model=GeneratedPlan)
async def generate_plan_from_schedules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 현재 사용자의 일정 가져오기
    schedules = db.query(Schedule).filter(Schedule.user_id == current_user.id).all()
    
    # AI 서비스를 사용하여 일정 기반 장기 계획 생성
    plan = await AIService.generate_schedule_based_plan(schedules)
    
    # 응답 반환
    return {"plan": plan}