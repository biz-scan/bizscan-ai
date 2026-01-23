from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.analysis_schema import AnalysisStoreResponse
from app.schemas.common_schema import CommonResponse
from app.core.database import get_db
from app.services.analysis_service import swot_ap_analysis

router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"],
)

@router.get("/stores/{store_id}")
async def analysis_store(
    store_id: int,
    db: Session = Depends(get_db),
):
    swot_ap_analysis(db, store_id)
    return CommonResponse(result=None)
    
