from __future__ import annotations

import time

from app.llm.base import LLMResponse
from app.llm.providers.common import HTTPProviderBase, ProviderSettings


class GeminiLLM(HTTPProviderBase):
    def __init__(self, settings: ProviderSettings) -> None:
        super().__init__(settings)

    def calculate_cost(self, *, prompt_tokens: int, completion_tokens: int) -> float:
        return (prompt_tokens * 0.00035 + completion_tokens * 0.00105) / 1000

    async def generate(self, prompt: str, *, temperature: float = 0.0, seed: int | None = None) -> LLMResponse:
        if not self._settings.api_key:
            raise RuntimeError("GOOGLE_API_KEY is required for the Gemini adapter")

        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": temperature},
        }
        if seed is not None:
            payload["generationConfig"]["seed"] = seed

        start = time.perf_counter()
        response = await self._request_json(
            "POST",
            f"{self._settings.base_url}/v1beta/models/{self._settings.model_name}:generateContent?key={self._settings.api_key}",
            json=payload,
        )
        latency_seconds = time.perf_counter() - start
        candidates = response.get("candidates", [])
        content_parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
        content = "".join(part.get("text", "") for part in content_parts)
        usage = response.get("usageMetadata", {})
        prompt_tokens = int(usage.get("promptTokenCount", self.count_tokens(prompt)))
        completion_tokens = int(usage.get("candidatesTokenCount", self.count_tokens(content)))
        return self._build_response(
            content=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_seconds=latency_seconds,
            raw_metadata={"raw": response},
        )
