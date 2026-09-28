import pytest
from app.providers.llm.mock import MockLLMProvider
from app.providers.llm.base import LLMProvider
from app.services.llm_service import get_llm_provider


@pytest.mark.asyncio
async def test_mock_provider():
    provider = MockLLMProvider()
    result = await provider.generate("system", "user")
    assert "Subject:" in result
    assert "Body:" in result or "Dear" in result


def test_get_llm_provider_mock():
    provider = get_llm_provider()
    assert isinstance(provider, LLMProvider)


@pytest.mark.asyncio
async def test_mock_provider_returns_professional_email():
    provider = MockLLMProvider()
    result = await provider.generate("Write professional email", "Introduce CRM")
    assert len(result) > 50
