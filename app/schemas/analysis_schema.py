from typing import List
from pydantic import BaseModel, Field
from app.schemas.action_plan_schema import ActionPlanResponse


class AnalysisStoreResponse(BaseModel):
    swot: List[str] # 임시
    action_plan: ActionPlanResponse
