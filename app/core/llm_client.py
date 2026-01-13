import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable

# 환경변수 로드
load_dotenv()

# API 키 검증
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

# LLM 인스턴스
chatOpenAI = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

# Pydantic 구조화 출력 체인
def build_structured_chain(
    llm: ChatOpenAI,
    prompt,
    output_schema,
) -> Runnable:
    structured_llm = llm.with_structured_output(output_schema)
    return prompt | structured_llm