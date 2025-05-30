# app/services/ai_service.py
import google.generativeai as genai
from app.core.config import GEMINI_API_KEY
from typing import List
from app.models.schedule import Schedule
import json
import re

# Gemini API 구성
genai.configure(api_key=GEMINI_API_KEY)

# 사용할 모델 이름 직접 지정
GEMINI_MODEL = "models/gemini-1.5-flash"

class AIService:
    @staticmethod
    async def list_available_models():
        """사용 가능한 모델 목록을 조회합니다."""
        try:
            models = genai.list_models()
            return [model.name for model in models]
        except Exception as e:
            print(f"모델 목록 조회 중 오류 발생: {e}")
            return []
    
    @staticmethod
    async def extract_json_from_text(text):
        """
        텍스트에서 JSON 데이터를 추출합니다.
        """
        try:
            # JSON 배열 패턴을 찾습니다 ([...])
            json_pattern = r'\[\s*{.*}\s*\]'
            match = re.search(json_pattern, text, re.DOTALL)
            
            if match:
                json_str = match.group(0)
                # JSON 문자열을 파싱하여 유효성 검사
                return json.loads(json_str)
            
            # JSON 객체 패턴을 찾습니다 ({...})
            json_pattern = r'\{.*\}'
            match = re.search(json_pattern, text, re.DOTALL)
            
            if match:
                json_str = match.group(0)
                # JSON 문자열을 파싱하여 유효성 검사
                return json.loads(json_str)
            
            # JSON 형식이 아닌 경우 원본 텍스트 반환
            return text
        except Exception as e:
            print(f"JSON 추출 중 오류: {e}")
            return text
    
    @staticmethod
    async def optimize_schedule(schedules: List[Schedule]):
        """
        AI를 사용하여 일정을 최적화합니다.
        """
        if not schedules:
            return "[]"
        
        # 일정 데이터 변환
        schedule_data = []
        for schedule in schedules:
            schedule_data.append({
                "id": schedule.id,
                "title": schedule.title,
                "description": schedule.description,
                "start_time": schedule.start_time.strftime("%Y-%m-%d %H:%M"),
                "end_time": schedule.end_time.strftime("%Y-%m-%d %H:%M"),
                "priority": schedule.priority,
                "is_completed": schedule.is_completed
            })
        
        try:
            # 사용 가능한 모델 목록 확인 (참고용)
            available_models = await AIService.list_available_models()
            print("사용 가능한 모델:", available_models)
            
            # 직접 지정한 모델 사용
            print(f"선택된 모델: {GEMINI_MODEL}")
            model = genai.GenerativeModel(GEMINI_MODEL)
            
            # Gemini 프롬프트 작성 - 명확한 JSON 형식 지시 강화
            prompt = f"""
            나는 일정 최적화 AI 도우미입니다. 아래 주어진 일정을 분석하고 최적화하는 작업을 수행하겠습니다:
        
            일정 목록:
            {schedule_data}
        
            다음 기준으로 일정을 최적화해 주세요:
            1. 우선순위(priority)가 높은 일정을 우선적으로 배치
            2. 시간 겹침 없이 가장 효율적인 일정 배치
            3. 유사한 일정들은 가능한 연속적으로 배치하여 컨텍스트 전환 최소화
            4. 일정 사이에 적절한 휴식 시간 포함
            
            응답은 반드시 다음과 같은 유효한 JSON 배열 형식으로만 제공해 주세요:
            [
                {{
                "id": 일정ID,
                "optimized_start_time": "YYYY-MM-DD HH:MM",
                "optimized_end_time": "YYYY-MM-DD HH:MM",
                "optimization_reason": "최적화 이유 설명"
                }},
                ...
            ]
            
            다른 설명이나 텍스트 없이 오직 JSON 배열만 반환해 주세요.
            일정의 원래 ID는 유지하고, 최적화된 시간과 이유만 제공해 주세요.
            """
            
            response = model.generate_content(prompt)
            
            # 응답 텍스트에서 JSON 데이터 추출 시도
            result = await AIService.extract_json_from_text(response.text)
            
            # JSON으로 추출했다면 다시 문자열로 변환, 아니면 원본 텍스트 반환
            if isinstance(result, (list, dict)):
                return json.dumps(result, ensure_ascii=False)
            else:
                return result
                
        except Exception as e:
            print(f"예외 발생: {e}")
            return "[]"
    
    @staticmethod
    async def generate_long_term_plan(goal_title, goal_description, schedules: List[Schedule]):
        """
        사용자의 목표와 현재 일정을 바탕으로 장기 계획을 생성합니다.
        """
        # 일정 데이터 변환
        schedule_data = []
        for schedule in schedules:
            schedule_data.append({
                "title": schedule.title,
                "description": schedule.description,
                "start_time": schedule.start_time.strftime("%Y-%m-%d %H:%M"),
                "end_time": schedule.end_time.strftime("%Y-%m-%d %H:%M"),
                "priority": schedule.priority
            })
        
        try:
            # 직접 지정한 모델 사용
            model = genai.GenerativeModel(GEMINI_MODEL)
            
            # Gemini 프롬프트 작성
            prompt = f"""
            나는 장기 목표 계획 AI 도우미입니다. 사용자의 목표와 현재 일정을 분석하여 
            실현 가능한 장기 계획을 수립하는 작업을 수행하겠습니다.
            
            사용자 목표:
            제목: {goal_title}
            설명: {goal_description}
            
            현재 사용자 일정:
            {schedule_data}
            
            다음 항목을 포함한 장기 계획을 제공해 주세요:
            1. 목표 달성을 위한 주요 단계 (5-7개 단계)
            2. 각 단계별 예상 소요 시간
            3. 현재 일정과의 통합 방안
            4. 목표 달성을 위한 주간 권장 활동
            5. 진행 상황을 측정할 수 있는 주요 성과 지표
            
            사용자가 실제로 실행할 수 있는 구체적이고 실용적인 계획을 작성해 주세요.
            """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"장기 계획 생성 중 오류 발생: {e}")
            # 더 자세한 오류 메시지 반환
            error_message = f"장기 계획을 생성하는 동안 오류가 발생했습니다: {str(e)}"
            return error_message
            
    @staticmethod
    async def generate_schedule_based_plan(schedules: List[Schedule]):
        """
        사용자의 현재 일정만을 바탕으로 장기 계획을 생성합니다.
        """
        # 일정 데이터 변환
        schedule_data = []
        for schedule in schedules:
            schedule_data.append({
                "title": schedule.title,
                "description": schedule.description,
                "start_time": schedule.start_time.strftime("%Y-%m-%d %H:%M"),
                "end_time": schedule.end_time.strftime("%Y-%m-%d %H:%M"),
                "priority": schedule.priority
            })
        
        try:
            # 직접 지정한 모델 사용
            model = genai.GenerativeModel(GEMINI_MODEL)
            
            # Gemini 프롬프트 작성 - 목표 정보 없이 일정만 사용
            prompt = f"""
            나는 장기 계획 AI 도우미입니다. 사용자의 현재 일정을 분석하여 
            사용자의 생활 패턴과 우선순위를 파악하고 이를 바탕으로
            실현 가능한 장기 계획을 수립하는 작업을 수행하겠습니다.
            
            현재 사용자 일정:
            {schedule_data}
            
            다음 항목을 포함한 장기 계획을 제공해 주세요:
            1. 사용자의 현재 일정 패턴 분석
            2. 사용자의 우선순위와 관심사 식별
            3. 발전 가능한 장기 목표 3-5개 제안
            4. 각 목표별 실행 단계 (5-7개 단계)
            5. 각 단계별 예상 소요 시간
            6. 현재 일정과의 통합 방안
            7. 주간 권장 활동
            8. 진행 상황을 측정할 수 있는 주요 성과 지표
            
            사용자가 실제로 실행할 수 있는 구체적이고 실용적인 계획을 작성해 주세요.
            """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"장기 계획 생성 중 오류 발생: {e}")
            error_message = f"장기 계획을 생성하는 동안 오류가 발생했습니다: {str(e)}"
            return error_message