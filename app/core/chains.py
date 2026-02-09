from langchain_core.runnables import Runnable

from app.core.llm_client import build_structured_chain, chatOpenAI_4o, chatOpenAI_5
from app.schemas.action_plan_schema import ActionDetailResponse, CandidateResponse, EvaluateResponse, FinalSelectResponse
from app.schemas.catchphrase_schema import CatchphraseResponse
from app.schemas.swot_schema import SWOTResponse

from app.core.prompt_templates.candidate_prompt import get_candidate_prompt
from app.core.prompt_templates.evaluate_prompt import get_evaluate_prompt
from app.core.prompt_templates.final_select_prompt import get_selection_prompt
from app.core.prompt_templates.action_detail_prompt import get_action_detail_prompt
from app.core.prompt_templates.catchphrase_templates import get_catchphrase_prompt
from app.core.prompt_templates.swot_templates import get_swot_prompt

swot_chain: Runnable = build_structured_chain(
    chatOpenAI_4o,
    get_swot_prompt(),
    SWOTResponse,
)
catchphrase_chain: Runnable = build_structured_chain(
    chatOpenAI_4o,
    get_catchphrase_prompt(),
    CatchphraseResponse,
)

candidate_chain: Runnable = build_structured_chain(
    chatOpenAI_4o,
    get_candidate_prompt(),
    CandidateResponse
)

evaluate_chain: Runnable = build_structured_chain(
    chatOpenAI_4o,
    get_evaluate_prompt(),
    EvaluateResponse
)

final_select_chain: Runnable = build_structured_chain(
    chatOpenAI_4o,
    get_selection_prompt(),
    FinalSelectResponse
)

action_detail_chain: Runnable = build_structured_chain(
    chatOpenAI_4o,
    get_action_detail_prompt(),
    ActionDetailResponse,
)

