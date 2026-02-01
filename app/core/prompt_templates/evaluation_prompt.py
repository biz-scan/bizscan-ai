import json
from langchain_core.prompts import ChatPromptTemplate

from app.utils.prompt_formatting import format_example_for_prompt

# 2. 후보 전략 평가 Chain
def get_evaluation_prompt() -> ChatPromptTemplate:
    # Few-shot Input
    example_swot = {
        "strengths": {
            "type": "S",
            "keyword": "가격 경쟁력 우수",
            "description": "객단가가 주변보다 낮아요",
            "diagnosis": "해당 업체는 가격 경쟁력이 우수합니다. 객단가가 주변보다 낮게 책정되어 있고, 소비자들에게 높은 가성비를 제공함으로써 인근 경쟁 업체 대비 신규 고객 유입 및 시장 점유율 확보에 매우 유리한 위치를 점하고 있습니다."
        },
        "weaknesses": {
            "type": "W",
            "keyword": "리뷰 수 부족",
            "description": "경쟁사 대비 20% 수준",
            "diagnosis": "현재 온라인상에 축적된 리뷰 수가 경쟁사 대비 20% 수준에 머물러 있어, 디지털 신뢰도가 매우 낮은 상태입니다. 이는 가격 경쟁력이라는 확실한 강점이 있음에도 불구하고, 실제 방문으로 이어지게 하는 '사회적 증거'가 부족하여 잠재 고객을 이탈시키는 주요 원인이 되고 있습니다."
        },
        "opportunities": {
            "type": "O",
            "keyword": "20대 유동인구 상승",
            "description": "저녁 시간대 급증",
            "diagnosis": "저녁 시간대를 중심으로 가성비를 중시하는 20대 유동인구가 급증하고 있는 점은 매출 성장의 강력한 기회 요인입니다. 이들의 활동 패턴에 맞춘 마케팅이나 메뉴 구성을 통해 유입을 유도한다면, 현재의 가격 경쟁력을 극대화하여 저녁 시간대 점유율을 빠르게 확대할 수 있습니다."
        },
        "threats": {
            "type": "T",
            "keyword": "유사 업종 과포화",
            "description": "반경 500m 내 150개",
            "diagnosis": "반경 500m 이내에 150개의 유사 업체가 밀집해 있는 과포화 상태는 시장 진입 장벽을 낮추고 출혈 경쟁을 야기하는 심각한 위협입니다. 단순한 가격 우위만으로는 차별화를 꾀하기 어려우며, 강력한 브랜드 인지도를 구축하지 못할 경우 치열한 점유율 싸움에서 도태될 위험이 큽니다."
        }
    }
    
    
    example_candidates = [
        {
            "id": 1,
            "title": "20대 타겟 '저녁 가성비 실속 세트' 출시",
            "tags": ["#매출증대", "#난이도하", "#상품개발"],
            "related_swot": ["S", "O"],
            "reason": "우수한 가격 경쟁력(S)과 저녁 시간대 급증하는 20대 유동인구(O)를 결합하여, 퇴근 및 하교길 청년층의 집객을 유도하는 SO 전략이다."
        },
        {
            "id": 2,
            "title": "리뷰 작성 시 '저녁 시간 전용' 할인권 증정",
            "tags": ["#인지도제고", "#난이도하", "#마케팅"],
            "related_swot": ["W", "O"],
            "reason": "부족한 리뷰 수(W)를 보완하기 위해 저녁 유동인구(O)를 대상으로 참여형 이벤트를 열어 디지털 신뢰도를 빠르게 확보하는 WO 전략이다."
        },
        {
            "id": 3,
            "title": "지역 내 '최저가 보상제' 및 단골 혜택 강화",
            "tags": ["#신규고객", "#난이도중", "#고객관리"],
            "related_swot": ["S", "T"],
            "reason": "치열한 과포화 시장(T)에서 압도적인 가격 우위(S)를 확실히 각인시켜 경쟁 업체들 사이에서 독보적인 시장 점유율을 지키는 ST 전략이다."
        },
        {
            "id": 4,
            "title": "네이버 플레이스 정보 최적화 및 신뢰 캠페인",
            "tags": ["#바이럴", "#난이도중", "#마케팅"],
            "related_swot": ["W", "T"],
            "reason": "낮은 디지털 신뢰도(W)를 개선하고 밀집된 경쟁사(T)들 사이에서 선택받기 위해, 매장의 강점을 온라인에 상세히 노출하여 이탈률을 줄이는 WT 전략이다."
        },
        {
            "id": 5,
            "title": "SNS 인증용 '오늘의 가성비 메뉴' 매일 공개",
            "tags": ["#운영효율", "#난이도중", "#마케팅"],
            "related_swot": ["S", "O"],
            "reason": "높은 가성비(S)를 선호하는 20대(O)의 특성에 맞춰 매일 다른 할인 상품을 SNS로 노출하여 신규 고객의 지속적인 유입을 만드는 고도화된 SO 전략이다."
        }
    ]
    
    # Few-shot Output
    example_output = [
        {
            "id": 1, 
            "impactScore": 9, 
            "effortScore": 3, 
            "evaluation": "성장세인 20대 유동인구를 타겟으로 강점인 가성비를 극대화하여 즉각적인 매출 상승이 기대되며, 기존 재료를 활용한 세트 구성이라 실행도 간편하다."
        },
        {
            "id": 2, 
            "impactScore": 8, 
            "effortScore": 2, 
            "evaluation": "가장 큰 약점인 리뷰 부족 문제를 저비용 할인권으로 해결하여 디지털 신뢰도를 빠르게 높일 수 있는 가성비 높은 전략이다."
        },
        {
            "id": 3, 
            "impactScore": 7, 
            "effortScore": 5, 
            "evaluation": "과포화 시장에서 확실한 우위를 점할 수 있는 강력한 카드지만, 경쟁사 가격 모니터링과 단골 관리 시스템 구축에 일정 수준의 운영 공수가 필요하다."
        },
        {
            "id": 4, 
            "impactScore": 6, 
            "effortScore": 4, 
            "evaluation": "장기적인 매장 신뢰도 구축에 필수적이나, 플레이스 정보 최적화와 콘텐츠 제작 등 초기 세팅 및 관리에 시간이 소요되는 측면이 있다."
        },
        {
            "id": 5, 
            "impactScore": 7, 
            "effortScore": 6, 
            "evaluation": "매일 새로운 정보를 제공하여 재방문을 유도하는 효과는 크지만, 담당자가 매일 SNS 콘텐츠를 업로드하고 소통해야 하는 운영 부담이 따른다."
        }
    ]

    formatting_example_swot = format_example_for_prompt(example_swot)
    formatting_example_candidates = format_example_for_prompt(example_candidates)
    formatting_example_output = format_example_for_prompt(example_output)

    # AI 프롬프트
    return ChatPromptTemplate.from_messages([
        ("system", """
        너는 생성된 비즈니스 전략 후보군을 객관적인 데이터와 시장 상황을 바탕으로 평가하는 전략 분석가다.

        ### 목표
        제시된 3~5개의 전략 후보군에 대해 '기대 효과(Impact)'와 '실행 난이도(Effort)'를 평가하라.

        ### 평가 기준
        1. **기대 효과 (Impact)**: 
            - 0~10점 (높을수록 좋음)
            - 매출 증대 가능성, 신규 고객 유입량, 브랜드 인지도 향상 등을 고려하라.
        2. **실행 난이도 (Effort)**: 
            - 0~10점 (낮을수록 실행이 쉬움)
            - 소요 시간, 자금 투자 규모, 기술적 복잡성, 인력 필요도를 고려하라.
            - Effort 점수는 투입되는 자원(시간, 자금, 인력)의 양을 의미한다. 1점은 사장님 혼자 즉시 할 수 있는 일이며, 10점은 외부 업체 고용이나 큰 자본 투자가 필요한 일이다.

        ### 핵심 규칙
        - `evaluation`은 왜 해당 점수를 부여했는지 전략적 근거를 2문장 내외로 서술하라.
        - SWOT 분석 결과와 전략의 연관성을 고려하여 평가의 객관성을 유지하라.
        """),

        # Few-shot: Human 예시 (SWOT + 후보군)
        ("human", f"""
        ### SWOT 데이터:
        {formatting_example_swot}

        ### 전략 후보군:
        {formatting_example_candidates}
        """),
        
        # Few-shot: AI 응답 예시 (평가 결과)
        ("ai", formatting_example_output),

        # 실제 사용자 요청
        ("human", """
        ### SWOT 데이터:
        {swot_json}

        ### 전략 후보군:
        {candidate_list}

        위 후보군들에 대해 'Impact'와 'Effort' 점수를 산출하고 그 이유를 분석해줘.
        """),
    ])