import httpx
from pydantic import HttpUrl
from typing import Dict, Any, Optional
from fastapi import HTTPException

import os
from dotenv import load_dotenv
load_dotenv()

from app.utils.client_manager import HttpClientManager
from app.schemas.analysis_schema import SummaryRequest, SummaryResponse

base_url = os.getenv("BASE_URL_LOCAL")
summary_path = os.getenv("SUMMARY_PATH")

async def send_callback(url: HttpUrl, payload: Dict[str, Any]):
    # 싱글톤 클라이언트 가져오기
    client = HttpClientManager.client
    
    if client is None:
        print("--- HTTP Client가 초기화되지 않았습니다. ---")
        return False

    try:
        response = await client.post(
            str(url),
            json=payload,
            timeout=10.0
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"--- 콜백 전송 최종 실패: {str(e)} ---")
        return False
    
async def get_summary_data(
    req: SummaryRequest
) -> SummaryResponse:
    params = req.model_dump(by_alias=True)

    # 싱글톤 클라이언트 가져오기
    client = HttpClientManager.client
    
    if client is None:
        raise HTTPException(status_code=500, detail="HTTP Client가 초기화되지 않았습니다.")
    
    url = base_url + summary_path
    print("url: " + url)

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