import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Gemini API 키 가져오기
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 기타 설정
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./schedule_ai.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")