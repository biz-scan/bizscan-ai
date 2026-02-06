import json
from typing import Dict, Any
from pydantic import HttpUrl

from app.core.logger import logger
from app.schemas.common_schema import CallbackResponse
from app.schemas.swot_schema import SWOTResponse
from app.schemas.catchphrase_schema import CatchphraseResponse
from app.schemas.analysis_schema import SWOTCallbackResponse, SummaryResponse, StoreInfo
from app.core.chains import swot_chain, catchphrase_chain
from app.utils.http_utils import send_callback

async def create_swot(store_info: StoreInfo, summary_result: SummaryResponse, swot_callback_url: HttpUrl, fail_callback_url: HttpUrl, request_id: str):
    """
    SWOT 분석 및 캐치프레이즈 생성을 수행하고 결과를 콜백으로 전송합니다.
    """
    
    try:
        # 1. 시작 콜백 전송 (SWOT_PROCESSING)
        logger.info(f"--- [Request ID: {request_id}] SWOT 분석 시작 콜백 전송 ---")
        start_payload = CallbackResponse(
            request_id=request_id,
            status="SWOT_PROCESSING",
            result=None
        )
        await send_callback(swot_callback_url, start_payload)

        # Chain 입력 데이터 준비 (JSON 직렬화)
        # store_info와 summary_result를 결합하여 context 생성
        input_data = {
               "store_info": store_info.model_dump(mode="json"), 
               "market_data": summary_result.model_dump(mode="json") # summary_data에서 market_data로 변경
          }

        # 2. SWOT 분석 실행
        logger.info("--- 1단계: SWOT 분석 체인 실행 ---")
        # 제공된 코드 스니펫의 타입을 참고하여 호출
        swot_res: SWOTResponse = await swot_chain.ainvoke(input_data)
        logger.debug(f"SWOT 결과: {swot_res.model_dump_json(indent=4, ensure_ascii=False)}")

        # 3. 캐치프레이즈 생성 실행
        logger.info("--- 2단계: 캐치프레이즈 생성 체인 실행 ---")
        catchphrase_res: CatchphraseResponse = await catchphrase_chain.ainvoke(input_data)
        logger.debug(f"Catchphrase 결과: {catchphrase_res.model_dump_json(indent=4, ensure_ascii=False)}")

        # 4. 종료 콜백 전송 (ACTION_PLAN_PROCESSING)
        logger.info("--- SWOT 분석 완료 및 결과 콜백 전송 ---")
        final_payload = CallbackResponse(
            request_id=request_id,
            status="ACTION_PLAN_PROCESSING",
            result=SWOTCallbackResponse(
                catchphrase=catchphrase_res,
                swot=swot_res
            )
        )
        await send_callback(swot_callback_url, final_payload)
        logger.info("SWOT 및 캐치프레이즈 콜백 전송 성공")

    except Exception as e:
        # 에러 발생 시 처리
        logger.error(f"SWOT 분석 중 오류 발생: {str(e)}", exc_info=True)
        
        error_payload = CallbackResponse(
            isSuccess=False,
            code="AI_ERROR_500",
            message="SWOT 분석 중 오류가 발생했습니다.",
            request_id=request_id,
            status="FAILED"
        )
        await send_callback(fail_callback_url, error_payload)

    return swot_res