from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class LLMResponse:
    provider_name: str
    model_name: str
    content: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    latency_ms: int
    raw_metadata: dict[str, object]


class BaseLLM(ABC):
    @abstractmethod
    async def generate(self, prompt: str, *, temperature: float = 0.0, seed: int | None = None) -> LLMResponse:
        raise NotImplementedError

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def calculate_cost(self, *, prompt_tokens: int, completion_tokens: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError
