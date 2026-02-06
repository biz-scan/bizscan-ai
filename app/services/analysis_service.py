# swot service + action_plan service
import re
from pydantic import HttpUrl
from app.core.logger import logger

from app.services.swot_service import create_swot
from app.services.action_plan_service import create_action_plan
from app.schemas.analysis_schema import AnalysisStoreRequest, SummaryRequest, SummaryResponse, StoreInfo
from app.schemas.common_schema import CallbackResponse
from app.utils.http_utils import get_summary_data, send_callback

async def run_analysis_flow(request: AnalysisStoreRequest):
    try:
        keyword = generate_keyword(request.address, request.signature)        

        summary_req = SummaryRequest(
            address=request.address,
            category=request.category,
            storeName=request.name,
            keyword=keyword
        )

        logger.info("--- 0단계: 공공데이터 전처리 시작 ---")
        summary_result: SummaryResponse = await get_summary_data(summary_req)        
        logger.debug(f"데이터 전처리 결과: {summary_result.model_dump_json(indent=4, ensure_ascii=False)}")
        store_info = StoreInfo(**request.model_dump())
        
        # SWOT 시작
        swot_data = await create_swot(store_info=store_info, summary_result=summary_result, swot_callback_url=request.swot_callback_url, request_id=request.request_id, fail_callback_url=request.fail_callback_url)
        # ActionPlan 시작
        await create_action_plan(swot_data=swot_data, action_plan_callback_url=request.action_plan_callback_url, action_detail_callback_url=request.action_detail_callback_url, request_id=request.request_id, fail_callback_url=request.fail_callback_url)

    except Exception as e:
        # 에러 발생 시 처리
        logger.error(f"AI 분석 중 오류 발생: {str(e)}", exc_info=True)
        
        error_payload = CallbackResponse(
            isSuccess=False,
            code="AI_ERROR_500",
            message="AI 분석 중 오류가 발생했습니다.",
            request_id=request.request_id,
            status="FAILED"
        )
        await send_callback(request.fail_callback_url, error_payload)



def generate_keyword(address: str, menu: str) -> str:
    if not address:
        return menu

    # 정규표현식: 동, 읍, 면, 가 단위를 모두 포함 (숫자 조합 및 띄어쓰기 대응)
    # 예: 성수동, 성수1동, 오창읍, 내수면, 을지로3가, 성수동 1가 등
    region_pattern = r'([가-힣0-9]+(?:동|읍|면|가)(?:\s?\d+가|제?\d+동)?)'

    # 1단계: 도로명 주소의 괄호 안 내용 우선 확인 (가장 정확한 행정동 정보)
    bracket_match = re.search(r'\(([^)]+)\)', address)
    if bracket_match:
        content = bracket_match.group(1)
        # 괄호 안에서 '동/읍/면/가' 패턴 찾기 (쉼표로 구분된 경우 대응)
        for part in content.split(','):
            match = re.search(region_pattern, part.strip())
            if match:
                return f"{match.group(1)} {menu}"

    # 2단계: 주소 전체에서 패턴 검색 (지번 주소 스타일)
    main_match = re.search(region_pattern, address)
    if main_match:
        return f"{main_match.group(1)} {menu}"

    # 3단계: '동'이 없는 경우 '구' 단위 추출
    gu_match = re.search(r'([가-힣]+구)', address)
    if gu_match:
        return f"{gu_match.group(1)} {menu}"

    # 4단계: 모든 패턴 실패 시, 앞의 두 단어 조합 (예: 서울 성동구)
    parts = address.split()
    fallback = " ".join(parts[:2]) if len(parts) >= 2 else (parts[0] if parts else "지역미정")
    return f"{fallback} {menu}"



# 임시 데이터
        # swot_data = {
        #     "strengths": {
        #         "type": "S",
        #         "keyword": "직접 로스팅한 고품질 원두",
        #         "description": "품질 대비 낮은 가격대 유지",
        #         "diagnosis": "자체 로스팅을 통해 원가를 절감하면서도 스페셜티급 품질을 유지하고 있습니다. 이는 저가형 커피 프랜차이즈와 고급 개인 카페 사이에서 독보적인 가성비 포지션을 구축할 수 있는 강력한 자산입니다."
        #     },
        #     "weaknesses": {
        #         "type": "W",
        #         "keyword": "협소한 매장 좌석",
        #         "description": "평균 체류 시간 20분 내외",
        #         "diagnosis": "매장 면적이 좁아 피크 타임 시 홀 이용 고객을 놓치는 경우가 많습니다. 특히 단체 고객 수용이 불가능하여 객단가를 높이는 데 한계가 있으며, 이는 회전율에만 의존해야 하는 수익 구조를 만듭니다."
        #     },
        #     "opportunities": {
        #         "type": "O",
        #         "keyword": "인근 직장인 테이크아웃 수요 증가",
        #         "description": "오전 8시~10시 매출 비중 40%",
        #         "diagnosis": "최근 인근 지식산업센터 입주로 인해 출근 시간대 테이크아웃 수요가 폭발적으로 증가하고 있습니다. 이들의 이동 동선에 맞춘 빠른 서빙 프로세스와 모바일 주문 시스템을 도입한다면 매출 극대화가 가능합니다."
        #     },
        #     "threats": {
        #         "type": "T",
        #         "keyword": "대형 프랜차이즈의 공격적 마케팅",
        #         "description": "반경 100m 내 브랜드 카페 3곳 신규 진입",
        #         "diagnosis": "대형 자본을 앞세운 프랜차이즈 카페들이 1+1 행사나 멤버십 혜택으로 고객을 유인하고 있습니다. 단순한 가격 비교보다는 우리 매장만의 '맛'과 '친밀함'을 강조한 로컬 브랜딩이 뒷받침되지 않으면 고객 이탈 우려가 큽니다."
        #     }
        # }