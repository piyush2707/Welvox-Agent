from fastapi import APIRouter
from datetime import datetime

from core.database import engine
from core.redis_client import redis_client
from core.vector_db import vector_db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with service status"""
    services = {}
    
    # Check database
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        services["database"] = "healthy"
    except Exception as e:
        services["database"] = f"unhealthy: {str(e)}"
    
    # Check Redis
    try:
        if redis_client.client:
            await redis_client.client.ping()
        services["redis"] = "healthy"
    except Exception as e:
        services["redis"] = f"unhealthy: {str(e)}"
    
    # Check Vector DB
    try:
        if vector_db.client:
            await vector_db.client.get_collection(vector_db.collection_name)
        services["vector_db"] = "healthy"
    except Exception as e:
        services["vector_db"] = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if all("healthy" in v for v in services.values()) else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "services": services
    }
