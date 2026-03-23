import os
from dataclasses import dataclass
from typing import Union

from dotenv import load_dotenv

# Load environment variables from backend/.env when available.
load_dotenv()


def _to_bool(value: str, default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _ssl_verify_setting(value: str):
    if value is None or not value.strip():
        return True

    normalized = value.strip().lower()
    if normalized in {"0", "false", "no", "off"}:
        return False
    if normalized in {"1", "true", "yes", "on"}:
        return True

    # Allows passing a corporate CA bundle path.
    return value.strip()


@dataclass(frozen=True)
class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY", "").strip()
    groq_base_url: str = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1").rstrip("/")
    groq_chat_model: str = os.getenv("GROQ_CHAT_MODEL", "llama-3.1-8b-instant")
    groq_enhance_model: str = os.getenv("GROQ_ENHANCE_MODEL", "llama-3.1-8b-instant")
    use_mock_fallback: bool = _to_bool(os.getenv("USE_MOCK_FALLBACK"), default=True)
    groq_verify_ssl: Union[bool, str] = _ssl_verify_setting(os.getenv("GROQ_VERIFY_SSL"))


settings = Settings()
