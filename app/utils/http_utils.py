import json
import httpx
from pydantic import HttpUrl, BaseModel
from typing import Dict, Any, Optional, Union
from fastapi import HTTPException

import os
from dotenv import load_dotenv
load_dotenv()
from app.core.logger import logger
from app.utils.client_manager import HttpClientManager
from app.schemas.analysis_schema import SummaryRequest, SummaryResponse

base_url = "http://localhost:8080"
summary_path = "/api/swot/summary"
test_base_url = os.getenv("BASE_URL")
test_summary_path = os.getenv("SUMMARY_PATH")


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

    try:
        response = await client.get(
            url, 
            params=params, 
        )
        
        # HTTP 상태 코드가 200번대가 아닐 경우 에러 발생
        response.raise_for_status()
        
        # 응답 데이터를 Pydantic 모델로 파싱하여 반환
        return SummaryResponse(**response.json())

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"External API Error: {e.response.text}"
        )
    except httpx.RequestError as e:
        # 네트워크 연결 문제 처리
        raise HTTPException(
            status_code=503,
            detail=f"외부 API 서버 연결 실패: {str(e)}"
        )