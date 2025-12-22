import streamlit as st
import requests

st.set_page_config(page_title="AntiSocial", page_icon="🧠", layout="wide")

API_URL = "http://localhost:8000"

# Session state
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "content" not in st.session_state:
    st.session_state.content = None

def call_api(endpoint, method="GET", data=None):
    try:
        if method == "POST":
            response = requests.post(f"{API_URL}{endpoint}", json=data)
        else:
            response = requests.get(f"{API_URL}{endpoint}")
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
    except:
        st.error("Cannot connect to backend")
    return None

def display_content(content):
    st.subheader("Trending Angles")
    for i, angle in enumerate(content["trending_angles"], 1):
        # Handle both string and object formats
        if isinstance(angle, dict):
            if "angle" in angle:
                st.write(f"{i}. {angle['angle']}")
                if "image" in angle:
                    st.caption(f"💡 {angle['image']}")
            else:
                st.write(f"{i}. {str(angle)}")
        else:
            st.write(f"{i}. {angle}")
    
    st.subheader("Hashtags")
    # Handle both list and string formats
    if isinstance(content["hashtags"], list):
        st.code(" ".join(content["hashtags"]))
    else:
        st.code(str(content["hashtags"]))
    
    st.subheader("Post Blueprints")
    for i, bp in enumerate(content["post_blueprints"], 1):
        with st.expander(f"Blueprint {i}"):
            # Handle different blueprint formats
            if isinstance(bp, dict):
                if "hook" in bp:
                    st.write(f"**Hook:** {bp['hook']}")
                if "outline" in bp and isinstance(bp["outline"], list):
                    st.write("**Outline:**")
                    for point in bp["outline"]:
                        st.write(f"• {point}")
                elif "outline" in bp:
                    st.write(f"**Outline:** {bp['outline']}")
                if "cta" in bp:
                    st.write(f"**CTA:** {bp['cta']}")
            else:
                st.write(str(bp))

# Main app
st.title("AntiSocial")
st.subheader("AI Content Brain for Social Media")

# Sidebar
with st.sidebar:
    st.header("Sessions")
    
    if st.session_state.session_id:
        st.success("Active Session")
        if st.button("New Session"):
            st.session_state.session_id = None
            st.session_state.messages = []
            st.session_state.content = None
            st.rerun()
    else:
        st.info("Generate content to start")
    
    st.divider()
    
    # Load session history
    sessions_data = call_api("/sessions")
    if sessions_data and sessions_data["sessions"]:
        st.subheader("Session History")
        
        for session in sessions_data["sessions"]:
            session_id = session["session_id"]
            platform = session["platform"].title()
            topic = session["topic"]
            
            # Create a nice display name
            display_name = f"{platform}: {topic[:20]}{'...' if len(topic) > 20 else ''}"
            
            # Show current session differently
            if session_id == st.session_state.session_id:
                st.info(f"🔵 {display_name}")
            else:
                if st.button(f" {display_name}", key=f"load_{session_id}"):
                    # Load this session
                    session_detail = call_api(f"/sessions/{session_id}")
                    if session_detail:
                        st.session_state.session_id = session_id
                        st.session_state.content = session_detail.get("content")
                        st.session_state.messages = [{
                            "role": "assistant",
                            "content": f"Loaded session: {topic} ({platform})"
                        }]
                        st.rerun()
    else:
        st.write("No previous sessions")

# Get platforms
platforms_data = call_api("/platforms")
if not platforms_data:
    st.error("Backend not available")
    st.stop()

platforms = platforms_data["platforms"]

# Main content
if not st.session_state.session_id:
    # Generate form
    st.header("Generate Content")
    
    with st.form("generate"):
        col1, col2 = st.columns(2)
        
        with col1:
            platform_options = {p["name"]: p["name"].lower() for p in platforms}
            platform_name = st.selectbox("Platform:", list(platform_options.keys()))
            platform = platform_options[platform_name]
            topic = st.text_input("Topic:", placeholder="e.g., AI for students")
        
        with col2:
            audience = st.text_input("Audience:", placeholder="e.g., college students")
            tone = st.selectbox("Tone:", ["professional", "casual", "funny", "educational"])
        
        if st.form_submit_button("Generate"):
            if topic and audience:
                with st.spinner("Generating..."):
                    result = call_api("/generate", "POST", {
                        "platform": platform,
                        "topic": topic,
                        "audience": audience,
                        "tone": tone
                    })
                    
                    if result:
                        st.session_state.session_id = result["session_id"]
                        st.session_state.content = result
                        st.session_state.messages = [{
                            "role": "assistant",
                            "content": f"Generated content for '{topic}' on {platform_name}!"
                        }]
                        st.rerun()
            else:
                st.warning("Fill all fields")

else:
    # Chat interface
    st.header("Chat with AI Agent")
    
    # Messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Example prompts
    st.markdown("**Try these example prompts:**")
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        if st.button("Make hashtags more professional"):
            example_prompt = "Make the hashtags more professional and industry-specific"
            st.session_state.messages.append({"role": "user", "content": example_prompt})
            st.rerun()
    
    with example_col2:
        if st.button("Change tone to casual"):
            example_prompt = "Change the tone to be more casual and friendly"
            st.session_state.messages.append({"role": "user", "content": example_prompt})
            st.rerun()
    
    with example_col3:
        if st.button("Add more technical angles"):
            example_prompt = "Add more technical and detailed content angles"
            st.session_state.messages.append({"role": "user", "content": example_prompt})
            st.rerun()
    
    # Chat input (outside columns)
    if prompt := st.chat_input("Ask me to modify the content..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Thinking..."):
            response = call_api("/chat", "POST", {
                "session_id": st.session_state.session_id,
                "message": prompt
            })
            
            if response:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["message"]
                })
                
                if response.get("updated_content"):
                    st.session_state.content = response["updated_content"]
                    # Show success message
                    st.success("Content updated! Check the updated content below.")
                
                st.rerun()
    
    # Current content (below chat)
    if st.session_state.content:
        st.divider()
        st.header("Current Content")
        
        # Debug section (can be removed later)
        with st.expander("Debug - Raw Content Structure"):
            st.json(st.session_state.content)
        
        display_content(st.session_state.content)