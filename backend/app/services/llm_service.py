from app.core.config import get_settings
from app.providers.llm.base import LLMProvider
from app.providers.llm.mock import MockLLMProvider
from app.providers.llm.gemini import GeminiProvider


def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    provider_name = settings.LLM_PROVIDER.lower()
    if provider_name == "gemini" and settings.LLM_API_KEY:
        return GeminiProvider(api_key=settings.LLM_API_KEY)
    return MockLLMProvider()
