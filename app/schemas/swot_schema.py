from pydantic import BaseModel, Field

class SwotResponse(BaseModel):
    strength: str = Field(description="강점 키워드")
    weakness: str = Field(description="약점 키워드")
    opportunity: str = Field(description="기회 키워드")
    threat: str = Field(description="위협 키워드")
    diagnosis: str = Field(description="SWOT 종합 심층 진단 (2~3문장)")