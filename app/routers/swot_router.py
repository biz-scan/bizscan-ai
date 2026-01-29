from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.common_schema import CommonResponse
from app.schemas.swot_summary_schema import SwotSummaryResponse
from app.schemas.swot_diagnosis_schema import SwotDiagnosisResponse
from app.services.swot_service import (
    generate_swot_summary,
    generate_swot_diagnosis,
)

router = APIRouter(
    prefix="/ai",
    tags=["SWOT Analysis"],
)


@router.post("/analysis", response_model=CommonResponse[SwotSummaryResponse])
async def swot_analysis(
    store_id: int,
    db: Session = Depends(get_db),
):
    """
    SWOT 요약 생성 API
    """
    result = generate_swot_summary(db, store_id)
    return CommonResponse(result=result)


@router.post("/diagnosis", response_model=CommonResponse[SwotDiagnosisResponse])
async def swot_diagnosis(
    store_id: int,
    swot_type: str,
    keyword: str,
    description: str,
    db: Session = Depends(get_db),
):
    """
    SWOT 항목 단일 정밀 진단 API
    """
    result = generate_swot_diagnosis(
        db,
        store_id,
        swot_type,
        keyword,
        description,
    )
    return CommonResponse(result=result)
