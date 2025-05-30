from app.models.user import User
from app.models.schedule import Schedule
from app.models.goal import Goal

# User 모델에 역참조 관계 추가
User.schedules = relationship("Schedule", back_populates="user")
User.goals = relationship("Goal", back_populates="user")