from app.llm.registry import build_default_factory


def test_default_factory_registers_supported_providers() -> None:
    factory = build_default_factory()

    providers = {
        name: factory.get(name).provider_name()
        for name in ["openai", "anthropic", "gemini", "mistral", "ollama"]
    }

    assert providers == {
        "openai": "openai",
        "anthropic": "anthropic",
        "gemini": "gemini",
        "mistral": "mistral",
        "ollama": "ollama",
    }
