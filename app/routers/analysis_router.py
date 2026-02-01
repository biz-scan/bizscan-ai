from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.schemas.analysis_schema import AnalysisStoreRequest
from app.schemas.common_schema import CommonResponse
from app.core.database import get_db
from app.services.analysis_service import run_analysis_flow

router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"],
)
    
@router.post("")
async def analysis_store(
    request_data: AnalysisStoreRequest,
    background_tasks: BackgroundTasks,
):
    
    background_tasks.add_task(run_analysis_flow, request_data)
    
    # SpringBoot에는 요청을 받았음을 즉시 응답
    return CommonResponse(result=None)


