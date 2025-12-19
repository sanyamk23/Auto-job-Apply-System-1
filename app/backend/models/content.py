from pydantic import BaseModel


class ContentRequest(BaseModel):
    platform: str
    topic: str
    audience: str
    tone: str
