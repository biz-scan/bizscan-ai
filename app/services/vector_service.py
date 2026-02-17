import os
import uuid  
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct  
from openai import OpenAI
from dotenv import load_dotenv
from app.schemas.vector_schema import StoreSwotIngestRequest, SimilarityResult

load_dotenv()

class VectorService:
    def __init__(self):
        self.qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
        self.qdrant_port = int(os.getenv("QDRANT_PORT", 6333))
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.collection_name = "bizscan_store_profile"

        # Qdrant 및 OpenAI 클라이언트 초기화
        self.client = QdrantClient(host=self.qdrant_host, port=self.qdrant_port)
        self.openai_client = OpenAI(api_key=self.api_key)

        self._init_collection()

    def _init_collection(self):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,
                    distance=models.Distance.COSINE
                )
            )

    def _get_embedding(self, text: str) -> list:
        text = text.replace("\n", " ")
        response = self.openai_client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    async def ingest_store_swot(self, request: StoreSwotIngestRequest):
        """
        Store의 모든 SWOT 정보를 하나의 텍스트로 합쳐서(Merge)
        단일 벡터로 저장합니다. ID는 store_id를 사용합니다.
        """
        
        # 1. 텍스트 합치기 (Context Merging)
        full_text = f"매장 특징 및 캐치프레이즈: {request.catchphrase}\n\n[SWOT 분석 상세]\n"
        
        # SWOT 아이템들을 순회하며 텍스트에 추가
        for item in request.items:
            full_text += f"- [{item.type}] {item.keyword}: {item.description} (AI 진단: {item.diagnosis})\n"

        # 2. 임베딩 생성
        vector = self._get_embedding(full_text)
        
        # 3. 메타데이터(Payload) 구성
        payload = {
            "store_id": request.store_id,
            "catchphrase": request.catchphrase,
            "category": "STORE_PROFILE", # 구분값 변경
            "full_text": full_text # 원문 전체 저장
        }
        
        # 4. Qdrant 저장 (Upsert)
        points = [
            PointStruct(
                id=request.store_id,  
                vector=vector, 
                payload=payload
            )
        ]
        
        self.client.upsert(collection_name=self.collection_name, points=points)
        return {"status": "success", "message": f"Store {request.store_id} profile ingested."}

    def search_similar(self, store_id: int, query_text: str, top_k: int) -> list[SimilarityResult]:
        """
        유사한 가게를 검색합니다.
        """
        query_vector = self._get_embedding(query_text)

        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            query_filter=models.Filter(
                must_not=[
                    models.FieldCondition(
                        key="store_id",
                        match=models.MatchValue(value=store_id)
                    )
                ]
            )
        ).points

        results = []
        for point in search_result:
            results.append(SimilarityResult(
                storeId=point.payload['store_id'],
                catchphrase=point.payload.get('catchphrase'),
                score=point.score,
                rawText=point.payload.get('full_text', '')[:200] + "..." 
            ))
        return results
    
    def get_store_vector_info(self, store_id: int):
        """
        [디버깅용] 특정 Store ID의 벡터 데이터가 잘 저장되어 있는지 확인
        """
        try:
            # Qdrant에서 ID로 포인트 조회
            points = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[store_id],
                with_payload=True,
                with_vectors=False 
            )
            
            if not points:
                return None
            
            point = points[0]
            return {
                "store_id": point.id,
                "payload": point.payload,
                "is_exists": True
            }
        except Exception as e:
            print(f"Error retrieving store info: {e}")
            return None

vector_service = VectorService()