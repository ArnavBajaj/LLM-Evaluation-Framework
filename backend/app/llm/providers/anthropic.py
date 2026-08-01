from __future__ import annotations

import time
from typing import Any

from app.llm.base import LLMResponse
from app.llm.providers.common import HTTPProviderBase, ProviderSettings


class AnthropicLLM(HTTPProviderBase):
    def __init__(self, settings: ProviderSettings) -> None:
        super().__init__(settings)

    def calculate_cost(self, *, prompt_tokens: int, completion_tokens: int) -> float:
        return (prompt_tokens * 0.003 + completion_tokens * 0.015) / 1000

    async def generate(self, prompt: str, *, temperature: float = 0.0, seed: int | None = None) -> LLMResponse:
        if not self._settings.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is required for the Anthropic adapter")

        payload: dict[str, Any] = {
            "model": self._settings.model_name,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        if seed is not None:
            payload["seed"] = seed

        headers = {
            "x-api-key": self._settings.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        start = time.perf_counter()
        response = await self._request_json("POST", f"{self._settings.base_url}/v1/messages", headers=headers, json=payload)
        latency_seconds = time.perf_counter() - start
        content = "".join(block.get("text", "") for block in response.get("content", []) if block.get("type") == "text")
        usage = response.get("usage", {})
        prompt_tokens = int(usage.get("input_tokens", self.count_tokens(prompt)))
        completion_tokens = int(usage.get("output_tokens", self.count_tokens(content)))
        return self._build_response(
            content=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_seconds=latency_seconds,
            raw_metadata={"raw": response},
        )
