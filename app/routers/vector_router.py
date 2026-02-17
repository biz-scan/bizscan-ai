from fastapi import APIRouter, Query
from app.schemas.vector_schema import StoreSwotIngestRequest, SimilarityResponse
from app.services.vector_service import vector_service

router = APIRouter(prefix="/api/vector", tags=["Vector Search"])

# 1. 데이터 적재 (Ingest)
@router.post("/ingest", status_code=201)
async def ingest_vector_data(request: StoreSwotIngestRequest):
    """
    [POST] SWOT 분석 결과를 벡터 DB(Qdrant)에 저장합니다.
    Spring Boot에서 마이그레이션하거나, 분석이 완료되었을 때 호출됩니다.
    """
    result = await vector_service.ingest_store_swot(request)
    
    return {
        "isSuccess": True, 
        "message": "데이터가 성공적으로 벡터 DB에 적재되었습니다.",
        "detail": result
    }

@router.get("/check/{store_id}")
def check_vector_data(store_id: int):
    """
    [GET] 특정 가게의 데이터가 Vector DB에 있는지 확인합니다.
    """
    result = vector_service.get_store_vector_info(store_id)
    if result:
        return {"status": "found", "data": result}
    else:
        return {"status": "not_found", "message": f"Store {store_id} data not found in Vector DB"}

# 2. 유사 매장 추천 (Recommend)
@router.get("/recommend", response_model=SimilarityResponse)
def recommend_similar_stores(
    storeId: int = Query(..., description="현재 분석 중인 가게 ID (결과에서 제외됨)"), 
    queryText: str = Query(..., description="유사도를 측정할 기준 문구 (예: '분위기 좋은 카페')"),
    topK: int = Query(4, description="가져올 유사 가게 개수")
):
    """
    [GET] Qdrant DB에서 현재 가게와 가장 유사한 특징을 가진 다른 가게들을 추천합니다.
    """
    results = vector_service.search_similar(storeId, queryText, topK)
    
    return {"results": results}