"""
Tasks API routes
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# In-memory storage
tasks_db = {}


@router.get("/")
async def list_tasks(project_id: Optional[str] = None, skip: int = 0, limit: int = 20):
    """List tasks"""
    tasks = list(tasks_db.values())

    if project_id:
        tasks = [t for t in tasks if t["project_id"] == project_id]

    return {
        "success": True,
        "data": tasks[skip : skip + limit],
        "meta": {"total": len(tasks), "skip": skip, "limit": limit},
    }


@router.post("/")
async def create_task(
    project_id: str,
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
):
    """Create a new task"""
    task_id = f"task_{datetime.utcnow().timestamp()}"
    task = {
        "id": task_id,
        "project_id": project_id,
        "title": title,
        "description": description or "",
        "status": "pending",
        "priority": priority,
        "assigned_agent": None,
        "dependencies": [],
        "due_date": None,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    tasks_db[task_id] = task
    return {"success": True, "data": task}


@router.get("/{task_id}")
async def get_task(task_id: str):
    """Get a specific task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "data": tasks_db[task_id]}


@router.put("/{task_id}")
async def update_task(
    task_id: str,
    title: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
):
    """Update a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasks_db[task_id]
    if title:
        task["title"] = title
    if status:
        task["status"] = status
    if priority:
        task["priority"] = priority

    task["updated_at"] = datetime.utcnow().isoformat()
    return {"success": True, "data": task}


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[task_id]
    return {"success": True, "message": "Task deleted"}
