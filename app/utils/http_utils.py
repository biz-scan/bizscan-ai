import json
import httpx
from pydantic import HttpUrl, BaseModel
from typing import Dict, Any, Optional, Union
from fastapi import HTTPException
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

import os
from dotenv import load_dotenv
load_dotenv()
from app.core.logger import logger
from app.utils.client_manager import HttpClientManager
from app.schemas.analysis_schema import SummaryRequest, SummaryResponse

base_url = os.getenv("BASE_URL")
summary_path = "/api/swot/summary"
test_base_url = os.getenv("BASE_URL")
test_summary_path = os.getenv("SUMMARY_PATH")

# 재시도 조건: 네트워크 에러이거나 서버 에러(5xx)일 때만 재시도
def is_retryable_error(exception):
    if isinstance(exception, httpx.HTTPStatusError):
        # 4xx 에러(잘못된 요청 등)는 재시도하지 않고 5xx(서버 장애)만 재시도
        return exception.response.status_code >= 500
    # 타임아웃, 연결 실패 등 네트워크 에러는 재시도
    return isinstance(exception, httpx.RequestError)



async def send_callback(url: HttpUrl, payload: Union[BaseModel, Dict[str, Any]]):
    # 싱글톤 클라이언트 가져오기
    client = HttpClientManager.client
    
    if client is None:
        logger.error("--- HTTP Client가 초기화되지 않았습니다. ---")
        raise RuntimeError("HTTP Client not initialized")

    # 데이터 직렬화
    data = payload.model_dump(mode="json") if isinstance(payload, BaseModel) else payload

    # callback 실패 시 service 로직의 fail_callback 수행
    response = await client.post(
        str(url),
        json=data,
        timeout=60.0
    )
    response.raise_for_status()
    return True
    

@retry(
    stop=stop_after_attempt(3),  # 최대 3번 시도
    wait=wait_exponential(multiplier=1, min=2, max=6),  # 2s, 4s, 6s 형태로 대기 시간 증가
    retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)), # 지정된 에러 발생 시
    before_sleep=lambda retry_state: logger.warning(
        f"재시도 중: {retry_state.attempt_number}회 실패, 다음 시도 대기 중..."
    ),
    reraise=True  # 최종 실패 시 마지막 예외를 호출자에게 다시 던짐
)
async def get_summary_data(
    req: SummaryRequest
) -> SummaryResponse:
    params = req.model_dump(by_alias=True)

    # 싱글톤 클라이언트 가져오기
    client = HttpClientManager.client
    
    if client is None:
        raise HTTPException(status_code=500, detail="HTTP Client가 초기화되지 않았습니다.")
    
    url = base_url + summary_path
    test_url = test_base_url + test_summary_path
    logger.info("현재 url: " + url)
    logger.info("Test URL: " + test_url)

    # 실패 시 @retry로 최대 3회 재시도
    response = await client.get(
        url, 
        params=params, 
    )
    
    # HTTP 상태 코드가 200번대가 아닐 경우 에러 발생
    response.raise_for_status()
    
    # 응답 데이터를 Pydantic 모델로 파싱하여 반환
    return SummaryResponse(**response.json())