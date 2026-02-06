from typing import List
from pydantic import BaseModel, Field, HttpUrl
from app.schemas.action_plan_schema import ActionDetailResponse, FinalSelectResponse
from app.schemas.swot_schema import SWOTResponse
from app.schemas.catchphrase_schema import CatchphraseResponse

# AI 분석 Request DTO의 태그
class TagInfo(BaseModel):
    type: str = Field(description="태그 타입", examples=["분위기"])
    name: str = Field(description="태그 이름", examples=["#뷰맛집"])

# 공통 데이터 모델 (핵심 정보)
class StoreInfo(BaseModel):
    store_id: int = Field(alias="storeId", description="가게 ID", examples=[1])
    name: str = Field(description="매장명", examples=["문화제빵"])
    address: str = Field(description="주소", examples=["서울 종로구 돈화문로 65 1층"])
    category: str = Field(description="업종", examples=["카페/베이커리"])
    category_detail: str = Field(alias="categoryDetail", description="업종 소분류", examples=["베이커리/디저트"])
    price: str = Field(description="가격대", examples=["1만원 미만"])
    target: str = Field(description="주 타겟", examples=["동네 주민"])
    pain_point: str = Field(alias="painPoint", description="사장님 고민", examples=["신규 손님이 너무 안 와요(모객)"])
    signature: str = Field(description="대표 메뉴", examples=["마늘빵"])
    tags: List[TagInfo] = Field(description="저장된 태그 목록")

    class Config:
        populate_by_name = True

# API 요청용 DTO (StoreInfo를 상속받음)
class AnalysisStoreRequest(StoreInfo):
    request_id: str = Field(
        alias="requestId", 
        description="요청 고유 ID", 
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    swot_callback_url: HttpUrl = Field(
        alias="swotCallbackUrl", 
        description="SWOT 분석 결과 수신 콜백 URL",
        examples=["http://localhost:8080/api/analysis/callback/swots"]
    )
    action_plan_callback_url: HttpUrl = Field(
        alias="actionPlanCallbackUrl", 
        description="ActionPlan 결과 수신 콜백 URL",
        examples=["http://localhost:8080/api/analysis/callback/action-plans"]
    )
    action_detail_callback_url: HttpUrl = Field(
        alias="actionDetailCallbackUrl", 
        description="ActionDetail 결과 수신 콜백 URL",
        examples=["http://localhost:8080/api/analysis/callback/action-details"]
    )
    fail_callback_url: HttpUrl = Field(
        alias="failCallbackUrl", 
        description="AI 분석 실패 콜백 URL",
        examples=["http://localhost:8080/api/analysis/callback/fail"]
    )

    class Config:
        populate_by_name = True

# 요약 정보 Request DTO
class SummaryRequest(BaseModel):
    address: str
    category: str
    storeName: str
    keyword: str

# 요약 정보 Response DTO
class SummaryResponse(BaseModel):
    mainAgeGroup: str
    mainGender: str
    peakTime: str
    avgDailyPop: int
    competitorCount: int
    competitionLevel: str
    avgMonthIncome: int
    mainHousingType: str
    topHashtags: str
    myReviewCount: int
    avgCompReviewCount: float
    myRating: float
    myReviewContents: str



# SWOT 분석 결과물 응답 DTO (콜백)
class SWOTCallbackResponse(BaseModel):    
    catchphrase: CatchphraseResponse
    swot: SWOTResponse


# ActionPlan 결과물 응답 DTO (콜백)
class ActionPlanCallbackResponse(BaseModel):
    action_plan: ActionDetailResponse

class FinalSelectCallbackResponse(BaseModel):
    final_select: FinalSelectResponse
