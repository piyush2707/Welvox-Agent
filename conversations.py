"""
Conversation API routes
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket
from typing import List
from datetime import datetime
import json

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


# Models
class MessageInput:
    def __init__(self, content: str, role: str = "user"):
        self.content = content
        self.role = role


class ConversationResponse:
    def __init__(self, id: str, title: str, messages: list, created_at: str):
        self.id = id
        self.title = title
        self.messages = messages
        self.created_at = created_at


# In-memory storage for demo
conversations_db = {}


@router.get("/")
async def list_conversations(skip: int = 0, limit: int = 20):
    """List user's conversations"""
    conversations = list(conversations_db.values())[skip : skip + limit]
    return {
        "success": True,
        "data": conversations,
        "meta": {"total": len(conversations_db), "skip": skip, "limit": limit},
    }


@router.post("/")
async def create_conversation(title: str):
    """Create a new conversation"""
    conv_id = f"conv_{datetime.utcnow().timestamp()}"
    conversation = {
        "id": conv_id,
        "title": title or "New Conversation",
        "messages": [],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    conversations_db[conv_id] = conversation
    return {"success": True, "data": conversation}


@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get a specific conversation"""
    if conversation_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"success": True, "data": conversations_db[conversation_id]}


@router.post("/{conversation_id}/messages")
async def send_message(conversation_id: str, content: str):
    """Send a message to a conversation"""
    if conversation_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Conversation not found")

    message = {
        "id": f"msg_{datetime.utcnow().timestamp()}",
        "role": "user",
        "content": content,
        "created_at": datetime.utcnow().isoformat(),
    }

    conversations_db[conversation_id]["messages"].append(message)

    # Simulate AI response
    ai_response = {
        "id": f"msg_{datetime.utcnow().timestamp()}",
        "role": "assistant",
        "content": f"I received your message: {content[:50]}...",
        "created_at": datetime.utcnow().isoformat(),
    }

    conversations_db[conversation_id]["messages"].append(ai_response)

    return {
        "success": True,
        "data": {
            "userMessage": message,
            "aiResponse": ai_response,
        },
    }


@router.get("/{conversation_id}/messages")
async def get_messages(conversation_id: str, skip: int = 0, limit: int = 50):
    """Get messages from a conversation"""
    if conversation_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = conversations_db[conversation_id]["messages"][skip : skip + limit]
    return {
        "success": True,
        "data": messages,
        "meta": {
            "total": len(conversations_db[conversation_id]["messages"]),
            "skip": skip,
            "limit": limit,
        },
    }


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id not in conversations_db:
        raise HTTPException(status_code=404, detail="Conversation not found")
    del conversations_db[conversation_id]
    return {"success": True, "message": "Conversation deleted"}


# WebSocket endpoint for real-time messaging
@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    """WebSocket endpoint for real-time messaging"""
    if conversation_id not in conversations_db:
        await websocket.close(code=4004, reason="Conversation not found")
        return

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Store message
            message = {
                "id": f"msg_{datetime.utcnow().timestamp()}",
                "role": "user",
                "content": message_data.get("content", ""),
                "created_at": datetime.utcnow().isoformat(),
            }

            conversations_db[conversation_id]["messages"].append(message)

            # Broadcast to all connected clients
            await websocket.send_json(
                {
                    "type": "message",
                    "message": message,
                }
            )

    except Exception as e:
        await websocket.close(code=1000, reason=str(e))
