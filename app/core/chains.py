from langchain_core.runnables import Runnable

from app.core.llm_client import build_structured_chain, chatOpenAI
from app.schemas.action_plan_schema import ActionPlanResponse, CandidateResponse, EvaluationResponse, SelectionResponse
from app.core.prompt_templates.candidate_prompt import get_candidate_prompt
from app.core.prompt_templates.evaluation_prompt import get_evaluation_prompt
from app.core.prompt_templates.final_select_prompt import get_selection_prompt
from app.core.prompt_templates.action_plan_prompt import get_action_plan_prompt

candidate_chain: Runnable = build_structured_chain(
    chatOpenAI,
    get_candidate_prompt(),
    CandidateResponse
)

evaluation_chain: Runnable = build_structured_chain(
    chatOpenAI,
    get_evaluation_prompt(),
    EvaluationResponse
)

selection_chain: Runnable = build_structured_chain(
    chatOpenAI,
    get_selection_prompt(),
    SelectionResponse
)

action_plan_chain: Runnable = build_structured_chain(
    chatOpenAI,
    get_action_plan_prompt(),
    ActionPlanResponse,
)

swot_chain: Runnable
catchphrase_chain: Runnable