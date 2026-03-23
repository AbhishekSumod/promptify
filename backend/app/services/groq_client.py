import logging
from typing import Optional

import httpx

from app.core.settings import settings

logger = logging.getLogger(__name__)


class GroqClient:
    """Small OpenAI-compatible Groq client wrapper."""

    def __init__(self) -> None:
        self._base_url = settings.groq_base_url
        self._api_key = settings.groq_api_key

    def is_configured(self) -> bool:
        return bool(self._api_key)

    def chat_completion(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float = 0.3,
        max_tokens: int = 350,
    ) -> Optional[str]:
        if not self.is_configured():
            return None

        url = f"{self._base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        try:
            response = httpx.post(
                url,
                headers=headers,
                json=payload,
                timeout=30,
                verify=settings.groq_verify_ssl,
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return content.strip() if isinstance(content, str) else None
        except Exception as exc:  # noqa: BLE001
            logger.warning("Groq request failed: %s", exc)
            return None


groq_client = GroqClient()
