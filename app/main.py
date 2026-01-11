from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from app.core.database import engine, Base
from app.routers import health_router
from app.schemas.common_schema import CommonResponse

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="Bizscan AI API",
    description="Bizscan AI API 입니다.",
    version="0.1.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(health_router.router)

# / -> /docs 리다이렉트
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# HTTP 예외 처리 (400, 401, 404 등)
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    response_body = CommonResponse(
        isSuccess=False,
        code=f"COMMON{exc.status_code}",
        message=exc.detail,
        result=None
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_body.model_dump()
    )

# 전역 예외 처리 (서버 내부 로직 에러)
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    response_body = CommonResponse(
        isSuccess=False,
        code="COMMON500",
        message=f"서버 내부 오류: {str(exc)}",
        result=None
    )
    
    return JSONResponse(
        status_code=500,
        content=response_body.model_dump()
    )
