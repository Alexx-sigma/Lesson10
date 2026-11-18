"""Safe offline AI stub. Replace only after agreeing on API contract."""


class AIServiceError(Exception):
    """Raised when the AI service cannot produce a response."""


def generate_reply(prompt: str) -> str:
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Запрос должен быть непустой строкой")
    return f"[ДЕМО-РЕЖИМ] Получен запрос: {prompt.strip()}"
