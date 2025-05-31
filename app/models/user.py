from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # 추가된 created_at 필드
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    schedules = relationship("Schedule", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")

    #community 추가
    posts = relationship("CommunityPost", back_populates="author", cascade="all, delete")
    schedules = relationship("UserSchedule", back_populates="user", cascade="all, delete")