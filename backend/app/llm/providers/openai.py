from __future__ import annotations

import time
from typing import Any

from app.llm.base import LLMResponse
from app.llm.providers.common import HTTPProviderBase, ProviderSettings


class OpenAILLM(HTTPProviderBase):
    def __init__(self, settings: ProviderSettings) -> None:
        super().__init__(settings)

    def calculate_cost(self, *, prompt_tokens: int, completion_tokens: int) -> float:
        return (prompt_tokens * 0.00015 + completion_tokens * 0.00060) / 1000

    async def generate(self, prompt: str, *, temperature: float = 0.0, seed: int | None = None) -> LLMResponse:
        if not self._settings.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for the OpenAI adapter")

        payload: dict[str, Any] = {
            "model": self._settings.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        if seed is not None:
            payload["seed"] = seed

        headers = {"Authorization": f"Bearer {self._settings.api_key}", "Content-Type": "application/json"}
        start = time.perf_counter()
        response = await self._request_json("POST", f"{self._settings.base_url}/chat/completions", headers=headers, json=payload)
        latency_seconds = time.perf_counter() - start
        message = response["choices"][0]["message"]["content"]
        usage = response.get("usage", {})
        prompt_tokens = int(usage.get("prompt_tokens", self.count_tokens(prompt)))
        completion_tokens = int(usage.get("completion_tokens", self.count_tokens(message)))
        return self._build_response(
            content=message,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_seconds=latency_seconds,
            raw_metadata={"raw": response},
        )
