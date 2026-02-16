from fastapi import APIRouter, Query
from app.schemas.vector_schema import StoreSwotIngestRequest, SimilarityResponse
from app.services.vector_service import vector_service

router = APIRouter(prefix="/api/vector", tags=["Vector Search"])

@router.post("/ingest", status_code=201)
async def ingest_vector_data(request: StoreSwotIngestRequest):
    """
    SWOT 분석 결과를 벡터 DB(Qdrant)에 저장합니다.
    관리자가 수동으로 데이터를 넣을 때 사용합니다.
    """
    await vector_service.ingest_store_swot(request)
    return {"isSuccess": True, "message": "데이터가 성공적으로 저장되었습니다."}

@router.get("/recommend", response_model=SimilarityResponse)
async def recommend_similar_stores(
    storeId: int = Query(..., description="현재 분석 중인 가게 ID (결과에서 제외됨)"), 
    queryText: str = Query(..., description="유사도를 측정할 기준 문구 (예: '분위기 좋은 카페')"),
    topK: int = Query(4, description="가져올 유사 가게 개수")
):
    """
    Qdrant DB에서 현재 가게와 가장 유사한 특징을 가진 다른 가게들을 추천합니다.
    """
    results = vector_service.search_similar(storeId, queryText, topK)
    return {"results": results}