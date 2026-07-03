from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class AgentRequest(BaseModel):
    message: str
    project_id: Optional[str] = None
    context: Optional[dict] = None


class AgentResponse(BaseModel):
    agent_id: str
    message: str
    status: str
    skills_used: List[str]
    tools_used: List[str]


class Agent(BaseModel):
    id: str
    name: str
    description: str
    status: str
    skills: List[str]


@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """Send message to agent and get response"""
    # This would integrate with LangGraph orchestration
    return {
        "agent_id": "default_agent",
        "message": f"Processing: {request.message}",
        "status": "processing",
        "skills_used": [],
        "tools_used": []
    }


@router.post("/chat/stream")
async def chat_with_agent_stream(request: AgentRequest):
    """Stream responses from agent"""
    # This would return a streaming response
    pass


@router.get("/agents", response_model=List[Agent])
async def list_agents():
    """List all available agents"""
    return []


@router.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str):
    """Get agent details"""
    raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/agents")
async def create_agent(name: str, description: str, skills: List[str] = []):
    """Create new agent"""
    return {"agent_id": "new_agent"}
