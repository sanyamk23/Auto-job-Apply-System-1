from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.backend.services.agents import agents
from app.backend.core.config import PLATFORMS
from app.backend.storage.storage import storage

router = APIRouter()

# ---------- Request Models ----------

class ContentRequest(BaseModel):
    platform: str
    topic: str
    audience: str
    tone: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

# ---------- Routes ----------

@router.get("/")
def health_check():
    return {"message": "AntiSocial API is running"}

@router.get("/platforms")
def get_platforms():
    return {"platforms": list(PLATFORMS.values())}

@router.post("/generate")
def generate_content(request: ContentRequest):
    if request.platform not in agents:
        raise HTTPException(status_code=400, detail="Invalid platform")

    agent = agents[request.platform]
    return agent.generate_content(
        request.topic,
        request.audience,
        request.tone
    )

@router.post("/chat")
def chat_with_agent(request: ChatRequest):
    session = storage.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    agent = agents[session["platform"]]
    return agent.chat(request.session_id, request.message)

@router.get("/sessions")
def get_sessions():
    sessions = storage.get_all_sessions()

    session_list = [
        {
            "session_id": session_id,
            "platform": data.get("platform", "unknown"),
            "topic": data.get("topic", "Untitled"),
            "audience": data.get("audience", ""),
            "tone": data.get("tone", ""),
            "created_at": data.get("created_at", "")
        }
        for session_id, data in sessions.items()
    ]

    return {"sessions": session_list}

@router.get("/sessions/{session_id}")
def get_session(session_id: str):
    session = storage.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
