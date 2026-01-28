import json
from langchain_core.prompts import ChatPromptTemplate

# 2. 후보 전략 평가 Chain
def get_evaluation_prompt() -> ChatPromptTemplate:
    # Few-shot Input
    example_swot = {
        "strengths": [{"id": "S1", "keyword": "당일 생산 수제 빵의 품질"}],
        "weaknesses": [{"id": "W1", "keyword": "온라인 홍보 부족"}],
        "opportunities": [{"id": "O1", "keyword": "인근 지하철역 출근길 유동인구 풍부"}],
        "threats": [{"id": "T1", "keyword": "대형 프랜차이즈 빵집 입점 예정"}]
    }
    
    
    example_candidates = [
        {
            "id": 1,
            "title": "출근길 타겟 '수제 모닝 샌드위치' 출시",
            "tags": ["#매출증대", "#난이도하", "#상품개발"],
            "related_swot": ["S1", "O1"],
            "reason": "수제 빵의 품질(S1)과 풍부한 출근길 유동인구(O1)를 결합하여 아침 시간대 구매를 유도하는 SO 전략이다."
        },
        {
            "id": 2,
            "title": "인스타그램 '빵 나오는 시간' 인증 이벤트",
            "tags": ["#인지도제고", "#난이도하", "#마케팅"],
            "related_swot": ["W1", "O1"],
            "reason": "홍보 부족(W1)을 해결하기 위해 유동인구(O1)를 대상으로 SNS 참여를 유도하여 온라인 노출을 극대화하는 WO 전략이다."
        },
        {
            "id": 3,
            "title": "프랜차이즈 대비 '프리미엄 수제 빵' 브랜딩",
            "tags": ["#신규고객", "#난이도중", "#고객관리"],
            "related_swot": ["S1", "T1"],
            "reason": "대형 프랜차이즈(T1)에 맞서 수제 빵의 품질(S1)을 강조하여 장인 정신이 담긴 매장임을 차별화하는 ST 전략이다."
        },
        {
            "id": 4,
            "title": "인근 지역 커뮤니티 타겟 마케팅 강화",
            "tags": ["#바이럴", "#난이도중", "#마케팅"],
            "related_swot": ["W1", "T1"],
            "reason": "부족한 홍보(W1)를 보완하고 경쟁사(T1)의 유입 독점을 막기 위해 지역 맘카페 등에 신뢰 기반 마케팅을 펼치는 WT 전략이다."
        },
        {
            "id": 5,
            "title": "출근 시간대 '사전 예약 및 픽업' 서비스",
            "tags": ["#운영효율", "#난이도중", "#시설개선"],
            "related_swot": ["S1", "O1"],
            "reason": "빵의 품질(S1)을 아는 바쁜 직장인(O1)을 위해 대기 시간을 줄여 편의성을 제공하는 고도화된 SO 전략이다."
        }
    ]
    
    # Few-shot Output
    example_output = [
        {"id": 1, "impactScore": 9, "effortScore": 2, "evaluation": "이미 확보된 품질과 유동인구를 즉시 매출로 연결하며, 메뉴 구성 외 추가 비용이 적어 효율적이다."},
        {"id": 2, "impactScore": 7, "effortScore": 1, "evaluation": "마케팅 비용 없이 고객 참여만으로 온라인 인지도를 빠르게 쌓을 수 있어 실행이 매우 쉽다."},
        {"id": 3, "impactScore": 8, "effortScore": 4, "evaluation": "경쟁사와 차별화되는 장기적 자산이 되지만, 브랜딩을 위한 스토리텔링과 디자인 작업이 수반되어야 한다."},
        {"id": 4, "impactScore": 6, "effortScore": 3, "evaluation": "지역 밀착형 홍보로 확실한 단골을 잡을 수 있으나, 커뮤니티 관리와 신뢰 형성에 시간이 소요된다."},
        {"id": 5, "impactScore": 5, "effortScore": 6, "evaluation": "편의성은 증대되나 예약 관리 시스템 도입과 인력 동선 조정 등 운영상 복잡성이 발생할 수 있다."}
    ]

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
            - 점수가 낮을수록 'Low Effort(쉬움)'이며, 점수가 높을수록 'High Effort(어려움)'이다.

        ### 핵심 규칙
        - `evaluation`은 왜 해당 점수를 부여했는지 전략적 근거를 2문장 내외로 서술하라.
        - SWOT 분석 결과와 전략의 연관성을 고려하여 평가의 객관성을 유지하라.
        """),

        # Few-shot: Human 예시 (SWOT + 후보군)
        ("human", f"""
        ### SWOT 데이터:
        {json.dumps(example_swot, ensure_ascii=False)}

        ### 전략 후보군:
        {json.dumps(example_candidates, ensure_ascii=False)}
        """),
        
        # Few-shot: AI 응답 예시 (평가 결과)
        ("ai", json.dumps(example_output, ensure_ascii=False)),

        # 실제 사용자 요청
        ("human", """
        ### SWOT 데이터:
        {swot_json}

        ### 전략 후보군:
        {candidate_list}

        위 후보군들에 대해 'Impact'와 'Effort' 점수를 산출하고 그 이유를 분석해줘.
        """),
    ])