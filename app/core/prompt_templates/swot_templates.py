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
    "strengths": {
        "type": "S",
        "keyword": "가격 경쟁력 우수",
        "description": "객단가가 주변보다 낮아요",
        "diagnosis": (
            "해당 업체는 가격 경쟁력이 우수합니다. "
            "객단가가 주변보다 낮게 책정되어 있고, "
            "소비자들에게 높은 가성비를 제공함으로써 "
            "인근 경쟁 업체 대비 신규 고객 유입 및 시장 점유율 확보에 "
            "매우 유리한 위치를 점하고 있습니다."
        )
    },
    "weaknesses": {
        "type": "W",
        "keyword": "리뷰 수 부족",
        "description": "경쟁사 대비 20% 수준",
        "diagnosis": (
            "현재 온라인상에 축적된 리뷰 수가 경쟁사 대비 20% 수준에 머물러 있어 "
            "디지털 신뢰도가 매우 낮은 상태입니다. "
            "이는 가격 경쟁력이라는 확실한 강점이 있음에도 불구하고, "
            "실제 방문으로 이어지게 하는 사회적 증거가 부족하여 "
            "잠재 고객을 이탈시키는 주요 원인이 되고 있습니다."
        )
    },
    "opportunities": {
        "type": "O",
        "keyword": "20대 유동인구 상승",
        "description": "저녁 시간대 급증",
        "diagnosis": (
            "저녁 시간대를 중심으로 가성비를 중시하는 "
            "20대 유동인구가 급증하고 있는 점은 "
            "매출 성장의 강력한 기회 요인입니다. "
            "활동 패턴에 맞춘 마케팅이나 메뉴 구성을 통해 "
            "저녁 시간대 점유율을 빠르게 확대할 수 있습니다."
        )
    },
    "threats": {
        "type": "T",
        "keyword": "유사 업종 과포화",
        "description": "반경 500m 내 150개",
        "diagnosis": (
            "반경 500m 이내에 150개의 유사 업체가 밀집한 과포화 상태는 "
            "출혈 경쟁을 야기하는 심각한 위협입니다. "
            "단순 가격 경쟁만으로는 차별화가 어려워 "
            "브랜드 인지도를 확보하지 못할 경우 "
            "시장 내 도태 위험이 큽니다."
        )
    }
}

    return ChatPromptTemplate.from_messages([
        ("system", """
        너는 소상공인을 위한 데이터 기반 비즈니스 분석 AI다.

        [목표]
        제공된 매장 정보와 분석 데이터를 바탕으로
        SWOT(Strength, Weakness, Opportunity, Threat)를 각각 도출하라.

        각 SWOT 항목에 대해 반드시 다음 정보를 포함하라.
        - type: S, W, O, T 중 하나
        - keyword: 핵심 키워드 (짧은 명사형)
        - description: 해당 키워드에 대한 간단한 상황 설명
        - diagnosis: 해당 요소가 매장에 미치는 영향을 2~3문장으로 분석

        [SWOT 판단 기준]
        - Strength / Weakness는 내부 요인이다.
        - Opportunity / Threat는 외부 요인이다.
        - 현재 고민(pain_point)은 Weakness 판단 시 가장 중요한 단서로 활용하라.
        - 경쟁 수준과 상권 주거 형태 비율을 반드시 고려하라.

        [출력 규칙]
        - 반드시 지정된 JSON 형식만 출력하라.
        - 각 SWOT은 객체 형태로 작성하라.
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
