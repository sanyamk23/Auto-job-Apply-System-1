from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from agents import agents
from config import PLATFORMS

app = FastAPI(title="AntiSocial API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    platform: str
    topic: str
    audience: str
    tone: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.get("/")
def root():
    return {"message": "AntiSocial API is running"}

@app.get("/platforms")
def get_platforms():
    return {"platforms": list(PLATFORMS.values())}

@app.post("/generate")
def generate_content(request: ContentRequest):
    try:
        if request.platform not in agents:
            raise HTTPException(400, "Invalid platform")
        
        agent = agents[request.platform]
        result = agent.generate_content(request.topic, request.audience, request.tone)
        
        return result
        
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/chat")
def chat_with_agent(request: ChatRequest):
    try:
        # Find which agent to use based on session
        from storage import storage
        session = storage.get_session(request.session_id)
        
        if not session:
            raise HTTPException(404, "Session not found")
        
        agent = agents[session["platform"]]
        result = agent.chat(request.session_id, request.message)
        
        return result
        
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/sessions")
def get_sessions():
    try:
        from storage import storage
        sessions = storage.get_all_sessions()
        
        # Format sessions for UI display
        session_list = []
        for session_id, session_data in sessions.items():
            session_list.append({
                "session_id": session_id,
                "platform": session_data.get("platform", "unknown"),
                "topic": session_data.get("topic", "Untitled"),
                "audience": session_data.get("audience", ""),
                "tone": session_data.get("tone", ""),
                "created_at": session_data.get("created_at", "")
            })
        
        # Sort by most recent first (if we had timestamps)
        return {"sessions": session_list}
        
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    try:
        from storage import storage
        session = storage.get_session(session_id)
        
        if not session:
            raise HTTPException(404, "Session not found")
        
        return session
        
    except Exception as e:
        raise HTTPException(500, str(e))