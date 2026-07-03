"""
Files API routes
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from datetime import datetime
from typing import Optional
import os

router = APIRouter(prefix="/api/files", tags=["files"])

# In-memory file registry
files_db = {}
STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage")


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file"""
    file_id = f"file_{datetime.utcnow().timestamp()}"

    # Create storage directory if it doesn't exist
    os.makedirs(STORAGE_PATH, exist_ok=True)

    # Save file
    file_path = os.path.join(STORAGE_PATH, f"{file_id}_{file.filename}")

    try:
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)

        file_ref = {
            "id": file_id,
            "name": file.filename,
            "mime_type": file.content_type,
            "size": len(contents),
            "path": file_path,
            "uploaded_at": datetime.utcnow().isoformat(),
        }

        files_db[file_id] = file_ref
        return {"success": True, "data": file_ref}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@router.get("/")
async def list_files(skip: int = 0, limit: int = 20):
    """List uploaded files"""
    files = list(files_db.values())[skip : skip + limit]
    return {
        "success": True,
        "data": files,
        "meta": {"total": len(files_db), "skip": skip, "limit": limit},
    }


@router.get("/{file_id}")
async def get_file(file_id: str):
    """Get file information"""
    if file_id not in files_db:
        raise HTTPException(status_code=404, detail="File not found")
    return {"success": True, "data": files_db[file_id]}


@router.post("/{file_id}/analyze")
async def analyze_file(file_id: str):
    """Analyze a file content"""
    if file_id not in files_db:
        raise HTTPException(status_code=404, detail="File not found")

    file_ref = files_db[file_id]

    # Simulate file analysis
    analysis = {
        "file_id": file_id,
        "file_name": file_ref["name"],
        "file_type": file_ref["mime_type"],
        "analysis": {
            "pages": 10,  # Would be actual count
            "words": 5000,  # Would be actual count
            "language": "en",
            "summary": "File successfully analyzed",
        },
    }

    return {"success": True, "data": analysis}


@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """Delete a file"""
    if file_id not in files_db:
        raise HTTPException(status_code=404, detail="File not found")

    file_ref = files_db[file_id]

    # Delete file from storage
    try:
        if os.path.exists(file_ref["path"]):
            os.remove(file_ref["path"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

    del files_db[file_id]
    return {"success": True, "message": "File deleted"}
