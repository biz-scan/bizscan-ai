from typing import List
from fastapi import APIRouter

from app.utils.http_utils import test_env

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

@router.get("")
def health_check():
    return "Hello, World!"

@router.get("/test-env",
            summary="로컬 환경과 배포 환경의 .env 파일 테스트")
def test():
    return test_env()
    