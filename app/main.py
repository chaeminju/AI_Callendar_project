from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

from app.db.database import engine, Base
from app.routers import schedules, goals, users

import jinja2
# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Schedule AI Backend")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 및 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.loader = jinja2.FileSystemLoader([
    "templates",
    "templates/includes"
])
# 라우터 등록
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["schedules"])
app.include_router(goals.router, prefix="/api/goals", tags=["goals"])

# 루트 경로('/') 핸들러 - 홈 페이지로 리다이렉트
@app.get("/")
async def root():
    return RedirectResponse(url="/home")

# HTML 페이지 라우터
@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard")
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/goals")
async def goals_page(request: Request):
    return templates.TemplateResponse("goals.html", {"request": request})

# 홈 페이지 라우터
@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)