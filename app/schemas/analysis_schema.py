from typing import List
from pydantic import BaseModel, Field, HttpUrl
from app.schemas.action_plan_schema import ActionPlanResponse

# AI 분석 Request DTO의 태그
class TagInfo(BaseModel):
    id: int = Field(description="태그 ID", examples=[10])
    type: str = Field(description="태그 타입", examples=["MOOD"])
    name: str = Field(description="태그 이름", examples=["VIEW"])

# AI 분석 Request DTO
class AnalysisStoreRequest(BaseModel):
    # 콜백 URL
    swot_callback_url: HttpUrl
    action_plan_callback_url: HttpUrl
    
    storeId: int = Field(description="가게 ID", examples=[1])
    name: str = Field(description="매장명", examples=["문화제빵"])
    address: str = Field(description="주소", examples=["서울 종로구 돈화문로 65 1층"])
    category: str = Field(description="업종", examples=["카페/베이커리"])
    categoryDetail: str = Field(description="업종 소분류", examples=["베이커리/디저트"])
    signature: str = Field(description="대표 메뉴", examples=["마늘빵"])
    price: str = Field(description="가격대", examples=["1만원 미만"])
    target: str = Field(description="주 타겟", examples=["동네 주민"])
    painPoint: str = Field(description="사장님 고민", examples=["신규 손님이 너무 안 와요(모객)"])
    
    # 태그 목록
    tags: List[TagInfo] = Field(description="저장된 태그 목록")

    class Config:
        # JSON 데이터의 필드명을 Java와 동일하게 유지 (CamelCase)
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

class StoreInfo(BaseModel):
    storeName: str

# SWOT 분석 결과물 응답 DTO (콜백)
class SWOTCallbackResponse(BaseModel):    
    swot: List[str] # 임시


# ActionPlan 결과물 응답 DTO (콜백)
class ActionPlanCallbackResponse(BaseModel):
    status: str
    action_plan: ActionPlanResponse