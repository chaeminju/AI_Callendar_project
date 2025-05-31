from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import community as community_schema
from app.services import community_service

router = APIRouter(prefix="/community", tags=["Community"])

# 커뮤니티 메인 페이지 렌더링 (필요한 경우)
@router.get("/", response_model=community_schema.CommunityPageResponse)
def get_community_page(db: Session = Depends(get_db)):
    return community_service.get_community_page(db)

# 특정 날짜별 사용자 일정 및 글 목록 조회
@router.get("/date/{date}", response_model=community_schema.CommunityDateResponse)
def get_schedule_and_posts_by_date(date: str, db: Session = Depends(get_db)):
    return community_service.get_schedule_and_posts_by_date(db, date)

# 글 작성
@router.post("/post", response_model=community_schema.PostResponse)
def create_post(post: community_schema.PostCreate, db: Session = Depends(get_db)):
    return community_service.create_post(db, post)

# 글 상세 조회
@router.get("/post/{post_id}", response_model=community_schema.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return community_service.get_post(db, post_id)

# 글 수정
@router.put("/post/{post_id}", response_model=community_schema.PostResponse)
def update_post(post_id: int, post: community_schema.PostUpdate, db: Session = Depends(get_db)):
    return community_service.update_post(db, post_id, post)

# 글 삭제
@router.delete("/post/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return community_service.delete_post(db, post_id)
