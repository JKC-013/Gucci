from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
import logging
from config import QDRANT_URL, QDRANT_API_KEY, EMBED_DIM

logger = logging.getLogger("gucci_ai")

class QdrantStorage:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=30)
        self.collection = "gucci_sim_data_v2"
        
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
            )
            logger.info(f"Created collection: {self.collection}")

    def upsert(self, ids, vectors, payloads):
        points = [PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))]
        self.client.upsert(self.collection, points=points)

    def search(self, query_vector, top_k: int = 3):
        results = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            with_payload=True,
            limit=top_k
        ).points
        
        contexts = []
        for r in results:
            payload = getattr(r, "payload", None) or {}
            text = payload.get("text", "")
            if text:
                contexts.append(text)
        return contexts

    def clear_collection(self):
        self.client.delete_collection(self.collection)
