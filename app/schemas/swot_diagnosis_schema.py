from pydantic import BaseModel, Field

class SwotDiagnosisResponse(BaseModel):
  diagnosis: str = Field(
    description="선택된 SWOT 항목에 대한 2~3문장의 심층 진단 텍스트"
  )