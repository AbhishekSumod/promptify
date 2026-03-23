import re


def clean_markdown_artifacts(text: str) -> str:
    """
    Convert common markdown formatting into clean plain text for UI display.
    """
    cleaned = text.replace("**", "").replace("__", "").replace("`", "")
    cleaned = re.sub(r"^\s{0,3}#{1,6}\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*[-*]\s+", "- ", cleaned, flags=re.MULTILINE)
    return cleaned.strip()

