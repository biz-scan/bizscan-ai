import json
from langchain_core.prompts import ChatPromptTemplate


def get_swot_prompt() -> ChatPromptTemplate:
    # =========================
    # Few-shot 예시 (카페)
    # =========================
    example_input = {
        "category": "카페",
        "main_menu": "아메리카노",
        "avg_price": "4,000~5,000원",
        "mood_tag": "조용한",
        "target_customer": "20대 직장인",
        "operation_type": "1인 운영",
        "pain_point": "단골 고객 부족",

        "main_age_group": "20대",
        "main_gender": "남성",

        "competitor_count": 25,
        "competition_level": "HIGH",

        "apartment_ratio": 0.15,
        "house_ratio": 0.10,
        "office_ratio": 0.75,
    }

    example_output = {
        "strength": "조용한 매장 분위기",
        "weakness": "단골 고객 부족",
        "opportunity": "직장인 밀집 상권",
        "threat": "카페 경쟁 과열",
        "diagnosis": (
            "조용한 분위기와 1인 운영 방식은 혼자 시간을 보내려는 직장인에게 적합한 강점이다. "
            "다만 경쟁 카페 수가 많고 단골 고객이 부족해 매출 안정성이 낮은 상황이다. "
            "사무실 비율이 높은 지역 특성을 반복 방문으로 연결할 수 있는지가 향후 성과를 좌우한다."
        )
    }

    return ChatPromptTemplate.from_messages([
        ("system", """
너는 소상공인을 위한 데이터 기반 비즈니스 분석 AI다.

[목표]
1단계: 제공된 매장 정보와 분석 데이터를 바탕으로
        SWOT(Strength, Weakness, Opportunity, Threat)
        핵심 키워드를 각각 1개씩 도출하라.
2단계: 도출한 SWOT을 종합하여
        매장의 현재 상황을 2~3문장으로 심층 진단하라.

[SWOT 판단 기준]
- Strength / Weakness는 내부 요인이다.
- Opportunity / Threat는 외부 요인이다.
- 현재 고민(pain_point)은 Weakness 판단 시 가장 중요한 단서로 활용하라.
- 경쟁 수준과 상권 주거 형태 비율을 반드시 고려하라.

[출력 규칙]
- 반드시 지정된 JSON 형식만 출력하라.
- 키워드는 짧은 명사형으로 작성하라.
- diagnosis는 설명형 문장으로 2~3문장 작성하라.
- 실행 전략이나 해결책은 포함하지 마라.
        """),

        # ---------- Few-shot 입력 ----------
        ("human", f"""
[매장 정보]
- 업종: {example_input["category"]}
- 대표 메뉴: {example_input["main_menu"]}
- 객단가: {example_input["avg_price"]}
- 분위기 태그: {example_input["mood_tag"]}
- 주요 타겟: {example_input["target_customer"]}
- 운영 방식: {example_input["operation_type"]}
- 현재 고민: {example_input["pain_point"]}

[분석 데이터]
- 주요 이용 연령대: {example_input["main_age_group"]}
- 주요 이용 성별: {example_input["main_gender"]}
- 동종 업계 점포 수: {example_input["competitor_count"]}
- 경쟁 강도: {example_input["competition_level"]}
- 주거 형태 비율:
  - 아파트: {example_input["apartment_ratio"]}
  - 단독주택: {example_input["house_ratio"]}
  - 오피스: {example_input["office_ratio"]}
        """),

        # ---------- Few-shot 출력 ----------
        ("ai", json.dumps(example_output, ensure_ascii=False)),

        # ---------- 실제 요청 ----------
        ("human", """
[매장 정보]
- 업종: {category}
- 대표 메뉴: {main_menu}
- 객단가: {avg_price}
- 분위기 태그: {mood_tag}
- 주요 타겟: {target_customer}
- 운영 방식: {operation_type}
- 현재 고민: {pain_point}

[분석 데이터]
- 주요 이용 연령대: {main_age_group}
- 주요 이용 성별: {main_gender}
- 동종 업계 점포 수: {competitor_count}
- 경쟁 강도: {competition_level}
- 주거 형태 비율:
  - 아파트: {apartment_ratio}
  - 단독주택: {house_ratio}
  - 오피스: {office_ratio}

위 정보를 바탕으로 SWOT 분석과 심층 진단을 생성하라.
        """),
    ])
