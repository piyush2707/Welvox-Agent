import logging
from typing import List, Optional

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from core.config import settings

logger = logging.getLogger(__name__)


class VectorDB:
    """Qdrant vector database client"""
    
    def __init__(self):
        self.client: Optional[AsyncQdrantClient] = None
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self.vector_size = 1536  # OpenAI embedding size
    
    async def initialize(self):
        """Initialize vector database"""
        try:
            self.client = AsyncQdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None
            )
            
            # Create collection if it doesn't exist
            try:
                await self.client.get_collection(self.collection_name)
                logger.info(f"Collection {self.collection_name} already exists")
            except Exception:
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Collection {self.collection_name} created")
            
            logger.info("Vector database initialized")
        except Exception as e:
            logger.error(f"Failed to initialize vector database: {e}")
            raise
    
    async def store(
        self,
        document_id: str,
        text: str,
        embedding: List[float],
        metadata: dict = None
    ) -> bool:
        """Store document with embedding"""
        try:
            point = PointStruct(
                id=hash(document_id) % (10 ** 8),  # Convert string ID to int
                vector=embedding,
                payload={
                    "document_id": document_id,
                    "text": text,
                    **(metadata or {})
                }
            )
            
            await self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            return True
        except Exception as e:
            logger.error(f"Error storing document: {e}")
            return False
    
    async def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        score_threshold: float = 0.5
    ) -> List[dict]:
        """Search for similar documents"""
        try:
            results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold
            )
            
            return [
                {
                    "document_id": result.payload.get("document_id"),
                    "text": result.payload.get("text"),
                    "score": result.score,
                    "metadata": {
                        k: v for k, v in result.payload.items()
                        if k not in ["document_id", "text"]
                    }
                }
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []
    
    async def delete(self, document_id: str) -> bool:
        """Delete document by ID"""
        try:
            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=[hash(document_id) % (10 ** 8)]
            )
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False


# Global instance
vector_db = VectorDB()
