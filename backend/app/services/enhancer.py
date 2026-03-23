from typing import List

from app.core.settings import settings
from app.services.groq_client import groq_client
from app.services.text_cleaner import clean_markdown_artifacts


def _enhance_rule_based(message: str) -> str:
    clean_message = message.strip()
    guidance: List[str] = [
        "Task: Respond clearly and practically.",
        f"User Request: {clean_message}",
        "Context: Assume beginner-friendly explanation unless specified.",
        "Output Format: Provide concise steps and one practical example.",
        "Quality Bar: Be specific, actionable, and avoid vague statements.",
    ]
    return "\n".join(guidance)


def enhance_prompt(message: str) -> str:
    """
    Uses Groq for enhancement when configured, otherwise falls back to rule-based.
    """
    system_prompt = (
        "You improve prompts for an AI assistant. "
        "Rewrite the user text into a clear, structured prompt with sections: "
        "Task, Context, Constraints, Output Format. "
        "Return plain text only. Do not use markdown symbols like **, #, or backticks. "
        "Keep it concise and practical."
    )

    enhanced = groq_client.chat_completion(
        system_prompt=system_prompt,
        user_prompt=message.strip(),
        model=settings.groq_enhance_model,
        temperature=0.2,
        max_tokens=350,
    )

    if enhanced:
        return clean_markdown_artifacts(enhanced)

    return _enhance_rule_based(message)
