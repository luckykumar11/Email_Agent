import logging

from app.core.config import get_settings
from app.providers.llm.base import LLMProvider
from app.providers.llm.mock import MockLLMProvider

logger = logging.getLogger(__name__)


def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    provider_name = settings.LLM_PROVIDER.lower()

    if provider_name == "fallback":
        return _build_fallback_chain(settings)

    if provider_name == "groq" and settings.GROQ_API_KEY:
        from app.providers.llm.groq import GroqProvider
        return GroqProvider(api_key=settings.GROQ_API_KEY)

    if provider_name == "gemini" and settings.LLM_API_KEY:
        from app.providers.llm.gemini import GeminiProvider
        return GeminiProvider(api_key=settings.LLM_API_KEY)

    return MockLLMProvider()


def _build_fallback_chain(settings) -> LLMProvider:
    providers = []

    if settings.GROQ_API_KEY:
        from app.providers.llm.groq import GroqProvider
        providers.append(("Groq", GroqProvider(api_key=settings.GROQ_API_KEY)))

    if settings.LLM_API_KEY:
        from app.providers.llm.gemini import GeminiProvider
        providers.append(("Gemini", GeminiProvider(api_key=settings.LLM_API_KEY)))

    providers.append(("Mock", MockLLMProvider()))

    return FallbackProvider(providers)


class FallbackProvider(LLMProvider):
    def __init__(self, providers: list[tuple[str, LLMProvider]]):
        self.providers = providers

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        last_error = None
        for name, provider in self.providers:
            try:
                logger.info("Attempting LLM generation with %s", name)
                result = await provider.generate(system_prompt, user_prompt)
                logger.info("LLM generation succeeded with %s", name)
                return result
            except Exception as e:
                logger.warning("LLM provider %s failed: %s", name, e)
                last_error = e
                continue

        raise RuntimeError(f"All LLM providers failed. Last error: {last_error}")
