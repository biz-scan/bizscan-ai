from typing import List
from pydantic import BaseModel, Field

# [추가] 1단계: 전략 후보 생성을 위한 스키마
class CandidateResult(BaseModel):
    id: int = Field(description="후보 전략의 임시 ID")
    title: str = Field(description="전략 후보의 제목")
    tags: List[str] = Field(
        default_factory=list, 
        description="전략의 특성을 나타내는 해시태그 리스트"
    )
    related_swot: List[str] = Field(
        default_factory=list, 
        description="전략 도출에 근거가 된 SWOT 요소 코드 리스트 (예: S1, O1)"
    )
    reason: str = Field(description="해당 전략이 제안된 상세 근거 및 논리")

class CandidateResponse(BaseModel):
    candidates: List[CandidateResult] = Field(description="생성된 전략 후보 목록")

# [추가] 2단계: 전략 평가를 위한 스키마
class EvaluationResult(BaseModel):
    id: int = Field(description="평가할 전략의 ID")
    impactScore: int = Field(
        ge=0, le=10, 
        description="전략의 예상 영향도 점수 (0-10)"
    )
    effortScore: int = Field(
        ge=0, le=10, 
        description="전략 실행에 필요한 노력/비용 점수 (0-10)"
    )
    evaluation: str = Field(
        description="점수 산정 근거 및 전략에 대한 종합 평가 의견"
    )

class EvaluationResponse(BaseModel):
    evaluations: List[EvaluationResult] = Field(description="각 후보 전략에 대한 평가 결과")

# 3단계
class SelectionResult(BaseModel):
    id: int = Field(description="전략의 고유 식별 번호")
    title: str = Field(description="최종 확정된 전략 명칭")
    tags: List[str] = Field(
        default_factory=list, 
        description="전략 성격 및 카테고리 태그 (예: #매출증대)"
    )
    related_swot: List[str] = Field(
        default_factory=list, 
        description="전략 수립의 근거가 된 SWOT 요소 리스트"
    )
    final_reason: str = Field(
        description="시장 분석 및 내부 역량을 종합한 최종 전략 수립 배경 및 기대 효과"
    )

class SelectionResponse(BaseModel):
    selections: List[SelectionResult] = Field(
        description="최종 선정된 전략들의 목록"
    )

# 4단계
class ActionStep(BaseModel):
    step: int = Field(description="실행 단계 번호 (1, 2, 3)")
    title: str = Field(description="해당 단계의 핵심 목표 또는 제목")
    description: str = Field(description="구체적인 실행 방법 및 내용")
    expected_outcome: str = Field(description="해당 단계를 완료했을 때의 기대 결과")

class StrategyActionPlan(BaseModel):
    id: int = Field(description="선정된 전략의 고유 ID")
    title: str = Field(description="전략의 제목")
    action_plan: List[ActionStep] = Field(min_items=3, max_items=3, description="3단계로 구성된 실행 계획")

class ActionPlanResponse(BaseModel):
    """최종 선정된 전략들에 대한 실행 계획 리스트"""
    plans: List[StrategyActionPlan] = Field(description="전략별 상세 실행 계획 목록")