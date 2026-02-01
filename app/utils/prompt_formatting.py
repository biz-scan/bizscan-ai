import json
from typing import Any

def format_example_for_prompt(data: Any) -> str:
    """
    JSON 데이터를 문자열로 변환하고, 
    LangChain 프롬프트 템플릿(str.format)을 위해 중괄호({})를 이스케이프합니다.
    """
    if not data:
        return ""
    
    # 1. JSON 문자열 변환
    json_str = json.dumps(data, ensure_ascii=False)
    
    # 2. { -> {{, } -> }} 로 치환
    return json_str.replace("{", "{{").replace("}", "}}")