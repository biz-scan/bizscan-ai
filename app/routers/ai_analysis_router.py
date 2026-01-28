from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.schemas.analysis_schema import AnalysisStoreRequest
from app.schemas.common_schema import CommonResponse
from app.core.database import get_db
from app.services.action_plan_service import create_action_plan

router = APIRouter(
    prefix="/api/ai-analysis",
    tags=["AiAnalysis"],
)
    
@router.post("/stores/{store_id}")
async def analysis_store(
    store_id: int,
    request_data: AnalysisStoreRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    swot_data: Dict[str, Any]
    # 백그라운드에서 작업 시작
    background_tasks.add_task(create_action_plan, swot_data, request_data.action_plan_callback_url)
    
    # SpringBoot에는 요청을 받았음을 즉시 응답
    return CommonResponse(result={"message": "Analysis started"})
