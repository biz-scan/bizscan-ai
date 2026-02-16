import os
import uuid  # 추가
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct  # 추가
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
                    size=1536, # OpenAI text-embedding-3-small 차원
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
        points = []
        for item in request.items:
            vector = self._get_embedding(item.rawText) 
            
            payload = {
                "store_id": request.store_id,
                "catchphrase": request.catchphrase,
                "category": "SWOT_ANALYSIS",
                "title": item.type,
                "keyword": item.keyword,
                "description": item.description,
                "diagnosis": item.diagnosis,
                "raw_text": item.rawText
            }
            
            points.append(PointStruct(
                id=str(uuid.uuid4()), 
                vector=vector, 
                payload=payload
            ))
        
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search_similar(self, store_id: int, query_text: str, top_k: int) -> list[SimilarityResult]:
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
                rawText=point.payload.get('raw_text', '')[:100] + "..."
            ))
        return results

vector_service = VectorService()