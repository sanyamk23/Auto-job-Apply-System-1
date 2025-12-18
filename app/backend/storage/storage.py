import json
import os
from datetime import datetime
from pathlib import Path

class SimpleStorage:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.sessions = {}
        self.conversations = {}
    
    def save_session(self, session_id, data):
        """Save session data"""
        self.sessions[session_id] = {
            **data,
            "updated_at": datetime.now().isoformat()
        }
        
        # Also save to file for persistence
        session_file = self.data_dir / f"{session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(self.sessions[session_id], f, indent=2)
    
    def get_session(self, session_id):
        """Get session data"""
        if session_id in self.sessions:
            return self.sessions[session_id]
        
        # Try loading from file
        session_file = self.data_dir / f"{session_id}.json"
        if session_file.exists():
            with open(session_file, 'r') as f:
                data = json.load(f)
                self.sessions[session_id] = data
                return data
        
        return None
    
    def save_conversation(self, session_id, messages):
        """Save conversation messages"""
        self.conversations[session_id] = messages
    
    def get_conversation(self, session_id):
        """Get conversation messages"""
        return self.conversations.get(session_id, [])
    
    def get_all_sessions(self):
        """Get all sessions"""
        # Load all session files from disk
        all_sessions = {}
        
        for session_file in self.data_dir.glob("*.json"):
            session_id = session_file.stem
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    all_sessions[session_id] = data
            except (json.JSONDecodeError, FileNotFoundError):
                continue
        
        # Merge with in-memory sessions
        all_sessions.update(self.sessions)
        
        return all_sessions

# Global storage instance
storage = SimpleStorage()