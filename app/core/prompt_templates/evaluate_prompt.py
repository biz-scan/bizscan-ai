import json
from langchain_core.prompts import ChatPromptTemplate

from app.utils.prompt_formatting import format_example_for_prompt

# 2. 후보 전략 평가 Chain
def get_evaluate_prompt() -> ChatPromptTemplate:
    # Few-shot Input
    example_swot = {
        "factor_1": {
            "type": "S",
            "keyword": "가격 경쟁력 우수",
            "description": "객단가가 주변보다 낮아요",
            "diagnosis": "해당 업체는 가격 경쟁력이 우수합니다. 객단가가 주변보다 낮게 책정되어 있고, 소비자들에게 높은 가성비를 제공함으로써 인근 경쟁 업체 대비 신규 고객 유입 및 시장 점유율 확보에 매우 유리한 위치를 점하고 있습니다."
        },
        "factor_2": {
            "type": "O",
            "keyword": "20대 유동인구 상승",
            "description": "저녁 시간대 급증",
            "diagnosis": "저녁 시간대를 중심으로 가성비를 중시하는 20대 유동인구가 급증하고 있는 점은 매출 성장의 강력한 기회 요인입니다. 이들의 활동 패턴에 맞춘 마케팅이나 메뉴 구성을 통해 유입을 유도한다면, 현재의 가격 경쟁력을 극대화하여 저녁 시간대 점유율을 빠르게 확대할 수 있습니다."
        }
    }
    
    
    example_candidates = [
        {
            "id": 1,
            "title": "20대 타겟 '저녁 가성비 실속 세트' 출시",
            "tags": ["#매출증대", "#난이도하", "#상품개발"],
            "related_swot": ["S", "O"],
            "reason": "우수한 가격 경쟁력(S)과 저녁 시간대 20대 유동인구(O)를 결합하여, 퇴근길 청년층의 집객을 유도하는 SO 전략입니다."
        },
        {
            "id": 2,
            "title": "SNS 인증용 '오늘의 가성비 메뉴' 매일 공개",
            "tags": ["#바이럴", "#난이도중", "#마케팅"],
            "related_swot": ["S", "O"],
            "reason": "높은 가성비(S)를 선호하는 20대(O)의 특성에 맞춰 매일 다른 할인 상품을 SNS로 노출하여 유입을 만드는 SO 전략입니다."
        },
        {
            "id": 3,
            "title": "저녁 피크타임 '가성비 1인 혼밥존' 운영",
            "tags": ["#운영효율", "#난이도하", "#시설개선"],
            "related_swot": ["S", "O"],
            "reason": "가격에 민감한 20대 1인 가구(O)의 방문 허들을 낮추기 위해 매장의 가격 우위(S)를 강조한 전용 공간을 제안합니다."
        },
        {
            "id": 4,
            "title": "대학생 서포터즈 '가성비 검증단' 운영",
            "tags": ["#인지도제고", "#난이도상", "#마케팅"],
            "related_swot": ["S", "O"],
            "reason": "주변 20대 유입 기회(O)를 활용해 매장의 최대 강점인 가격(S)을 지역 커뮤니티에 확산시키는 고도화된 SO 전략입니다."
        }
    ]
    
    # Few-shot Output
    example_output = [
        {
            "id": 1, 
            "impactScore": 9, 
            "effortScore": 3, 
            "evaluate": "성장세인 20대 유동인구를 타겟으로 강점인 가성비를 극대화하여 즉각적인 매출 상승이 기대되며, 기존 재료를 활용한 세트 구성이라 실행도 간편합니다."
        },
        {
            "id": 2, 
            "impactScore": 7, 
            "effortScore": 5, 
            "evaluate": "20대 트렌드에 적합한 바이럴 전략이나, 매일 새로운 콘텐츠를 제작하고 관리해야 하는 사장님의 운영 공수가 지속적으로 발생합니다."
        },
        {
            "id": 3, 
            "impactScore": 6, 
            "effortScore": 2, 
            "evaluate": "혼밥족 유입을 통한 회전율 개선 효과는 있으나, 가성비 세트 출시에 비해 객단가 상승이나 폭발적인 매출 증대 효과는 다소 제한적일 수 있습니다."
        },
        {
            "id": 4, 
            "impactScore": 8, 
            "effortScore": 8, 
            "evaluate": "지역 내 확실한 브랜딩이 가능해 기대 효과는 매우 크지만, 서포터즈 모집 및 운영 관리에 상당한 시간과 비용이 소요되는 고난도 전략입니다."
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
        특정 SWOT 조합을 통해 도출된 4개의 전략 후보군에 대해 '기대 효과(Impact)'와 '실행 난이도(Effort)'를 평가하라.

        ### 평가 기준
        1. **기대 효과 (Impact)**: 
            - 0~10점 (높을수록 좋음)
            - 매출 증대 가능성, 신규 고객 유입량, 브랜드 인지도 향상, 시장 점유율 확보 가능성 등을 고려하라.
        2. **실행 난이도 (Effort)**: 
            - 0~10점 (숫자가 작을수록 실행이 쉬움 / 숫자가 클수록 자원이 많이 필요함)
            - 1~3점: 사장님 혼자 즉시 실행 가능 (예: 메뉴판 수정, 간단한 홍보물 부착)
            - 4~6점: 약간의 자금이나 준비 시간 필요 (예: 새로운 식재료 수급, 간단한 SNS 광고)
            - 7~10점: 외부 업체 고용, 대규모 시설 투자, 장기적인 운영 관리 필요

        ### 핵심 규칙
        - **ID 일관성**: 각 평가 결과의 `id`는 반드시 입력받은 전략 후보군의 `id`와 동일해야 한다.
        - `evaluate` 필드에는 점수 부여의 근거를 '가성비'와 '전략적 가치' 관점에서 2문장 내외로 서술하라.
        - 입력된 SWOT 요소의 `diagnosis`와 전략의 연관성을 분석하여 평가의 객관성을 유지하라.
        - 4개의 전략이 서로 변별력을 가질 수 있도록 점수를 신중하게 산출하라.
        """),

        # Few-shot: Human 예시 (SWOT + 후보군)
        ("human", f"""
        ### 분석 대상 데이터:
        {formatting_example_swot}

        ### 평가할 전략 후보군:
        {formatting_example_candidates}
        """),
        
        # Few-shot: AI 응답 예시 (평가 결과)
        ("ai", formatting_example_output),

        # 실제 사용자 요청
        ("human", """
        ### 분석 대상 데이터:
        {swot_json}

        ### 평가할 전략 후보군:
        {candidate_list}

        위 후보군들에 대해 'Impact'와 'Effort' 점수를 산출하고 그 이유를 전문적으로 분석해줘.
        """),
    ])