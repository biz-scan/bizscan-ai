from typing import Optional
from pydantic import BaseModel, Field

class CatchphraseResponse(BaseModel):
    catchphrase: Optional[str] = Field(
        description="AI가 생성한 매장 캐치프레이즈"
    )
