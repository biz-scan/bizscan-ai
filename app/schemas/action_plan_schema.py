from typing import List
from pydantic import BaseModel, Field

# 개별 전략의 구조 정의
class ActionPlanResult(BaseModel):
    category: str = Field(description="전략 카테고리 (마케팅/메뉴/운영)")
    title: str = Field(description="전략의 제목")
    tags: List[str] = Field(description="관련 키워드 태그 리스트")
    reason: str = Field(description="이 전략을 제안하는 이유 (데이터 근거)")
    action_details: List[str] = Field(description="3개 이내의 구체적인 실행 단계")

# 전체 응답 구조 정의 (전략 여러개)
class ActionPlanResponse(BaseModel):
    action_plans: List[ActionPlanResult] = Field(description="3가지 맞춤형 실행 전략 리스트")


