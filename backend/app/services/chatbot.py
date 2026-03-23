from typing import Dict

from app.core.settings import settings
from app.services.groq_client import groq_client
from app.services.text_cleaner import clean_markdown_artifacts


MOCK_RESPONSES: Dict[str, str] = {
    "gym": "For gym progress, focus on progressive overload: add small weight or reps weekly, train 3-4 days, and track workouts.",
    "diet": "A sustainable diet starts with protein at each meal, mostly whole foods, and a slight calorie deficit if fat loss is the goal.",
    "study": "Use 45-minute focused study blocks, active recall, and spaced repetition. End each session with a 5-minute recap.",
}


def _mock_reply(message: str) -> str:
    lowered = message.lower()
    for keyword, reply in MOCK_RESPONSES.items():
        if keyword in lowered:
            return reply
    return (
        "I can help with planning, productivity, fitness, or learning goals. "
        "Try adding details like your objective, timeline, and constraints."
    )


def generate_reply(message: str) -> str:
    """
    Uses Groq for chat when configured, with a mock fallback for resilience.
    """
    system_prompt = (
        "You are a helpful assistant. Provide concise, actionable responses. "
        "If the request is broad, return short step-by-step guidance. "
        "Return plain text only. Do not use markdown symbols like **, #, or backticks."
    )

    ai_reply = groq_client.chat_completion(
        system_prompt=system_prompt,
        user_prompt=message.strip(),
        model=settings.groq_chat_model,
        temperature=0.5,
        max_tokens=450,
    )

    if ai_reply:
        return clean_markdown_artifacts(ai_reply)

    return _mock_reply(message) if settings.use_mock_fallback else "AI service is currently unavailable."
