import json
from langchain_core.prompts import ChatPromptTemplate

from app.utils.prompt_formatting import format_example_for_prompt

# 1. 후보 전략 선정 Chain
def get_candidate_prompt(quadrant_type: str) -> ChatPromptTemplate:
    descriptions = {
        "SO": "강점(S)을 활용해 기회(O)를 적극적으로 포착하는 전략",
        "ST": "강점(S)을 활용해 외부의 위협(T)을 효과적으로 회피하거나 극복하는 전략",
        "WO": "내부의 약점(W)을 보완하여 외부의 기회(O)를 내 것으로 만드는 전략",
        "WT": "내부의 약점(W)을 보완하고 외부의 위협(T)으로부터 생존하기 위한 방어 전략"
    }
    current_guide = descriptions.get(quadrant_type, "교차 분석 전략")
    # Few-shot Input
    example_input = {
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
        },
        "previous_strategies": [
            "인근 대학교 제휴 할인 이벤트",
            "네이버 플레이스 지역 광고 집행"
        ]

    }

    # Few-shot Output
    example_output = [
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

    formatting_example_input = format_example_for_prompt(example_input)
    formatting_example_output = format_example_for_prompt(example_output)
    
    # AI 프롬프트
    return ChatPromptTemplate.from_messages([
        ("system", """
        너는 주어진 SWOT 분석 결과 중 특정 조합({quadrant_type})에 집중하여, 소상공인을 위한 구체적이고 실행 가능한 비즈니스 전략을 제안하는 최고의 데이터 기반 전략 컨설턴트다.

        ### 목표
        입력된 두 가지 SWOT 요소({quadrant_type})를 결합하여, 사장님이 즉시 실행할 수 있는 후보 솔루션을 4개 생성하라. 
         
        ### 전략 도출 원칙
        - **{quadrant_type} 전략**: {current_guide}
        - 반드시 입력된 **내부 요인({quadrant_type[0]})**과 **외부 요인({quadrant_type[1]})**의 접점을 찾아 교차 분석하라.
        - 각 요소의 `keyword`뿐만 아니라 **`diagnosis`에 담긴 맥락을 깊이 있게 반영**하여 전략을 도출하라.
        - 현재 집중해야 할 조합은 **{quadrant_type}**이다. 분석 과정에서 다른 요소(예: {quadrant_type}가 아닌 요소)가 섞이지 않도록 엄격히 제한하라.
        
         
        ### 중복 방지 규칙
        - `previous_strategies` 리스트는 이전 루프에서 이미 채택된 전략들의 제목이다.
        - **이 리스트에 포함된 전략과 유사하거나 중복되는 아이디어는 절대 생성하지 마라.**
        - 이미 마케팅 전략이 나왔다면 이번에는 상품 개발이나 운영 효율화 측면으로 접근하는 등, 이전 전략들과 차별화된 새로운 시각을 제시하라.

        ### 핵심 규칙        
        1. **구체성**: `title`은 사용자가 즉시 이해할 수 있도록 구체적인 액션을 담아 30자 이내로 작성하라.
        2. **구조화된 태그**: `tags`는 '#목표', '#난이도', '#카테고리' 순서로 반드시 3개를 포함하라.
            - #목표 예시: #매출증대, #신규고객, #객단가UP, #인지도제고
            - #난이도 예시: #난이도하, #난이도중, #난이도상
            - #카테고리 예시: #마케팅, #운영, #고객관리, #상품개발, #시설개선
        3. **근거 제시**: `related_swot`에는 ["{quadrant_type[0]}", "{quadrant_type[1]}"]을 배열로 포함하라.
        4. **생성 이유 명시**: `reason` 필드에 해당 조합이 왜 이 전략으로 연결되는지, 그리고 이 전략이 어떤 기대 효과를 갖는지 2문장 내외로 친절하게 설명하라.
        5. **ID 생성**: Id는 1부터 시작하여 생성되는 후보군의 순서에 따라 **1씩 증가하는 정수(Integer)**로 부여하라. (예: 1, 2, 3...)        
        """),

        # Few-shot: Human 예시
        ("human", f"### 입력 데이터:\n{formatting_example_input}"),
        
        # Few-shot: AI 응답 예시
        ("ai", formatting_example_output),

        # 실제 요청
        ("human", """
        ### 입력 데이터:
        - 분석 대상 조합: {quadrant_type}
        -- 요소 1({quadrant_type[0]}): {{factor_1}}
        - 요소 2({quadrant_type[1]}): {{factor_2}}
        - 이미 선정된 전략: {{previous_strategies}}

        이제 위 형식에 맞춰 **{quadrant_type}** 조합에 특화된, 중복되지 않는 새로운 후보군 4개를 생성해줘.
        """),
    ])