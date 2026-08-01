import asyncio

import pytest

from app.evaluators.base import BaseEvaluator, EvaluationResult, FailureCategory
from app.llm.base import BaseLLM, LLMResponse
from app.llm.factory import LLMFactory
from app.metrics.aggregator import AggregatedMetrics, MetricsAggregator
from app.services.execution_engine import EvaluationEngine, PromptInput


class FlakyLLM(BaseLLM):
    def __init__(self) -> None:
        self.calls = 0

    async def generate(self, prompt: str, *, temperature: float = 0.0, seed: int | None = None) -> LLMResponse:
        del temperature, seed
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("temporary provider failure")
        return LLMResponse(
            provider_name="openai",
            model_name="gpt-test",
            content=f"response to {prompt}",
            prompt_tokens=10,
            completion_tokens=4,
            total_tokens=14,
            cost_usd=0.02,
            latency_ms=12,
            raw_metadata={},
        )

    def count_tokens(self, text: str) -> int:
        return len(text.split())

    def calculate_cost(self, *, prompt_tokens: int, completion_tokens: int) -> float:
        return 0.0

    def provider_name(self) -> str:
        return "openai"


class RecordingEvaluator(BaseEvaluator):
    def evaluate(self, prompt: str, response: str, *, context: dict[str, object] | None = None) -> EvaluationResult:
        assert context == {"dataset": "bench"}
        return EvaluationResult(
            score=0.9,
            confidence=0.8,
            explanation=f"prompt={prompt} response={response}",
            failure_category=FailureCategory.hallucination,
        )


class TrackingLLM(BaseLLM):
    def __init__(self) -> None:
        self.active_calls = 0
        self.max_active_calls = 0

    async def generate(self, prompt: str, *, temperature: float = 0.0, seed: int | None = None) -> LLMResponse:
        del temperature, seed
        self.active_calls += 1
        self.max_active_calls = max(self.max_active_calls, self.active_calls)
        await asyncio.sleep(0)
        self.active_calls -= 1
        return LLMResponse(
            provider_name="openai",
            model_name="gpt-test",
            content=f"ok:{prompt}",
            prompt_tokens=1,
            completion_tokens=1,
            total_tokens=2,
            cost_usd=0.01,
            latency_ms=5,
            raw_metadata={},
        )

    def count_tokens(self, text: str) -> int:
        return len(text.split())

    def calculate_cost(self, *, prompt_tokens: int, completion_tokens: int) -> float:
        return 0.0

    def provider_name(self) -> str:
        return "openai"


@pytest.mark.asyncio
async def test_engine_retries_and_aggregates_results() -> None:
    llm = FlakyLLM()
    factory = LLMFactory({"openai": llm})
    engine = EvaluationEngine(factory, [RecordingEvaluator()], MetricsAggregator(), max_retries=1, retry_backoff_seconds=0)

    outcome = await engine.evaluate_prompt(
        provider_name="openai",
        prompt=PromptInput(prompt_id="prompt-1", prompt_text="Explain the model"),
        context={"dataset": "bench"},
    )

    assert outcome.error is None
    assert outcome.attempts == 2
    assert outcome.response is not None
    assert outcome.response.content == "response to Explain the model"
    assert outcome.metrics == AggregatedMetrics(
        average_score=0.9,
        hallucination_rate=1.0,
        unsafe_rate=0.0,
        average_latency_ms=12,
        average_cost_usd=0.02,
        pass_rate=1.0,
    )
    assert outcome.evaluator_results[0].failure_category == FailureCategory.hallucination


@pytest.mark.asyncio
async def test_engine_runs_prompts_in_parallel() -> None:
    llm = TrackingLLM()
    factory = LLMFactory({"openai": llm})
    engine = EvaluationEngine(factory, [], MetricsAggregator(), max_concurrency=2, max_retries=0)

    outcomes = await engine.evaluate_batch(
        provider_names=["openai"],
        prompts=[
            PromptInput(prompt_id="p1", prompt_text="first"),
            PromptInput(prompt_id="p2", prompt_text="second"),
        ],
    )

    assert len(outcomes) == 2
    assert llm.max_active_calls == 2
    assert all(outcome.metrics is not None for outcome in outcomes)
