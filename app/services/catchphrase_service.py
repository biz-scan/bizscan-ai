from sqlalchemy.orm import Session

from app.core.llm_client import call_llm
from app.core.prompt_templates.tmp_templates import catchphrase_prompt
from app.crud.tmp_crud import get_store_info, get_latest_swot_summary

def generate_catchphrase(db: Session, store_id: int) -> str | None:
    store = get_store_info(db, store_id)
    swot = get_latest_swot_summary(db, store_id)

    if not store or not swot:
        return None

    prompt = catchphrase_prompt(store, swot)
    result = call_llm(prompt)

    if not result:
        return None

    text = result.strip()

    return text[:15]  # 15자 제한
