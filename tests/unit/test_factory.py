import pytest

from app.llm.base import BaseLLM, LLMResponse
from app.llm.factory import LLMFactory


class StubLLM(BaseLLM):
    async def generate(self, prompt: str, *, temperature: float = 0.0, seed: int | None = None) -> LLMResponse:
        del prompt, temperature, seed
        return LLMResponse(
            provider_name="stub",
            model_name="stub-model",
            content="ok",
            prompt_tokens=1,
            completion_tokens=1,
            total_tokens=2,
            cost_usd=0.0,
            latency_ms=1,
            raw_metadata={},
        )

    def count_tokens(self, text: str) -> int:
        return len(text.split())

    def calculate_cost(self, *, prompt_tokens: int, completion_tokens: int) -> float:
        return 0.0

    def provider_name(self) -> str:
        return "stub"


def test_factory_returns_registered_provider() -> None:
    provider = StubLLM()
    factory = LLMFactory({"stub": provider})

    assert factory.get("stub") is provider


def test_factory_raises_for_unknown_provider() -> None:
    factory = LLMFactory({})

    with pytest.raises(ValueError, match="Unknown provider"):
        factory.get("missing")
