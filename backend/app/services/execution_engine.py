from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Sequence

from app.evaluators.base import BaseEvaluator, EvaluationResult
from app.llm.base import BaseLLM, LLMResponse
from app.llm.factory import LLMFactory
from app.metrics.aggregator import AggregatedMetrics, MetricsAggregator


@dataclass(slots=True)
class PromptInput:
    prompt_id: str
    prompt_text: str
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutionOutcome:
    prompt_id: str
    provider_name: str
    model_name: str | None
    response: LLMResponse | None
    evaluator_results: list[EvaluationResult]
    metrics: AggregatedMetrics | None
    attempts: int
    error: str | None = None


class EvaluationEngine:
    def __init__(
        self,
        llm_factory: LLMFactory,
        evaluators: Sequence[BaseEvaluator],
        metrics_aggregator: MetricsAggregator,
        *,
        max_concurrency: int = 8,
        max_retries: int = 2,
        retry_backoff_seconds: float = 0.25,
    ) -> None:
        self._llm_factory = llm_factory
        self._evaluators = list(evaluators)
        self._metrics_aggregator = metrics_aggregator
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._max_retries = max_retries
        self._retry_backoff_seconds = retry_backoff_seconds

    async def evaluate_prompt(
        self,
        *,
        provider_name: str,
        prompt: PromptInput,
        temperature: float = 0.0,
        seed: int | None = None,
        context: dict[str, object] | None = None,
    ) -> ExecutionOutcome:
        llm = self._llm_factory.get(provider_name)
        response, attempts, error = await self._generate_with_retry(llm, prompt.prompt_text, temperature=temperature, seed=seed)
        if response is None:
            return ExecutionOutcome(
                prompt_id=prompt.prompt_id,
                provider_name=provider_name,
                model_name=None,
                response=None,
                evaluator_results=[],
                metrics=None,
                attempts=attempts,
                error=error,
            )

        evaluator_results = [self._safe_evaluate(evaluator, prompt.prompt_text, response.content, context=context) for evaluator in self._evaluators]
        scores = [result.score for result in evaluator_results]
        latency_ms = [response.latency_ms]
        costs = [response.cost_usd]
        metrics = self._metrics_aggregator.aggregate(scores, latency_ms, costs, evaluator_results)
        return ExecutionOutcome(
            prompt_id=prompt.prompt_id,
            provider_name=response.provider_name,
            model_name=response.model_name,
            response=response,
            evaluator_results=evaluator_results,
            metrics=metrics,
            attempts=attempts,
        )

    async def evaluate_batch(
        self,
        *,
        provider_names: Sequence[str],
        prompts: Sequence[PromptInput],
        temperature: float = 0.0,
        seed: int | None = None,
        context: dict[str, object] | None = None,
    ) -> list[ExecutionOutcome]:
        tasks = [
            self.evaluate_prompt(provider_name=provider_name, prompt=prompt, temperature=temperature, seed=seed, context=context)
            for provider_name in provider_names
            for prompt in prompts
        ]
        return await asyncio.gather(*tasks)

    async def _generate_with_retry(
        self,
        llm: BaseLLM,
        prompt_text: str,
        *,
        temperature: float,
        seed: int | None,
    ) -> tuple[LLMResponse | None, int, str | None]:
        attempts = 0
        last_error: str | None = None
        while attempts <= self._max_retries:
            attempts += 1
            try:
                async with self._semaphore:
                    response = await llm.generate(prompt_text, temperature=temperature, seed=seed)
                return response, attempts, None
            except Exception as exc:  # pragma: no cover - exercised through retry tests
                last_error = str(exc)
                if attempts > self._max_retries:
                    break
                await asyncio.sleep(self._retry_backoff_seconds * attempts)
        return None, attempts, last_error

    def _safe_evaluate(
        self,
        evaluator: BaseEvaluator,
        prompt_text: str,
        response_text: str,
        *,
        context: dict[str, object] | None,
    ) -> EvaluationResult:
        try:
            return evaluator.evaluate(prompt_text, response_text, context=context)
        except Exception as exc:  # pragma: no cover - defensive path for evaluator failures
            return EvaluationResult(
                score=0.0,
                confidence=0.0,
                explanation=f"Evaluator {evaluator.__class__.__name__} failed: {exc}",
                failure_category=None,
            )
