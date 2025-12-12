from groq_service import call_groq, parse_json_response
from storage import storage
import uuid

class ContentAgent:
    def __init__(self, platform):
        self.platform = platform
    
    def generate_content(self, topic, audience, tone):
        """Generate content for the platform"""
        prompt = self._build_prompt(topic, audience, tone)
        
        messages = [
            {"role": "system", "content": self._get_system_prompt()},
            {"role": "user", "content": prompt}
        ]
        
        response = call_groq(messages)
        content_data = parse_json_response(response)
        
        # If parsing failed, use fallback
        if not content_data:
            content_data = self._get_fallback_content(topic)
        
        # Create session
        from datetime import datetime
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "platform": self.platform,
            "topic": topic,
            "audience": audience,
            "tone": tone,
            "content": content_data,
            "created_at": datetime.now().isoformat()
        }
        
        storage.save_session(session_id, session_data)
        storage.save_conversation(session_id, [])
        
        return {
            **content_data,
            "session_id": session_id
        }
    
    def _get_fallback_content(self, topic):
        """Get fallback content if AI parsing fails"""
        if self.platform == "linkedin":
            return {
                "trending_angles": [
                    f"Professional insights about {topic}",
                    f"Career opportunities in {topic}",
                    f"Industry trends related to {topic}",
                    f"Business applications of {topic}",
                    f"Professional development through {topic}"
                ],
                "hashtags": ["#LinkedIn", "#Professional", "#Career", "#Industry", "#Business", f"#{topic.replace(' ', '')}"],
                "post_blueprints": [
                    {
                        "hook": f"Here's what professionals need to know about {topic}...",
                        "outline": [
                            f"Key professional insight about {topic}",
                            f"Industry impact and opportunities",
                            f"Actionable advice for career growth",
                            f"Real-world applications in business"
                        ],
                        "cta": "What's your experience with this? Share your thoughts in the comments."
                    },
                    {
                        "hook": f"3 career lessons I learned from {topic}:",
                        "outline": [
                            f"Lesson 1: Strategic thinking about {topic}",
                            f"Lesson 2: Leadership opportunities in {topic}",
                            f"Lesson 3: Network building through {topic}",
                            f"How to apply these in your career"
                        ],
                        "cta": "Which lesson resonates most with you? Let me know below."
                    },
                    {
                        "hook": f"The future of {topic} in professional settings:",
                        "outline": [
                            f"Current state of {topic} in business",
                            f"Emerging trends and opportunities",
                            f"Skills professionals need to develop",
                            f"Action steps for career preparation"
                        ],
                        "cta": "How are you preparing for these changes? Share your strategy."
                    }
                ]
            }
        
        elif self.platform == "instagram":
            return {
                "trending_angles": [
                    f"Behind the scenes of {topic}",
                    f"Daily life with {topic}",
                    f"Visual guide to {topic}",
                    f"Before and after with {topic}",
                    f"Aesthetic {topic} inspiration"
                ],
                "hashtags": ["#Instagram", "#Visual", "#Lifestyle", "#Aesthetic", "#Daily", f"#{topic.replace(' ', '')}", "#Inspiration"],
                "post_blueprints": [
                    {
                        "hook": f"This {topic} moment caught my attention...",
                        "outline": [
                            f"Visual story about {topic}",
                            f"Personal connection to {topic}",
                            f"Lifestyle integration tips",
                            f"Community inspiration"
                        ],
                        "cta": "Save this for later! What's your experience with this? ✨"
                    },
                    {
                        "hook": f"Step-by-step {topic} tutorial 📖",
                        "outline": [
                            f"Step 1: Getting started with {topic}",
                            f"Step 2: The key technique for {topic}",
                            f"Step 3: Pro tips for {topic}",
                            f"Final result and celebration"
                        ],
                        "cta": "Try this and tag me in your results! 🙌"
                    },
                    {
                        "hook": f"Before vs After: My {topic} journey",
                        "outline": [
                            f"Where I started with {topic}",
                            f"The transformation process",
                            f"Key moments and breakthroughs",
                            f"Current results and future goals"
                        ],
                        "cta": "What's your transformation story? Share below! 💫"
                    },
                    {
                        "hook": f"Aesthetic {topic} inspiration for your feed ✨",
                        "outline": [
                            f"Color palette ideas for {topic}",
                            f"Styling tips and arrangements",
                            f"Photography angles and lighting",
                            f"Creating cohesive visual story"
                        ],
                        "cta": "Which style speaks to you? Save for inspo! 📌"
                    }
                ]
            }
        
        else:  # twitter
            return {
                "trending_angles": [
                    f"Hot take on {topic}",
                    f"Thread about {topic} insights",
                    f"Quick {topic} tips",
                    f"Discussion starter about {topic}",
                    f"Real-time {topic} observations"
                ],
                "hashtags": ["#Twitter", "#Thread", "#Discussion", f"#{topic.replace(' ', '')}", "#Insights"],
                "post_blueprints": [
                    {
                        "hook": f"Unpopular opinion about {topic}... 🧵",
                        "outline": [
                            f"Main point about {topic}",
                            f"Supporting evidence or example",
                            f"Why this matters now",
                            f"Call for community discussion"
                        ],
                        "cta": "What's your take? Reply with your thoughts 👇"
                    },
                    {
                        "hook": f"Quick thread: 5 things about {topic} that changed my perspective",
                        "outline": [
                            f"Thing 1: Surprising insight about {topic}",
                            f"Thing 2: Common misconception debunked",
                            f"Thing 3: Practical application tip",
                            f"Thing 4: Future implications",
                            f"Thing 5: Key takeaway for everyone"
                        ],
                        "cta": "Which one surprised you most? RT if helpful! 🔄"
                    },
                    {
                        "hook": f"Let's discuss: What's your experience with {topic}?",
                        "outline": [
                            f"My personal experience with {topic}",
                            f"What I've learned from others",
                            f"Common challenges people face",
                            f"Question for the community"
                        ],
                        "cta": "Share your story in the replies - let's learn together! 💬"
                    },
                    {
                        "hook": f"Educational thread: Everything you need to know about {topic} 📚",
                        "outline": [
                            f"Basic definition and importance of {topic}",
                            f"Key concepts everyone should understand",
                            f"Common mistakes to avoid",
                            f"Resources for learning more",
                            f"Action steps to get started"
                        ],
                        "cta": "Bookmark this thread! Share with someone who needs to see it 🔖"
                    },
                    {
                        "hook": f"Real talk about {topic} - here's what nobody tells you:",
                        "outline": [
                            f"The reality behind {topic}",
                            f"What the experts don't mention",
                            f"Hidden challenges and solutions",
                            f"Honest advice from experience"
                        ],
                        "cta": "Agree or disagree? Let's have an honest conversation 🗣️"
                    }
                ]
            }
    
    def chat(self, session_id, message):
        """Chat to modify content"""
        session = storage.get_session(session_id)
        if not session:
            return {"error": "Session not found"}
        
        # Get conversation history
        conversation = storage.get_conversation(session_id)
        
        # Build chat prompt for content modification
        chat_prompt = f"""
        You are helping modify social media content for {session['platform'].upper()}.
        
        Current content:
        Topic: {session['topic']}
        Audience: {session['audience']}
        Tone: {session['tone']}
        
        Current trending angles: {session['content']['trending_angles']}
        Current hashtags: {session['content']['hashtags']}
        Current post blueprints: {session['content']['post_blueprints']}
        
        User request: "{message}"
        
        Based on the user's request, modify the content and return ONLY a JSON response with the updated content in this exact format:
        {{
            "trending_angles": [updated list of 5-7 angles],
            "hashtags": [updated list of hashtags],
            "post_blueprints": [updated list of post structures with hook, outline, cta]
        }}
        
        Make sure the modifications align with the user's request while keeping the content optimized for {session['platform']}.
        """
        
        messages = [
            {"role": "system", "content": self._get_chat_system_prompt()},
            {"role": "user", "content": chat_prompt}
        ]
        
        response = call_groq(messages, max_tokens=1500)
        
        # Add to conversation
        conversation.append({"role": "user", "content": message})
        storage.save_conversation(session_id, conversation)
        
        # Parse updated content
        updated_data = parse_json_response(response)
        
        if updated_data:
            # Successfully parsed updated content
            session["content"] = updated_data
            storage.save_session(session_id, session)
            
            # Add assistant response to conversation
            conversation.append({"role": "assistant", "content": f"✅ Updated content based on: {message}"})
            storage.save_conversation(session_id, conversation)
            
            return {
                "message": f"✅ I've updated your content based on: '{message}'. Check the updated content below!",
                "updated_content": updated_data
            }
        else:
            # If parsing failed, it might be a conversational response
            conversation.append({"role": "assistant", "content": response})
            storage.save_conversation(session_id, conversation)
            
            return {
                "message": response,
                "updated_content": None
            }
    
    def _get_system_prompt(self):
        """Get system prompt for the platform"""
        if self.platform == "linkedin":
            return """You are a LinkedIn content expert. Create professional, engaging content 
            focused on career growth, industry insights, and business value. Use 8-12 professional hashtags."""
        
        elif self.platform == "instagram":
            return """You are an Instagram content expert. Create visual, engaging content 
            focused on lifestyle, tutorials, and aesthetic appeal. Use 15-25 discovery hashtags."""
        
        elif self.platform == "twitter":
            return """You are a Twitter content expert. Create concise, engaging content 
            focused on discussions, threads, and real-time engagement. Use 5-8 strategic hashtags."""
        
        return "You are a social media content expert."
    
    def _get_chat_system_prompt(self):
        """Get system prompt for chat/modification mode"""
        if self.platform == "linkedin":
            return """You are a LinkedIn content expert helping modify existing content. 
            Focus on professional tone, career insights, and business value. 
            Always return valid JSON with updated content when asked to modify."""
        
        elif self.platform == "instagram":
            return """You are an Instagram content expert helping modify existing content. 
            Focus on visual appeal, lifestyle content, and engagement. 
            Always return valid JSON with updated content when asked to modify."""
        
        elif self.platform == "twitter":
            return """You are a Twitter content expert helping modify existing content. 
            Focus on concise, engaging discussions and real-time relevance. 
            Always return valid JSON with updated content when asked to modify."""
        
        return "You are a social media content expert helping modify content. Always return valid JSON when asked to modify."
    
    def _build_prompt(self, topic, audience, tone):
        """Build content generation prompt"""
        if self.platform == "linkedin":
            return f"""
            Create LinkedIn content for "{topic}" targeting {audience} with a {tone} tone.
            
            Return EXACTLY this JSON structure:
            {{
                "trending_angles": [5-7 professional content angles],
                "hashtags": [8-12 professional hashtags including #LinkedIn, #Professional, #CareerGrowth],
                "post_blueprints": [
                    {{
                        "hook": "Professional hook line 1",
                        "outline": ["Professional point 1", "Professional point 2", "Professional point 3"],
                        "cta": "Professional call-to-action"
                    }},
                    {{
                        "hook": "Different professional hook line 2", 
                        "outline": ["Different point 1", "Different point 2", "Different point 3"],
                        "cta": "Different professional CTA"
                    }},
                    {{
                        "hook": "Third professional hook line 3",
                        "outline": ["Third point 1", "Third point 2", "Third point 3"], 
                        "cta": "Third professional CTA"
                    }}
                ]
            }}
            
            Make all 3 blueprints different approaches to the same topic.
            """
        
        elif self.platform == "instagram":
            return f"""
            Create Instagram content for "{topic}" targeting {audience} with a {tone} tone.
            
            Return EXACTLY this JSON structure:
            {{
                "trending_angles": [5-7 visual content angles],
                "hashtags": [15-25 discovery hashtags including #Instagram, #Visual, #Aesthetic],
                "post_blueprints": [
                    {{
                        "hook": "Visual hook for Reel/Post 1",
                        "outline": ["Visual element 1", "Story element 1", "Engagement element 1"],
                        "cta": "Instagram CTA 1 (save, share, tag)"
                    }},
                    {{
                        "hook": "Different visual hook for Story/Carousel 2",
                        "outline": ["Different visual 1", "Different story 1", "Different engagement 1"],
                        "cta": "Different Instagram CTA 2"
                    }},
                    {{
                        "hook": "Third visual hook for Tutorial/Behind-scenes 3",
                        "outline": ["Tutorial step 1", "Tutorial step 2", "Tutorial step 3"],
                        "cta": "Tutorial CTA 3"
                    }},
                    {{
                        "hook": "Fourth aesthetic hook for Lifestyle content 4",
                        "outline": ["Lifestyle element 1", "Aesthetic element 1", "Community element 1"],
                        "cta": "Lifestyle CTA 4"
                    }}
                ]
            }}
            
            Make all 4 blueprints different content formats (Reel, Story, Tutorial, Lifestyle).
            """
        
        elif self.platform == "twitter":
            return f"""
            Create Twitter content for "{topic}" targeting {audience} with a {tone} tone.
            
            Return EXACTLY this JSON structure:
            {{
                "trending_angles": [5-7 Twitter content angles],
                "hashtags": [5-8 strategic hashtags including #Twitter, #Thread],
                "post_blueprints": [
                    {{
                        "hook": "Thread hook (under 280 chars) 1",
                        "outline": ["Tweet 1 point", "Tweet 2 point", "Tweet 3 point", "Tweet 4 point"],
                        "cta": "Thread CTA encouraging replies"
                    }},
                    {{
                        "hook": "Quick take hook (under 280 chars) 2",
                        "outline": ["Quick insight 1", "Quick insight 2", "Quick insight 3"],
                        "cta": "Quick take CTA for retweets"
                    }},
                    {{
                        "hook": "Discussion starter hook 3",
                        "outline": ["Discussion point 1", "Discussion point 2", "Question for community"],
                        "cta": "Discussion CTA asking for opinions"
                    }},
                    {{
                        "hook": "Hot take hook 4",
                        "outline": ["Controversial point 1", "Supporting evidence", "Why it matters"],
                        "cta": "Hot take CTA for engagement"
                    }},
                    {{
                        "hook": "Educational thread hook 5",
                        "outline": ["Educational point 1", "Educational point 2", "Educational point 3", "Key takeaway"],
                        "cta": "Educational CTA for sharing"
                    }}
                ]
            }}
            
            Make all 5 blueprints different Twitter formats (Thread, Quick take, Discussion, Hot take, Educational).
            """
        
        return f"""
        Create social media content for {self.platform.upper()} about "{topic}" 
        for {audience} with a {tone} tone.
        
        Return JSON with:
        - trending_angles: 5-7 content angles
        - hashtags: platform-appropriate hashtags
        - post_blueprints: 3-5 different post structures with hook, outline, and cta
        
        Make each blueprint a different approach to the same topic.
        """

# Agent instances
agents = {
    "linkedin": ContentAgent("linkedin"),
    "instagram": ContentAgent("instagram"), 
    "twitter": ContentAgent("twitter")
}