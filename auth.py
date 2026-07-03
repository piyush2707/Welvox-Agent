"""
Authentication API routes
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["auth"])


class TokenResponse:
    def __init__(self, access_token: str, token_type: str = "bearer"):
        self.access_token = access_token
        self.token_type = token_type


# In-memory user store for demo
users_db = {}
tokens_db = {}


@router.post("/signup")
async def signup(email: str, password: str, name: str):
    """Create a new user account"""
    if email in users_db:
        raise HTTPException(status_code=409, detail="Email already exists")

    user_id = f"user_{datetime.utcnow().timestamp()}"
    user = {
        "id": user_id,
        "email": email,
        "name": name,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }

    users_db[email] = user
    token = f"token_{user_id}"
    tokens_db[token] = user_id

    return {
        "success": True,
        "data": {
            "user": user,
            "token": token,
            "token_type": "bearer",
        },
    }


@router.post("/login")
async def login(email: str, password: str):
    """Login user"""
    if email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = users_db[email]
    token = f"token_{user['id']}"
    tokens_db[token] = user["id"]

    return {
        "success": True,
        "data": {
            "user": user,
            "token": token,
            "token_type": "bearer",
        },
    }


@router.post("/logout")
async def logout(token: str):
    """Logout user"""
    if token in tokens_db:
        del tokens_db[token]

    return {"success": True, "message": "Logged out successfully"}


@router.get("/verify")
async def verify_token(token: str):
    """Verify authentication token"""
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = tokens_db[token]
    return {"success": True, "data": {"userId": user_id, "valid": True}}


@router.post("/refresh")
async def refresh_token(token: str):
    """Refresh authentication token"""
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = tokens_db[token]
    new_token = f"token_{user_id}_{datetime.utcnow().timestamp()}"
    tokens_db[new_token] = user_id
    del tokens_db[token]

    return {
        "success": True,
        "data": {
            "token": new_token,
            "token_type": "bearer",
        },
    }
