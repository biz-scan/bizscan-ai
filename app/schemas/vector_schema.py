from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class SwotItem(BaseModel):
    type: str         # S, W, O, T
    keyword: str
    description: str
    diagnosis: Optional[str] = None
    rawText: str

class StoreSwotIngestRequest(BaseModel):
    store_id: int = Field(alias="storeId")
    catchphrase: str = Field(..., description="가게의 핵심 캐치프레이즈")
    items: List[SwotItem]

    model_config = ConfigDict(populate_by_name=True)

class SimilarityResult(BaseModel):
    store_id: int = Field(alias="storeId")
    catchphrase: Optional[str] = Field(None, alias="catchphrase")
    score: float
    raw_text: Optional[str] = Field(None, alias="rawText")

    model_config = ConfigDict(populate_by_name=True)

class SimilarityResponse(BaseModel):
    results: List[SimilarityResult]