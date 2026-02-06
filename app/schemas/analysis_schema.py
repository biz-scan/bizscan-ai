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
    mainAgeGroup: str = Field(description="주요 방문 고객 연령대")
    mainGender: str = Field(description="주요 방문 고객 성별")
    peakTime: str = Field(description="매장이 가장 붐비는 시간대")
    avgDailyPop: int = Field(description="일평균 유동인구 수")
    competitorCount: int = Field(description="주변 경쟁 업체 수")
    competitionLevel: str = Field(description="상권 경쟁 강도 (예: 높음, 중간, 낮음)")
    avgMonthIncome: int = Field(description="상권 내 가구당 평균 월소득")
    mainHousingType: str = Field(description="상권의 주요 주거 형태 (예: 오피스 밀집, 원룸 등)")
    topHashtags: str = Field(description="상권을 대표하는 주요 해시태그")
    myReviewCount: int = Field(description="내 매장의 총 리뷰 수")
    avgCompReviewCount: float = Field(description="경쟁 업체들의 평균 리뷰 수")
    myRating: float = Field(description="내 매장의 평균 별점")
    myReviewContents: str = Field(
        description="내 매장 방문객들의 실제 리뷰 내용 요약 또는 대표적인 고객 피드백",
        example="고기가 구워져서 나와서 편해요. 직원들이 친절하지만 웨이팅이 좀 길어요."
    )



# SWOT 분석 결과물 응답 DTO (콜백)
class SWOTCallbackResponse(BaseModel):    
    catchphrase: CatchphraseResponse
    swot: SWOTResponse


# ActionPlan 결과물 응답 DTO (콜백)
class ActionPlanCallbackResponse(BaseModel):
    action_plan: ActionDetailResponse

class FinalSelectCallbackResponse(BaseModel):
    final_select: FinalSelectResponse
