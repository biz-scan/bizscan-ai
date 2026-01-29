from langchain_core.prompts import ChatPromptTemplate

def catchphrase_prompt(store: dict, swot: dict) -> str:
    return f"""
너는 소상공인 매장의 브랜드를 한 문장으로 요약하는 AI다.

아래 정보를 바탕으로
이 매장을 대표하는 캐치프레이즈를 하나 생성하라.

[매장 정보]
- 업종: {store.get("category")}
- 대표 메뉴: {store.get("main_menu")}
- 주요 타겟: {store.get("target")}

[SWOT 요약]
- 강점: {swot.get("strength")}
- 기회: {swot.get("opportunity")}

[조건]
- 한글
- 공백 포함 15자 이내
- 설명 없이 문구만 출력
- 이모지, 특수문자 금지
"""
