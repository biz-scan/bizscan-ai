from pydantic import BaseModel, Field

class SwotItem(BaseModel):
    type: str = Field(description="SWOT 타입 (S, W, O, T)")
    keyword: str = Field(description="SWOT 핵심 키워드")
    description: str = Field(description="상황 요약 설명")
    diagnosis: str = Field(description="해당 요소에 대한 심층 진단 (2~3문장)")

class SwotResponse(BaseModel):
    strengths: SwotItem
    weaknesses: SwotItem
    opportunities: SwotItem
    threats: SwotItem
