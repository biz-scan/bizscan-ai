from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.common_schema import CommonResponse
from app.schemas.swot_schema import SwotResponse
from app.services.swot_service import generate_swot_analysis

router = APIRouter(
    prefix="/swot",
    tags=["SWOT Analysis"],
)

@router.post("/swot", response_model=CommonResponse[SwotResponse])
async def swot_analysis(
    store_id: int,
    db: Session = Depends(get_db),
):
    """
    SWOT 요약 + 심층 진단 통합 API
    """
    result = generate_swot_analysis(db, store_id)
    return CommonResponse(result=result)