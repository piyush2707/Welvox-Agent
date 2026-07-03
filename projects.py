"""
Projects API routes
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/projects", tags=["projects"])

# In-memory storage
projects_db = {}


@router.get("/")
async def list_projects(skip: int = 0, limit: int = 20):
    """List user's projects"""
    projects = list(projects_db.values())[skip : skip + limit]
    return {
        "success": True,
        "data": projects,
        "meta": {"total": len(projects_db), "skip": skip, "limit": limit},
    }


@router.post("/")
async def create_project(name: str, description: Optional[str] = None):
    """Create a new project"""
    project_id = f"proj_{datetime.utcnow().timestamp()}"
    project = {
        "id": project_id,
        "name": name,
        "description": description or "",
        "status": "planning",
        "tasks": [],
        "artifacts": [],
        "memory": [],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    projects_db[project_id] = project
    return {"success": True, "data": project}


@router.get("/{project_id}")
async def get_project(project_id: str):
    """Get a specific project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"success": True, "data": projects_db[project_id]}


@router.put("/{project_id}")
async def update_project(project_id: str, name: Optional[str] = None, status: Optional[str] = None):
    """Update a project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")

    if name:
        projects_db[project_id]["name"] = name
    if status:
        projects_db[project_id]["status"] = status

    projects_db[project_id]["updated_at"] = datetime.utcnow().isoformat()
    return {"success": True, "data": projects_db[project_id]}


@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """Delete a project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    del projects_db[project_id]
    return {"success": True, "message": "Project deleted"}
