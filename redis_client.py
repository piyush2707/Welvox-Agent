import json
import logging
from typing import Any, Optional

import redis.asyncio as redis

from core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Async Redis client wrapper"""
    
    def __init__(self):
        self.client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.client = await redis.from_url(settings.REDIS_URL, decode_responses=True)
            await self.client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def close(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()
            logger.info("Redis connection closed")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = await self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = settings.REDIS_CACHE_TIMEOUT
    ):
        """Set value in cache"""
        try:
            await self.client.setex(
                key,
                ttl,
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
    
    async def delete(self, key: str):
        """Delete key from cache"""
        try:
            await self.client.delete(key)
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            return await self.client.exists(key)
        except Exception as e:
            logger.error(f"Error checking key {key}: {e}")
            return False
    
    async def lpush(self, key: str, *values: Any):
        """Push to queue (left side)"""
        try:
            await self.client.lpush(key, *[json.dumps(v) for v in values])
        except Exception as e:
            logger.error(f"Error pushing to queue {key}: {e}")
    
    async def rpop(self, key: str) -> Optional[Any]:
        """Pop from queue (right side)"""
        try:
            value = await self.client.rpop(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error popping from queue {key}: {e}")
            return None
    
    async def llen(self, key: str) -> int:
        """Get queue length"""
        try:
            return await self.client.llen(key)
        except Exception as e:
            logger.error(f"Error getting queue length {key}: {e}")
            return 0


# Global instance
redis_client = RedisClient()
