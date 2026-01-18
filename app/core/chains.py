from langchain_core.runnables import Runnable

from app.core.llm_client import build_structured_chain, chatOpenAI
from app.schemas.action_plan_schema import ActionPlanResponse
from app.core.prompt_templates.action_plan_templates import get_action_plan_prompt

action_plan_chain: Runnable = build_structured_chain(
    chatOpenAI,
    get_action_plan_prompt(),
    ActionPlanResponse,
)