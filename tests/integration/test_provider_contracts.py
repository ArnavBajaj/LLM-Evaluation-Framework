import pytest

from app.llm.providers import AnthropicLLM, GeminiLLM, MistralLLM, OllamaLLM, OpenAILLM
from app.llm.providers.common import ProviderSettings


@pytest.mark.parametrize(
    "provider_cls, provider_name, base_url",
    [
        (OpenAILLM, "openai", "https://api.openai.com/v1"),
        (AnthropicLLM, "anthropic", "https://api.anthropic.com"),
        (GeminiLLM, "gemini", "https://generativelanguage.googleapis.com"),
        (MistralLLM, "mistral", "https://api.mistral.ai/v1"),
        (OllamaLLM, "ollama", "http://localhost:11434"),
    ],
)
def test_provider_contract_metadata(provider_cls, provider_name, base_url) -> None:
    provider = provider_cls(
        ProviderSettings(
            provider_name=provider_name,
            model_name="test-model",
            base_url=base_url,
            api_key="test-key",
        )
    )

    assert provider.provider_name() == provider_name
    assert provider.count_tokens("hello world") == 2
    assert provider.calculate_cost(prompt_tokens=10, completion_tokens=5) >= 0.0
