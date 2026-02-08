import json
from langchain_core.prompts import ChatPromptTemplate

from app.utils.prompt_formatting import format_example_for_prompt

# 3. 최종 선정 Chain
def get_selection_prompt() -> ChatPromptTemplate:
    # 1단계: SWOT 데이터 정의
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

    # 2단계: 1번 프롬프트에서 생성된 후보군 (4개)
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

    # 3단계: 2번 프롬프트에서 생성된 평가 결과 (5개)
    example_evaluate = [
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

    # 최종 결과물: 가성비(Impact 높고 Effort 낮은) 및 다양성 고려한 상위 3개 선정
    example_output = [
        {
            "id": 1,
            "title": "20대 타겟 '저녁 가성비 실속 세트' 출시",
            "tags": ["#매출증대", "#난이도하", "#상품개발"],
            "related_swot": ["S", "O"],
            "final_reason": "현재 저녁 시간대 매장 인근에 가성비를 중시하는 20대 유동인구가 급증하고 있는 점은 매출 성장의 핵심 기회입니다. 이미 확보된 매장의 강점인 가격 경쟁력을 기반으로 청년층의 지갑 사정에 맞춘 전용 세트 메뉴를 구성하면, 별도의 대규모 시설 투자 없이도 신규 고객을 즉각적으로 유입시킬 수 있습니다. 이는 단순히 판매량을 늘리는 것을 넘어, 저녁 시간대 점유율을 선점함으로써 인근 경쟁 업체들과의 체급 차이를 만드는 가장 효율적인 수익 창출 전략이 될 것입니다."
        },
        {
            "id": 4,
            "title": "대학생 서포터즈 '가성비 검증단' 운영",
            "tags": ["#인지도제고", "#난이도상", "#마케팅"],
            "related_swot": ["S", "O"],
            "final_reason": "가장 큰 기회 요인인 주변 20대 유동인구를 잠재 고객에서 충성 고객으로 전환하기 위해서는 매장의 강점인 '가격 우위'를 신뢰도 높은 방식으로 확산시켜야 합니다. 대학생 서포터즈를 통해 실질적인 가격 검증과 바이럴을 유도함으로써, 온라인 신뢰도를 구축하고 장기적인 지역구 맛집으로 자리 잡는 브랜딩 효과를 기대할 수 있습니다. 초기 운영 공수는 발생하지만, 경쟁이 치열한 상권 내에서 독보적인 가성비 이미지를 선점하는 가장 강력한 공격적 전략이 될 것입니다."
        }
    ]

    formatting_example_swot = format_example_for_prompt(example_swot)
    formatting_example_candidates = format_example_for_prompt(example_candidates)
    formatting_example_evaluate = format_example_for_prompt(example_evaluate)
    formatting_example_output = format_example_for_prompt(example_output)
    
    # AI 프롬프트
    return ChatPromptTemplate.from_messages([
        ("system", """
        너는 여러 비즈니스 전략 중 소상공인에게 가장 큰 이익을 줄 수 있는 핵심 솔루션을 엄선하는 수석 전략 컨설턴트다.

        ### 목표
        평가된 후보군 중 가성비(Efficiency)가 뛰어난 **핵심 솔루션(Core Solutions)**을 우선순위에 따라 **2개** 선정하여 리스트 형식으로 반환하라.

        ### 선정 기준
        1. **제 1원칙 (Impact)**: 기대 효과(Impact Score)가 가장 높은 솔루션을 우선한다.
        2. **제 2원칙 (Efficiency)**: 기대 효과 점수가 비슷하다면, 실행 난이도(Effort Score)가 낮은 '가성비 전략'을 선택한다.
        3. **제 3원칙 (Diversity)**: 가급적 단기적인 매출 상승 전략과 장기적인 브랜딩/운영 관리 전략을 적절히 조합하라.
        3. **최종 검증**: 선정된 솔루션이 주어진 SWOT 데이터의 두 요소와 논리적으로 완벽하게 연결되는지 확인하라.
         
        ### final_reason 작성 지침 (분석적 접근)
        사장님이 전략의 타당성을 이성적으로 납득할 수 있도록 다음 규칙을 엄수하라.
        1. **전문적이고 정중한 톤**: 예의는 갖추되, 감성적인 위로보다는 전문가적인 통찰을 전달하라.
        2. **논리적 인과관계**: '강점 활용 - 기회 포착 - 약점 보완' 등 SWOT 분석 결과가 어떻게 수익으로 연결되는지 4~5줄로 상세히 서술하라.
        3. **기대 효과 명시**: 단순한 예측이 아니라 '매출 상승', '객단가 확보', '운영 효율화' 등 구체적인 비즈니스 이득을 강조하라.
        4. **논리적 구조**:
           - 1. 현재 상태 진단: 데이터 기반의 냉정한 현 상황 요약
           - 2. 전략적 근거: 왜 이 솔루션이 지금 가장 효율적인지에 대한 분석 (`reason`과 `evaluate` 활용)
           - 3. 최종 결과: 실행을 통해 얻게 될 정량적/정성적 기대 효과

        ### 선정 및 핵심 규칙
        - 반드시 입력받은 후보군의 **ID를 그대로 유지**하며 최적의 솔루션 2개만 선정한다.
        - 가성비(High Impact, Low Effort)를 최우선으로 하되, 매장의 장기적인 성장 가능성을 고려하라.          
        - 선정되지 않은 나머지 2개의 후보는 결과에서 제외한다.
        """),

        # Few-shot: Human 예시 (SWOT + 평가 완료된 후보군)
        ("human", f"""
        ### 분석 데이터:
        - SWOT 데이터: {formatting_example_swot}
        - 전략 후보군: {formatting_example_candidates}
        - 평가 결과: {formatting_example_evaluate}

        위 데이터를 바탕으로 시스템 지침(선정 기준 및 작성 규칙)에 따라 최적의 솔루션 2개를 최종 선정하고 상세 이유(final_reason)를 작성해줘.
        """),
        
        # Few-shot: AI 응답 예시 (최종 선정 결과)
        ("ai", formatting_example_output),

        # 실제 사용자 요청
        ("human", """
        ### 분석 데이터:
        - SWOT 데이터: {swot_json}
        - 전략 후보군: {candidate_list}
        - 평가 결과: {evaluated_candidates}

        위 데이터를 바탕으로 시스템 지침(선정 기준 및 작성 규칙)에 따라 최적의 솔루션 2개를 최종 선정하고 상세 이유(final_reason)를 작성해줘.
        """),        
    ])