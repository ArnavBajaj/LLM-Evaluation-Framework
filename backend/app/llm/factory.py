from app.llm.base import BaseLLM


class LLMFactory:
    def __init__(self, providers: dict[str, BaseLLM]) -> None:
        self._providers = providers

    def get(self, provider_name: str) -> BaseLLM:
        try:
            return self._providers[provider_name]
        except KeyError as exc:
            raise ValueError(f"Unknown provider: {provider_name}") from exc
