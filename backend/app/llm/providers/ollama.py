from __future__ import annotations

import time

from app.llm.base import LLMResponse
from app.llm.providers.common import HTTPProviderBase, ProviderSettings


class OllamaLLM(HTTPProviderBase):
    def __init__(self, settings: ProviderSettings) -> None:
        super().__init__(settings)

    def calculate_cost(self, *, prompt_tokens: int, completion_tokens: int) -> float:
        del prompt_tokens, completion_tokens
        return 0.0

    async def generate(self, prompt: str, *, temperature: float = 0.0, seed: int | None = None) -> LLMResponse:
        payload = {
            "model": self._settings.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": temperature},
        }
        if seed is not None:
            payload["options"]["seed"] = seed

        start = time.perf_counter()
        response = await self._request_json("POST", f"{self._settings.base_url}/api/chat", json=payload)
        latency_seconds = time.perf_counter() - start
        message = response.get("message", {}).get("content", "")
        prompt_tokens = int(response.get("prompt_eval_count", self.count_tokens(prompt)))
        completion_tokens = int(response.get("eval_count", self.count_tokens(message)))
        return self._build_response(
            content=message,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_seconds=latency_seconds,
            raw_metadata={"raw": response},
        )
