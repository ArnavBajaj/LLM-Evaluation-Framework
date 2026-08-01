from app.core.config import settings
from app.llm.factory import LLMFactory
from app.llm.providers import AnthropicLLM, GeminiLLM, MistralLLM, OllamaLLM, OpenAILLM
from app.llm.providers.common import ProviderSettings


def build_default_factory() -> LLMFactory:
    providers = {
        "openai": OpenAILLM(
            ProviderSettings(
                provider_name="openai",
                model_name="gpt-4o-mini",
                base_url="https://api.openai.com/v1",
                api_key=settings.openai_api_key,
            )
        ),
        "anthropic": AnthropicLLM(
            ProviderSettings(
                provider_name="anthropic",
                model_name="claude-3-5-sonnet-latest",
                base_url="https://api.anthropic.com",
                api_key=settings.anthropic_api_key,
            )
        ),
        "gemini": GeminiLLM(
            ProviderSettings(
                provider_name="gemini",
                model_name="gemini-2.0-flash",
                base_url="https://generativelanguage.googleapis.com",
                api_key=settings.google_api_key,
            )
        ),
        "mistral": MistralLLM(
            ProviderSettings(
                provider_name="mistral",
                model_name="mistral-large-latest",
                base_url="https://api.mistral.ai/v1",
                api_key=settings.mistral_api_key,
            )
        ),
        "ollama": OllamaLLM(
            ProviderSettings(
                provider_name="ollama",
                model_name="llama3.1",
                base_url=settings.ollama_base_url,
                api_key=None,
            )
        ),
    }
    return LLMFactory(providers)
