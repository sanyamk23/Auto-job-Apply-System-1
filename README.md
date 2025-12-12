# 🧠 AntiSocial - AI Content Brain for Social Media

> **Transform your social media strategy with AI-powered content generation and conversational refinement**

AntiSocial is a production-ready social media content generation platform that uses specialized AI agents to create platform-optimized content for LinkedIn, Instagram, and Twitter. Unlike generic content tools, AntiSocial provides multiple content blueprints per platform and allows real-time conversational refinement through an intuitive chat interface.

## ✨ Key Features

### 🤖 **Specialized AI Agents**
- **LinkedIn Agent**: Professional content focused on career growth, industry insights, and business networking
- **Instagram Agent**: Visual-first content with aesthetic appeal, tutorials, and lifestyle integration
- **Twitter Agent**: Engagement-driven content including threads, discussions, and real-time commentary

### 📊 **Multi-Blueprint Generation**
- **LinkedIn**: 3 different professional approaches per topic
- **Instagram**: 4 content formats (Reels, Stories, Tutorials, Lifestyle)
- **Twitter**: 5 engagement types (Threads, Quick takes, Discussions, Hot takes, Educational)

### 💬 **Conversational Content Refinement**
- Chat with AI agents to modify content in real-time
- Natural language requests: *"Make hashtags more professional"*, *"Change tone to casual"*
- Iterative improvement without starting over

### 📚 **Session Management**
- Persistent session storage with automatic saving
- Session history sidebar for easy project switching
- Resume work on any previous content generation

### 🎯 **Platform Optimization**
- Platform-specific hashtag strategies (8-12 for LinkedIn, 15-25 for Instagram, 5-8 for Twitter)
- Content structure optimized for each platform's algorithm
- Audience-targeted messaging and tone adaptation

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.8+** (recommended: Python 3.9 or higher)
- **Groq API Key** (free tier available at [console.groq.com](https://console.groq.com/))

### Installation

1. **Clone and Setup Environment**:
```bash
git clone <repository-url>
cd AntiSocial
pip install -r requirements.txt
```

2. **Configure Environment**:
```bash
cp .env.example .env
```

3. **Add Your API Key**:
Edit `.env` file and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192
```

4. **Launch Application**:
```bash
python run.py
```

5. **Access Interface**:
- **Frontend**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

## 📖 How to Use

### Basic Content Generation

1. **Select Platform**: Choose LinkedIn, Instagram, or Twitter
2. **Define Parameters**:
   - **Topic**: Your content subject (e.g., "AI in healthcare")
   - **Audience**: Target demographic (e.g., "healthcare professionals")
   - **Tone**: Content style (professional, casual, funny, educational)
3. **Generate Content**: Click "🚀 Generate" to create initial content
4. **Review Output**: Examine trending angles, hashtags, and multiple post blueprints

### Advanced Content Refinement

Use the chat interface to refine your content with natural language:

**Example Refinement Prompts**:
```
"Make the hashtags more industry-specific"
"Change the tone to be more conversational"
"Add technical details to the content angles"
"Create more engaging hooks for the blueprints"
"Focus on actionable advice rather than theory"
```

### Session Management

- **Active Sessions**: Current work is automatically saved
- **Session History**: Access previous projects from the sidebar
- **Session Loading**: Click any previous session to resume work
- **New Sessions**: Start fresh content generation anytime

## 🏗️ Architecture Overview

### Core Components

```
AntiSocial/
├── 🎨 Frontend (Streamlit)
│   ├── Content generation forms
│   ├── Chat interface
│   └── Session management
├── 🔧 Backend (FastAPI)
│   ├── Content generation API
│   ├── Chat refinement API
│   └── Session management API
├── 🤖 AI Agents
│   ├── Platform-specific prompts
│   ├── Content structure templates
│   └── Refinement logic
└── 💾 Storage System
    ├── File-based persistence
    ├── Session data management
    └── Conversation history
```

### File Structure

| File | Purpose | Description |
|------|---------|-------------|
| `run.py` | **Application Launcher** | Starts both backend and frontend servers |
| `api.py` | **FastAPI Backend** | RESTful API with 6 endpoints for content generation and management |
| `frontend.py` | **Streamlit UI** | Interactive web interface with chat functionality |
| `agents.py` | **AI Content Agents** | Three specialized agents with platform-specific logic |
| `groq_service.py` | **AI Integration** | Groq API client with JSON parsing and error handling |
| `storage.py` | **Data Persistence** | Simple file-based storage for sessions and conversations |
| `config.py` | **Configuration** | Platform definitions and application settings |

## 🔧 API Reference

### Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/` | Health check | None |
| `GET` | `/platforms` | List available platforms | None |
| `POST` | `/generate` | Generate new content | `platform`, `topic`, `audience`, `tone` |
| `POST` | `/chat` | Refine existing content | `session_id`, `message` |
| `GET` | `/sessions` | List all sessions | None |
| `GET` | `/sessions/{id}` | Get specific session | `session_id` |

### Example API Usage

**Generate Content**:
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "linkedin",
    "topic": "AI in healthcare",
    "audience": "healthcare professionals",
    "tone": "professional"
  }'
```

**Refine Content**:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "message": "Make the hashtags more professional"
  }'
```

## 🎯 Content Output Structure

### Generated Content Format

Each content generation produces:

```json
{
  "trending_angles": [
    "Professional insight angle 1",
    "Industry trend angle 2",
    "Career development angle 3",
    "Business application angle 4",
    "Future outlook angle 5"
  ],
  "hashtags": [
    "#LinkedIn", "#Professional", "#Healthcare", 
    "#AI", "#Innovation", "#CareerGrowth"
  ],
  "post_blueprints": [
    {
      "hook": "Engaging opening line",
      "outline": [
        "Key point 1",
        "Supporting detail",
        "Actionable insight"
      ],
      "cta": "Call-to-action for engagement"
    }
  ],
  "session_id": "unique-session-identifier"
}
```

### Platform-Specific Outputs

**LinkedIn** (Professional Focus):
- 3 blueprints with different professional angles
- 8-12 industry-relevant hashtags
- Business-focused content structure

**Instagram** (Visual Focus):
- 4 blueprints for different content formats
- 15-25 discovery hashtags
- Visual storytelling elements

**Twitter** (Engagement Focus):
- 5 blueprints for various engagement types
- 5-8 strategic hashtags
- Thread-optimized content structure

## 🛠️ Development & Customization

### Adding New Platforms

1. **Update Configuration** (`config.py`):
```python
PLATFORMS = {
    "your_platform": {
        "name": "Your Platform",
        "description": "Platform description"
    }
}
```

2. **Create Agent** (`agents.py`):
```python
class YourPlatformAgent(ContentAgent):
    def _get_system_prompt(self):
        return "Your platform-specific prompt"
```

3. **Add to Agent Registry**:
```python
agents["your_platform"] = YourPlatformAgent("your_platform")
```

### Customizing Content Templates

Modify the `_build_prompt()` method in `agents.py` to adjust:
- Content structure requirements
- Number of blueprints generated
- Hashtag strategies
- Platform-specific formatting

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | Required | Your Groq API key |
| `GROQ_MODEL` | `llama3-8b-8192` | AI model to use |
| `API_PORT` | `8000` | Backend server port |
| `FRONTEND_PORT` | `8501` | Frontend server port |

## 🔍 Troubleshooting

### Common Issues

**API Connection Errors**:
- Verify Groq API key is correctly set in `.env`
- Check internet connection
- Ensure API key has sufficient credits

**Frontend Not Loading**:
- Confirm both servers are running (`python run.py`)
- Check ports 8000 and 8501 are available
- Try accessing http://localhost:8501 directly

**Content Generation Failures**:
- Check Groq API status
- Verify input parameters are complete
- Review logs for specific error messages

**Session Loading Issues**:
- Ensure `data/` directory exists and is writable
- Check session files in `data/` folder
- Verify JSON file integrity

### Debug Mode

Enable debug output by adding to your `.env`:
```env
DEBUG=true
```

## 📊 Performance & Scaling

### Current Capabilities
- **Concurrent Users**: Suitable for small teams (1-10 users)
- **Session Storage**: File-based (easily scalable to database)
- **API Rate Limits**: Dependent on Groq API tier
- **Response Time**: 2-5 seconds per generation

### Scaling Recommendations
- **Database**: Replace file storage with PostgreSQL/MongoDB for production
- **Caching**: Add Redis for session and content caching
- **Load Balancing**: Use nginx for multiple backend instances
- **API Management**: Implement rate limiting and authentication

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- **New Platform Support**: TikTok, YouTube, Facebook
- **Enhanced AI Models**: GPT-4, Claude integration
- **Advanced Features**: Content scheduling, analytics
- **UI/UX Improvements**: Better mobile experience
- **Performance**: Caching, optimization

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq**: Fast AI inference platform
- **Streamlit**: Rapid web app development
- **FastAPI**: Modern Python web framework
- **Community**: Open source contributors and users

---

**Built with ❤️ for content creators who want AI-powered social media strategies without the complexity.**