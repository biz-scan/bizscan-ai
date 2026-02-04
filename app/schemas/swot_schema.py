from pydantic import BaseModel, Field
from typing import Literal

class SWOTItem(BaseModel):
    type: Literal["S", "W", "O", "T"] = Field(description="SWOT 타입 (S, W, O, T)")
    keyword: str = Field(description="SWOT 핵심 키워드")
    description: str = Field(description="상황 요약 설명")
    diagnosis: str = Field(description="해당 요소에 대한 심층 진단 (2~3문장)")

class SWOTResponse(BaseModel):
    strengths: SWOTItem
    weaknesses: SWOTItem
    opportunities: SWOTItem
    threats: SWOTItem



