import json
from langchain_core.prompts import ChatPromptTemplate


def get_catchphrase_prompt() -> ChatPromptTemplate:
    # =========================
    # Few-shot 예시
    # =========================
    example_input_1 = {
        "store_info": {
            "store_name": "성수네 고깃집",
            "location": "성수동",
            "category_main": "음식점",
            "category_sub": "고기/구이",
            "target_customer": "3040 직장인",
            "avg_price": "2~3만원",
            "main_menu": "삼겹살",
            "vibe_tags": ["#활기찬"]
        },
        "market_data": {
            "dominant_age_group": "30대",
            "dominant_gender": "남성",
            "peak_time": "18-20시",
            "competition_level": "높음",
            "avg_income_level": "높음",
            "housing_type_ratio": "오피스 밀집"
        }
    }

    example_output_1 = {
        "catchphrase": "성수동 직장인 회식 1타"
    }

    example_input_2 = {
        "store_info": {
            "store_name": "연남 베이커리",
            "location": "연남동",
            "category_main": "카페",
            "category_sub": "베이커리/디저트",
            "target_customer": "20대 여성",
            "avg_price": "5천원 내외",
            "main_menu": "크루아상",
            "vibe_tags": ["#감성", "#아늑한"]
        },
        "market_data": {
            "dominant_age_group": "20대",
            "dominant_gender": "여성",
            "peak_time": "14-17시",
            "competition_level": "중간",
            "avg_income_level": "보통",
            "housing_type_ratio": "1인 가구 55%"
        }
    }

    example_output_2 = {
        "catchphrase": "연남동 감성 데이트의 완성"
    }

    return ChatPromptTemplate.from_messages([
        # =========================
        # System (역할 + 규칙)
        # =========================
        ("system", """
너는 소상공인 가게의 강점을 발견해
한 문장의 슬로건으로 압축하는 천재 브랜드 카피라이터다.

[목표]
- 주어진 가게 정보(store_info)와 상권 데이터(market_data)를
  종합적으로 분석하고 추론하여
  이 가게의 핵심 매력을 가장 잘 드러내는
  'AI 캐치프레이즈'를 딱 하나 생성하라.

[핵심 규칙]
1. 반드시 제공된 JSON 데이터에 근거해서 생성하라.
2. 데이터들을 창의적으로 조합하여 숨겨진 컨셉을 추론하라.
   (예: '30대 직장인' + '고기/구이' + '18-20시' → '회식')
3. 결과는 공백 포함 15자 이내의 한글 문구여야 한다.
4. 이모지, 특수문자, 설명 문장, 따옴표를 포함하지 마라.
5. 결과는 반드시 아래 JSON 형식으로만 출력하라.

[출력 형식]
{
  "catchphrase": "결과 문구"
}
        """),

        # =========================
        # Few-shot 예시 1
        # =========================
        ("human", json.dumps({
            "store_info": example_input_1["store_info"],
            "market_data": example_input_1["market_data"]
        }, ensure_ascii=False)),
        ("ai", json.dumps(example_output_1, ensure_ascii=False)),

        # =========================
        # Few-shot 예시 2
        # =========================
        ("human", json.dumps({
            "store_info": example_input_2["store_info"],
            "market_data": example_input_2["market_data"]
        }, ensure_ascii=False)),
        ("ai", json.dumps(example_output_2, ensure_ascii=False)),

        # =========================
        # 실제 요청
        # =========================
        ("human", """
아래 입력 데이터를 바탕으로
동일한 규칙을 적용해 캐치프레이즈를 생성하라.

{
  "store_info": {store_info},
  "market_data": {market_data}
}
        """),
    ])
