from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.llm.base import BaseLLM, LLMResponse


@dataclass(slots=True)
class ProviderSettings:
    provider_name: str
    model_name: str
    base_url: str
    api_key: str | None
    timeout_seconds: float = 60.0


class HTTPProviderBase(BaseLLM):
    def __init__(self, settings: ProviderSettings) -> None:
        self._settings = settings

    def _token_estimate(self, text: str) -> int:
        return len(text.split())

    def count_tokens(self, text: str) -> int:
        return self._token_estimate(text)

    def calculate_cost(self, *, prompt_tokens: int, completion_tokens: int) -> float:
        del prompt_tokens, completion_tokens
        return 0.0

    def provider_name(self) -> str:
        return self._settings.provider_name

    async def _request_json(self, method: str, url: str, *, headers: dict[str, str] | None = None, json: dict[str, Any]) -> dict[str, Any]:
        timeout = httpx.Timeout(self._settings.timeout_seconds)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(method, url, headers=headers, json=json)
            response.raise_for_status()
            return response.json()

    def _build_response(
        self,
        *,
        content: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_seconds: float,
        raw_metadata: dict[str, Any],
    ) -> LLMResponse:
        total_tokens = prompt_tokens + completion_tokens
        return LLMResponse(
            provider_name=self._settings.provider_name,
            model_name=self._settings.model_name,
            content=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=self.calculate_cost(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens),
            latency_ms=int(latency_seconds * 1000),
            raw_metadata=raw_metadata,
        )
