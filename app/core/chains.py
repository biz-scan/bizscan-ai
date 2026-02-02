from langchain_core.runnables import Runnable

from app.core.llm_client import build_structured_chain, chatOpenAI
from app.schemas.action_plan_schema import ActionDetailResponse, CandidateResponse, EvaluateResponse, FinalSelectResponse
from app.core.prompt_templates.candidate_prompt import get_candidate_prompt
from app.core.prompt_templates.evaluate_prompt import get_evaluate_prompt
from app.core.prompt_templates.final_select_prompt import get_selection_prompt
from app.core.prompt_templates.action_detail_prompt import get_action_detail_prompt

candidate_chain: Runnable = build_structured_chain(
    chatOpenAI,
    get_candidate_prompt(),
    CandidateResponse
)

evaluate_chain: Runnable = build_structured_chain(
    chatOpenAI,
    get_evaluate_prompt(),
    EvaluateResponse
)

final_select_chain: Runnable = build_structured_chain(
    chatOpenAI,
    get_selection_prompt(),
    FinalSelectResponse
)

action_detail_chain: Runnable = build_structured_chain(
    chatOpenAI,
    get_action_detail_prompt(),
    ActionDetailResponse,
)

swot_chain: Runnable
catchphrase_chain: Runnable