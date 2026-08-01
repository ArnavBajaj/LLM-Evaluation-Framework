from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass

from celery import Celery

from app.core.config import settings
from app.evaluators.base import EvaluationResult
from app.evaluators.registry import build_default_evaluators
from app.llm.registry import build_default_factory
from app.metrics.aggregator import MetricsAggregator
from app.services.execution_engine import EvaluationEngine, PromptInput


celery_app = Celery("llm_eval_framework", broker=settings.redis_url, backend=settings.redis_url)


@dataclass(slots=True)
class WorkerConfig:
    max_concurrency: int = 8
    max_retries: int = 2


class EvaluationTaskRunner:
    def __init__(self, worker_config: WorkerConfig | None = None) -> None:
        self._worker_config = worker_config or WorkerConfig()
        self._factory = build_default_factory()
        self._evaluators = build_default_evaluators()
        self._hallucination_evaluator = self._evaluators[0]
        self._metrics_aggregator = MetricsAggregator()
        self._engine = EvaluationEngine(
            self._factory,
            self._evaluators,
            self._metrics_aggregator,
            max_concurrency=self._worker_config.max_concurrency,
            max_retries=self._worker_config.max_retries,
        )

    async def run_batch(self, provider_names: list[str], prompts: list[PromptInput]) -> list[object]:
        return await self._engine.evaluate_batch(provider_names=provider_names, prompts=prompts)

    def run_batch_sync(self, provider_names: list[str], prompts: list[PromptInput]) -> list[object]:
        return asyncio.run(self.run_batch(provider_names, prompts))

    def run_single(self, prompt: str, response: str) -> dict[str, object]:
        results = [evaluator.evaluate(prompt, response) for evaluator in self._evaluators]
        metrics = self._metrics_aggregator.aggregate([result.score for result in results], [0], [0.0], results)
        return {"evaluation": results[0], "evaluations": results, "metrics": metrics}


@celery_app.task(name="evaluation.run_batch")
def run_batch(provider_names: list[str], prompts: list[dict[str, object]]) -> list[dict[str, object]]:
    runner = EvaluationTaskRunner()
    prompt_inputs = [PromptInput(prompt_id=str(item["prompt_id"]), prompt_text=str(item["prompt_text"]), metadata=dict(item.get("metadata", {}))) for item in prompts]
    results = runner.run_batch_sync(provider_names, prompt_inputs)
    return [
        {
            "prompt_id": outcome.prompt_id,
            "provider_name": outcome.provider_name,
            "model_name": outcome.model_name,
            "attempts": outcome.attempts,
            "error": outcome.error,
            "evaluations": [
                {
                    "score": evaluation.score,
                    "confidence": evaluation.confidence,
                    "explanation": evaluation.explanation,
                    "failure_category": None if evaluation.failure_category is None else evaluation.failure_category.value,
                }
                for evaluation in outcome.evaluator_results
            ],
            "metrics": None if outcome.metrics is None else asdict(outcome.metrics),
        }
        for outcome in results
    ]
