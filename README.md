# Schedule AI Backend

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.23-red.svg)](https://www.sqlalchemy.org/)
[![Google AI](https://img.shields.io/badge/Google_Gemini_AI-0.3.1-yellow.svg)](https://ai.google.dev/)

## 📋 프로젝트 개요

**Schedule AI Backend**는 Google Gemini AI를 활용하여 사용자의 일정을 지능적으로 최적화하고 장기 계획을 생성하는 웹 애플리케이션입니다. FastAPI와 SQLite를 기반으로 구축되었으며, JWT 인증 시스템과 RESTful API를 제공합니다.

### 🌟 주요 특징

- **AI 기반 일정 최적화**: Google Gemini AI를 활용한 스마트 일정 재배치
- **장기 목표 계획 생성**: 사용자의 목표와 현재 일정을 분석한 맞춤형 장기 계획
- **사용자 인증 시스템**: JWT 토큰 기반의 보안 인증
- **직관적인 웹 인터페이스**: Jinja2 템플릿을 활용한 사용자 친화적 UI
- **RESTful API**: 완전한 CRUD 연산 지원
- **실시간 일정 관리**: 일정 추가, 수정, 삭제 및 완료 상태 관리

## 🏗️ 프로젝트 구조

```
SCHEDULE-AI-BACKEND/
├── app/
│   ├── core/               # 핵심 설정 및 인증
│   │   ├── auth.py        # JWT 인증 로직
│   │   └── config.py      # 환경 설정
│   ├── db/                # 데이터베이스 설정
│   │   ├── database.py    # SQLAlchemy 설정
│   │   └── __init__.py
│   ├── models/            # SQLAlchemy ORM 모델
│   │   ├── goal.py        # 목표 모델
│   │   ├── schedule.py    # 일정 모델
│   │   ├── user.py        # 사용자 모델
│   │   └── __init__.py
│   ├── routers/           # FastAPI 라우터
│   │   ├── goals.py       # 목표 관련 API
│   │   ├── schedules.py   # 일정 관련 API
│   │   ├── users.py       # 사용자 관련 API
│   │   └── __init__.py
│   ├── schemas/           # Pydantic 스키마
│   │   ├── goal.py        # 목표 스키마
│   │   ├── schedule.py    # 일정 스키마
│   │   ├── user.py        # 사용자 스키마
│   │   └── __init__.py
│   ├── services/          # 비즈니스 로직
│   │   ├── ai_service.py  # AI 서비스 (Gemini 통합)
│   │   └── __init__.py
│   └── main.py           # FastAPI 애플리케이션 진입점
├── static/               # 정적 파일 (CSS, JS, 이미지)
├── templates/            # Jinja2 HTML 템플릿
│   ├── dashboard.html    # 대시보드 페이지
│   ├── goals.html        # 목표 관리 페이지
│   ├── login.html        # 로그인 페이지
│   └── register.html     # 회원가입 페이지
├── requirements.txt      # Python 의존성
└── .env                 # 환경 변수 (개발용)
```

## 🚀 시작하기

### 전제 조건

- Python 3.8 이상
- Google Gemini API 키 ([Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급)

### 설치 과정

1. **저장소 클론**
   ```bash
   git clone https://github.com/your-username/schedule-ai-backend.git
   cd schedule-ai-backend
   ```

2. **가상 환경 생성 및 활성화**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **환경 변수 설정**
   
   `.env` 파일을 프로젝트 루트에 생성하고 다음 내용을 입력:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your_secret_key_for_jwt
   DATABASE_URL=sqlite:///./schedule_ai.db
   ```

5. **애플리케이션 실행**
   ```powershell
   python -m app.main 
   ```

6. **브라우저 접속**
   
   http://localhost:8000 으로 접속하여 애플리케이션을 확인합니다.


### 주요 엔드포인트

#### 🔐 사용자 인증

| 메서드 | 엔드포인트 | 설명 |
|---------|------------|------|
| `POST` | `/api/users/register` | 회원가입 |
| `POST` | `/api/users/token` | 로그인 (토큰 발급) |
| `GET` | `/api/users/me` | 현재 사용자 정보 조회 |

#### 📅 일정 관리

| 메서드 | 엔드포인트 | 설명 |
|---------|------------|------|
| `POST` | `/api/schedules` | 새 일정 생성 |
| `GET` | `/api/schedules` | 사용자 일정 목록 조회 |
| `GET` | `/api/schedules/{id}` | 특정 일정 조회 |
| `PUT` | `/api/schedules/{id}` | 일정 수정 |
| `DELETE` | `/api/schedules/{id}` | 일정 삭제 |
| `POST` | `/api/schedules/optimize` | **AI 일정 최적화** |
| `POST` | `/api/schedules/generate-plan` | **일정 기반 장기 계획 생성** |

#### 🎯 목표 관리

| 메서드 | 엔드포인트 | 설명 |
|---------|------------|------|
| `POST` | `/api/goals` | 새 목표 생성 |
| `GET` | `/api/goals` | 사용자 목표 목록 조회 |
| `GET` | `/api/goals/{id}` | 특정 목표 조회 |
| `PUT` | `/api/goals/{id}` | 목표 수정 |
| `DELETE` | `/api/goals/{id}` | 목표 삭제 |
| `POST` | `/api/goals/{id}/generate-plan` | **AI 장기 계획 생성** |
| `GET` | `/api/goals/{id}/schedules` | 목표 관련 일정 조회 |

## 🤖 AI 기능 상세

### 1. 일정 최적화 (`/api/schedules/optimize`)

**기능**: 사용자의 미완료된 일정을 분석하여 다음 기준으로 최적화합니다:
- 높은 우선순위 일정 우선 배치
- 시간 겹침 방지 및 효율적 배치
- 유사 일정의 연속 배치로 컨텍스트 전환 최소화
- 적절한 휴식 시간 포함

**요청**: 인증된 사용자만 접근 가능
**응답**: 최적화된 일정 목록과 변경 사유

### 2. 목표 기반 장기 계획 생성 (`/api/goals/{id}/generate-plan`)

**기능**: 특정 목표와 사용자의 현재 일정을 분석하여 장기 계획을 생성합니다:
- 목표 달성을 위한 주요 단계 (5-7개)
- 각 단계별 예상 소요 시간
- 현재 일정과의 통합 방안
- 주간 권장 활동
- 성과 측정 지표

**요청**: 목표 ID 필요
**응답**: 상세한 실행 가능한 장기 계획

### 3. 일정 기반 계획 생성 (`/api/schedules/generate-plan`)

**기능**: 사용자의 현재 일정 패턴만을 분석하여 장기 계획을 제안합니다:
- 현재 일정 패턴 분석
- 우선순위와 관심사 식별
- 발전 가능한 목표 3-5개 제안
- 각 목표별 실행 단계

## 🔒 보안

- **JWT 토큰 인증**: 모든 보호된 엔드포인트에서 Bearer 토큰 필요
- **비밀번호 해싱**: bcrypt를 사용한 안전한 비밀번호 저장
- **CORS 설정**: 개발 환경에서 모든 오리진 허용 (프로덕션에서는 수정 필요)

## 🗄️ 데이터베이스 스키마

### User 테이블
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Schedule 테이블
```sql
CREATE TABLE schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    priority INTEGER DEFAULT 1,
    is_completed BOOLEAN DEFAULT 0,
    is_optimized BOOLEAN DEFAULT 0,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Goal 테이블
```sql
CREATE TABLE goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    target_date TIMESTAMP,
    ai_generated_plan TEXT,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```





## 📋 사용 예시

### 1. 사용자 등록 및 로그인

**회원가입:**
```bash
curl -X POST "http://localhost:8000/api/users/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "secure_password"
     }'
```

**로그인:**
```bash
curl -X POST "http://localhost:8000/api/users/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john@example.com&password=secure_password"
```

### 2. 일정 생성

```bash
curl -X POST "http://localhost:8000/api/schedules" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "팀 미팅",
       "description": "주간 프로젝트 리뷰",
       "start_time": "2024-01-15T09:00:00",
       "end_time": "2024-01-15T10:00:00",
       "priority": 4
     }'
```

### 3. AI 일정 최적화

```bash
curl -X POST "http://localhost:8000/api/schedules/optimize" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🛠️ 기술 스택

- **백엔드 프레임워크**: FastAPI 0.104.1
- **데이터베이스**: SQLite with SQLAlchemy 2.0.23
- **AI 통합**: Google Gemini AI 0.3.1
- **인증**: JWT (python-jose)
- **비밀번호 해싱**: bcrypt (passlib)
- **데이터 검증**: Pydantic
- **템플릿 엔진**: Jinja2
- **ASGI 서버**: Uvicorn

## 📄 환경 변수

| 변수명 | 필수 | 기본값 | 설명 |
|--------|------|--------|------|
| `GEMINI_API_KEY` | ✅ | - | Google Gemini AI API 키 |
| `SECRET_KEY` | ✅ | - | JWT 토큰 암호화 키 |
| `DATABASE_URL` | ❌ | `sqlite:///./schedule_ai.db` | 데이터베이스 연결 URL |


