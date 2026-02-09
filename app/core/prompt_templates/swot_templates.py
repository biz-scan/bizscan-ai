import json
from langchain_core.prompts import ChatPromptTemplate

from app.utils.prompt_formatting import format_example_for_prompt


def get_swot_prompt() -> ChatPromptTemplate:
    # =========================
    # Few-shot 예시 (카페)
    # =========================
    example_input = {
        "store_info": {
            "storeId": 1,
            "name": "문화제빵",
            "address": "서울 성동구 성수동",
            "category": "카페/베이커리",
            "categoryDetail": "베이커리/디저트",
            "price": "5,000원 내외",
            "target": "가성비를 중시하는 젊은 층",
            "painPoint": "온라인 인지도 부족",
            "signature": "마늘빵",
            "tags": [{"type": "분위기", "name": "#조용한"}]
        },
        "market_data": {
            "mainAgeGroup": "20대",
            "mainGender": "여성",
            "peakTime": "18-21시",
            "avgDailyPop": 5000,
            "competitorCount": 150,
            "competitionLevel": "HIGH",
            "avgMonthIncome": 2500000,
            "mainHousingType": "원룸 및 오피스 밀집",
            "topHashtags": "#마늘빵맛집 #가성비카페",
            "myReviewCount": 20,
            "avgCompReviewCount": 100.0,
            "myRating": 4.5,            
        }
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
    formatting_example_input = format_example_for_prompt(example_input)
    formatting_example_output = format_example_for_prompt(example_output)

    return ChatPromptTemplate.from_messages([
        ("system", """
        너는 소상공인을 위한 데이터 기반 비즈니스 분석 AI다.

        [목표]
        제공된 매장 정보와 분석 데이터를 바탕으로
        SWOT(Strength, Weakness, Opportunity, Threat)를 각각 도출하라.

        각 SWOT 항목에 대해 반드시 다음 정보를 포함하라.
        - type: S, W, O, T 중 하나
        - keyword: 핵심 키워드 (짧은 명사형)
        - description: 해당 키워드에 대한 18자 이내의 간단한 상황 설명
        - diagnosis: 해당 요소가 매장에 미치는 영향을 2~3문장으로 분석

        [SWOT 추론 로직 가이드라인]

        SWOT은 임의로 생성하지 말고,
        아래에 정의된 추론 방식을 기준으로 논리적으로 도출하라.
        각 항목(S/W/O/T)은 가장 강하게 부합하는 조건 1가지를 선택한다.
        
        각 SWOT 항목을 생성할 때,
        먼저 어떤 추론 조건(IF 기준)을 선택했는지 내부적으로 결정한 후,
        그 선택 결과를 keyword, description, diagnosis에 일관되게 반영하라.

        ────────────────
        1. Strengths (강점: 내부 요인, 긍정)
        ────────────────
        추론 기준:
        - 사용자가 입력한 store_info(price, target, tags 등)를
        market_data와 비교하여
        상대적으로 "우위"에 해당하는 요소를 강점으로 도출한다.

        추론 예시:
        - IF store_info.price < 지역 평균 객단가
        → keyword: "가격 경쟁력 우수"
        - IF store_info.target과 market_data.mainAgeGroup의 연령대가 일치
        → keyword: "명확한 타겟 고객층"
        - IF store_info.tags에 '#단체석' 포함 AND market_data.mainHousingType에 '오피스' 비중 높음 
          → keyword: "직장인 단체 수요 가능"
        - IF store_info.signature가 확실하고 market_data.myRating >= 4.0 
        → keyword: "검증된 상품 경쟁력"
        - IF store_info.tags나 signature가 market_data.topHashtags와 일치
        → keyword: "트렌드 적합성 우수"

        ────────────────
        2. Weaknesses (약점: 내부 요인, 부정)
        ────────────────
        추론 기준:
        - 사용자가 입력한 store_info.painPoint을
        가장 우선적인 판단 근거로 사용한다.
        - market_data 대비
        매장이 불리한 내부 요소를 약점으로 도출한다.

        추론 예시:
        - IF store_info.painPoint가 재방문이나 단골 관련 내용임
        → keyword: "재방문율 낮음"
        - IF market_data.competitorCount > 100 
        → keyword: "높은 경쟁 강도"
        - IF store_info.categoryDetail이 '테이크아웃 전문' BUT market_data.peakTime이 '저녁' 
        → keyword: "저녁 시간대 매출 약세"
        - IF market_data.myReviewCount < market_data.avgCompReviewCount
        → keyword: "온라인 신뢰도 부족"
        - IF market_data.myRating < 3.5
        → keyword: "상품/서비스 품질 개선 필요"

        ────────────────
        3. Opportunities (기회: 외부 요인, 긍정)
        ────────────────
        추론 기준:
        - market_data의 환경 변화 중
        store_info의 특성과 결합했을 때 시너지가 발생할 수 있는 요소를 도출한다.

        추론 예시:
        - IF market_data.mainAgeGroup/mainGender가 store_info.target과 부합
        → keyword: "주요 수요층 집중"
        - IF market_data.peakTime이 '12-14시'로 집중 
          → keyword: "직장인 점심 특수"
        - IF market_data.mainHousingType이 1인 가구 위주이고 매장이 배달/테이크아웃 강점
        → keyword: "특정 수요층 확대"
        - IF market_data.avgMonthIncome이 높음
        → keyword: "높은 소비 잠재력"

        ────────────────
        4. Threats (위협: 외부 요인, 부정)
        ────────────────
        추론 기준:
        - 시장의 부정적 환경 요소 중
        매장에 직접적인 리스크가 되는 요인을 도출한다.

        추론 예시:
        - IF market_data.competitorCount > 150
        → keyword: "동종 업계 과포화"
        - IF market_data.competitionLevel == 'HIGH'
        → keyword: "가격 경쟁 심화"        

        ────────────────
        [출력 강제 규칙]
        - 각 SWOT 항목은 반드시 위 추론 규칙 중 하나에 근거해야 한다.
        - keyword는 추론 결과를 요약한 명사형 문구여야 한다.
        - description은 데이터 또는 상황 요약이다.
        - diagnosis는 선택된 추론 근거를 자연어로 풀어 설명한 것이다.

        [출력 강제 규칙]
        - strengths.type = "S"
        - weaknesses.type = "W"
        - opportunities.type = "O"
        - threats.type = "T"
        - 각 SWOT 항목은 반드시 위 추론 규칙 중 하나에 근거해야 한다.
        - keyword는 명사형으로 작성한다.
        - description은 데이터 또는 상황 요약이다.
        - diagnosis는 선택한 추론 근거를 자연어로 풀어 설명한다.
        - 반드시 지정된 JSON 형식만 출력하라.
        """),

    ("human", json.dumps(formatting_example_input, ensure_ascii=False)),

    # ---------- Few-shot 출력 ----------
    ("ai", json.dumps(formatting_example_output, ensure_ascii=False)),

    ("human", """
아래 입력 데이터를 바탕으로 SWOT 분석과 심층 진단을 생성하라.

{{
  "store_info": {store_info},
  "market_data": {market_data}
}}
        """),
            ])
