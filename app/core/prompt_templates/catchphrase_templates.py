import json
from langchain_core.prompts import ChatPromptTemplate

from app.utils.prompt_formatting import format_example_for_prompt


def get_catchphrase_prompt() -> ChatPromptTemplate:
    # =========================
    # Few-shot 예시
    # =========================
    example_input_1 = {
        "store_info": {
            "storeId": 1,
            "name": "성수네 고깃집",
            "address": "서울 성동구 성수동",
            "category": "음식점",
            "categoryDetail": "고기/구이",
            "price": "2~3만원",
            "target": "3040 직장인",
            "painPoint": "신규 손님이 안 와요",
            "signature": "삼겹살",
            "tags": [{"type": "분위기", "name": "#활기찬"}]
        },
        "market_data": {
            "mainAgeGroup": "30대",
            "mainGender": "남성",
            "peakTime": "18-20시",
            "avgDailyPop": 5000,
            "competitorCount": 10,
            "competitionLevel": "높음",
            "avgMonthIncome": 4500000,
            "mainHousingType": "오피스 밀집",
            "topHashtags": "#회식 #삼겹살맛집",
            "myReviewCount": 150,
            "avgCompReviewCount": 120.5,
            "myRating": 4.8,            
        }
    }

    example_output_1 = {
        "catchphrase": "성수동 직장인 회식 1타"
    }

    example_input_2 = {
        "store_info": {
            "storeId": 2,
            "name": "연남 베이커리",
            "address": "서울 마포구 연남동",
            "category": "카페/베이커리",
            "categoryDetail": "베이커리/디저트",
            "price": "1만원 미만",
            "target": "20대 여성",
            "painPoint": "단골 확보가 어려워요",
            "signature": "크루아상",
            "tags": [{"type": "분위기", "name": "#감성"}, {"type": "특징", "name": "#아늑한"}]
        },
        "market_data": {
            "mainAgeGroup": "20대",
            "mainGender": "여성",
            "peakTime": "14-17시",
            "avgDailyPop": 8000,
            "competitorCount": 25,
            "competitionLevel": "중간",
            "avgMonthIncome": 2500000,
            "mainHousingType": "원룸/오피스텔",
            "topHashtags": "#디저트카페 #인생샷",
            "myReviewCount": 300,
            "avgCompReviewCount": 280.0,
            "myRating": 4.2,            
        }
    }

    example_output_2 = {
        "catchphrase": "연남동 감성 데이트의 완성"
    }

    formatting_example_input_1 = format_example_for_prompt(example_input_1)
    formatting_example_output_1 = format_example_for_prompt(example_output_1)
    formatting_example_input_2 = format_example_for_prompt(example_input_2)
    formatting_example_output_2 = format_example_for_prompt(example_output_2)

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
{{
  "catchphrase": "결과 문구"
}}
        """),

        # =========================
        # Few-shot 예시 1
        # =========================
        ("human", json.dumps(formatting_example_input_1, ensure_ascii=False)),
        ("ai", json.dumps(formatting_example_output_1, ensure_ascii=False)),

        # =========================
        # Few-shot 예시 2
        # =========================
        ("human", json.dumps(formatting_example_input_2, ensure_ascii=False)),
        ("ai", json.dumps(formatting_example_output_2, ensure_ascii=False)),

        # =========================
        # 실제 요청
        # =========================
        ("human", """
아래 입력 데이터를 바탕으로
동일한 규칙을 적용해 캐치프레이즈를 생성하라.

{{
  "store_info": {store_info},
  "market_data": {market_data}
}}
        """),
    ])
