from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message")


class EnhanceResponse(BaseModel):
    enhanced_message: str


class ChatResponse(BaseModel):
    reply: str
