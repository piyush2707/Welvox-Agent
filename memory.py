"""
Memory API routes - Retrieval Augmented Generation
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional, List

router = APIRouter(prefix="/api/memory", tags=["memory"])

# In-memory storage
memory_db = {}


@router.get("/")
async def list_memories(memory_type: Optional[str] = None, skip: int = 0, limit: int = 20):
    """List memories"""
    memories = list(memory_db.values())

    if memory_type:
        memories = [m for m in memories if m["type"] == memory_type]

    return {
        "success": True,
        "data": memories[skip : skip + limit],
        "meta": {"total": len(memories), "skip": skip, "limit": limit},
    }


@router.post("/")
async def store_memory(
    content: str,
    memory_type: str = "short_term",
    tags: Optional[List[str]] = None,
):
    """Store a memory"""
    memory_id = f"mem_{datetime.utcnow().timestamp()}"
    memory = {
        "id": memory_id,
        "type": memory_type,
        "content": content,
        "embedding": None,  # Would be computed by embedding service
        "metadata": {
            "source": "user",
            "importance": 0.5,
            "tags": tags or [],
            "related_ids": [],
        },
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    memory_db[memory_id] = memory
    return {"success": True, "data": memory}


@router.get("/{memory_id}")
async def get_memory(memory_id: str):
    """Get a specific memory"""
    if memory_id not in memory_db:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"success": True, "data": memory_db[memory_id]}


@router.post("/search")
async def search_memories(query: str, limit: int = 10):
    """Search memories semantically (would use vector similarity in production)"""
    memories = list(memory_db.values())

    # Simple keyword search for demo
    results = [
        m
        for m in memories
        if query.lower() in m["content"].lower()
    ]

    return {
        "success": True,
        "data": results[:limit],
        "meta": {"total": len(results), "limit": limit},
    }


@router.delete("/{memory_id}")
async def delete_memory(memory_id: str):
    """Delete a memory"""
    if memory_id not in memory_db:
        raise HTTPException(status_code=404, detail="Memory not found")
    del memory_db[memory_id]
    return {"success": True, "message": "Memory deleted"}
