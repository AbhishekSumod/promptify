from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import ChatResponse, EnhanceResponse, MessageRequest, PdfSummaryResponse
from app.services.chatbot import generate_reply
from app.services.enhancer import enhance_prompt
from app.services.pdf_summarizer import summarize_pdf

router = APIRouter()


@router.post("/enhance", response_model=EnhanceResponse)
def enhance_message(payload: MessageRequest) -> EnhanceResponse:
    enhanced = enhance_prompt(payload.message)
    return EnhanceResponse(enhanced_message=enhanced)


@router.post("/chat", response_model=ChatResponse)
def chat(payload: MessageRequest) -> ChatResponse:
    reply = generate_reply(payload.message)
    return ChatResponse(reply=reply)


@router.post("/summarize-pdf", response_model=PdfSummaryResponse)
async def summarize_uploaded_pdf(file: UploadFile = File(...)) -> PdfSummaryResponse:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty.")

    summary = summarize_pdf(file_bytes)
    return PdfSummaryResponse(summary=summary)