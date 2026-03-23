from io import BytesIO
from typing import List

from pypdf import PdfReader

from app.core.settings import settings
from app.services.groq_client import groq_client
from app.services.text_cleaner import clean_markdown_artifacts


def _extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    parts: List[str] = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            parts.append(page_text.strip())

    return "\n\n".join(parts).strip()


def _chunk_text(text: str, chunk_size: int = 5500) -> List[str]:
    if len(text) <= chunk_size:
        return [text]

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks


def summarize_pdf(file_bytes: bytes) -> str:
    extracted = _extract_pdf_text(file_bytes)
    if not extracted:
        return "Could not extract readable text from this PDF."

    chunks = _chunk_text(extracted)
    partial_summaries: List[str] = []

    system_prompt = (
        "You summarize PDF content for business and learning use cases. "
        "Return plain text only. Keep the summary clear and concise."
    )

    for index, chunk in enumerate(chunks, start=1):
        user_prompt = (
            f"Summarize PDF chunk {index}/{len(chunks)}. "
            "Focus on key points, major conclusions, and actionable insights.\n\n"
            f"{chunk}"
        )
        ai_summary = groq_client.chat_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=settings.groq_chat_model,
            temperature=0.2,
            max_tokens=500,
        )
        if ai_summary:
            partial_summaries.append(clean_markdown_artifacts(ai_summary))
        else:
            fallback = chunk[:700].strip()
            partial_summaries.append(f"Chunk {index} summary fallback:\n{fallback}...")

    if len(partial_summaries) == 1:
        return partial_summaries[0]

    combined_prompt = "\n\n".join(partial_summaries)
    final_summary = groq_client.chat_completion(
        system_prompt=(
            "Merge multiple chunk summaries into one final plain-text summary. "
            "Use short sections: Overview, Key Points, Action Items."
        ),
        user_prompt=combined_prompt,
        model=settings.groq_chat_model,
        temperature=0.2,
        max_tokens=700,
    )
    if final_summary:
        return clean_markdown_artifacts(final_summary)

    return "\n\n".join(partial_summaries)

