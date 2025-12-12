#!/usr/bin/env python3
import subprocess
import sys
import time
import os
from dotenv import load_dotenv

def check_env():
    # Load .env file
    load_dotenv()
    
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("❌ GROQ_API_KEY not found")
        print("Add it to .env file or export GROQ_API_KEY=your_key")
        return False
    
    print("✅ Environment OK")
    print(f"✅ Groq API key found: {groq_key[:10]}...")
    return True

def main():
    print("🧠 AntiSocial - Simple AI Content Platform")
    print("=" * 40)
    
    if not check_env():
        sys.exit(1)
    
    try:
        print("🚀 Starting backend...")
        backend = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "api:app", "--reload", "--port", "8000"
        ])
        
        time.sleep(2)
        
        print("🎨 Starting frontend...")
        frontend = subprocess.Popen([
            sys.executable, "-m", "streamlit", 
            "run", "frontend.py", "--server.port", "8501"
        ])
        
        print("\n🎉 Running!")
        print("Frontend: http://localhost:8501")
        print("API: http://localhost:8000")
        print("\nPress Ctrl+C to stop")
        
        try:
            backend.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
            backend.terminate()
            frontend.terminate()
            print("✅ Stopped")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()