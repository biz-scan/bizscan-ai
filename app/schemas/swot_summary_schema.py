from pydantic import BaseModel, Field

class SwotSummaryResponse(BaseModel):
  strength: str = Field(description="강점 키워드 (예: 가격 경쟁력 우수)")
  weakness: str = Field(description="약점 키워드 (예: 단골 고객 확보 어려움)")
  opportunity: str = Field(description="기회 키워드 (예: 20대 유동인구 증가)")
  threat: str = Field(description="위협 키워드 (예: 유사 업종 과포화)")