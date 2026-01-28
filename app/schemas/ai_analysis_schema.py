from typing import List
from pydantic import BaseModel, Field, HttpUrl
from app.schemas.action_plan_schema import ActionPlanResponse


class AnalysisStoreRequest(BaseModel):
    swot_callback_url: HttpUrl
    action_plan_callback_url: HttpUrl

class SWOTResponse(BaseModel):    
    swot: List[str] # 임시

class ActionPlanResponse(BaseModel):
    action_plan: ActionPlanResponse
