from pydantic import BaseModel, Field
from typing import Literal

class SWOTItem(BaseModel):
    type: Literal["S", "W", "O", "T"]
    keyword: str
    description: str
    diagnosis: str

class SWOTResponse(BaseModel):
    strengths: SWOTItem
    weaknesses: SWOTItem
    opportunities: SWOTItem
    threats: SWOTItem
    
class CatchphraseResponse(BaseModel):
    catchphrase: str = Field(
        description="AI가 생성한 매장 캐치프레이즈"
    )

    