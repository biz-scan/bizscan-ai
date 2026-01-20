from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.store_schema import StoreAnalysisResponse
from app.schemas.common_schema import CommonResponse
from app.core.database import get_db
from app.services.store_service import swot_ap_analysis

router = APIRouter(
    prefix="/api/stores",
    tags=["Store"],
)

@router.get("/{store_id}/analysis")
async def analysis_store(
    store_id: int,
    db: Session = Depends(get_db),
):
    swot_ap_analysis(db, store_id)
    return CommonResponse(result=None)
    
