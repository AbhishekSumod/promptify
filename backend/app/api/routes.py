from fastapi import APIRouter

from app.models.schemas import ChatResponse, EnhanceResponse, MessageRequest
from app.services.chatbot import generate_reply
from app.services.enhancer import enhance_prompt

router = APIRouter()


@router.post("/enhance", response_model=EnhanceResponse)
def enhance_message(payload: MessageRequest) -> EnhanceResponse:
    enhanced = enhance_prompt(payload.message)
    return EnhanceResponse(enhanced_message=enhanced)


@router.post("/chat", response_model=ChatResponse)
def chat(payload: MessageRequest) -> ChatResponse:
    reply = generate_reply(payload.message)
    return ChatResponse(reply=reply)
