from pydantic import BaseModel, Field
from typing import Literal

class SWOTItem(BaseModel):
    type: Literal["S", "W", "O", "T"]
    keyword: str
    description: str
    diagnosis: str

class SWOTResult(BaseModel):
    strengths: SWOTItem
    weaknesses: SWOTItem
    opportunities: SWOTItem
    threats: SWOTItem
    