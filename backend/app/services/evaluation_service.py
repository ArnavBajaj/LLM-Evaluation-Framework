from __future__ import annotations

from app.evaluators.base import BaseEvaluator
from app.llm.base import BaseLLM
from app.metrics.aggregator import MetricsAggregator


class EvaluationService:
    def __init__(self, llm: BaseLLM, evaluators: list[BaseEvaluator], metrics_aggregator: MetricsAggregator) -> None:
        self._llm = llm
        self._evaluators = evaluators
        self._metrics_aggregator = metrics_aggregator

    async def evaluate_prompt(self, prompt: str, *, context: dict[str, object] | None = None) -> dict[str, object]:
        response = await self._llm.generate(prompt)
        results = [evaluator.evaluate(prompt, response.content, context=context) for evaluator in self._evaluators]
        metrics = self._metrics_aggregator.aggregate(
            [result.score for result in results],
            [response.latency_ms],
            [response.cost_usd],
            results,
        )
        return {"response": response, "results": results, "metrics": metrics}
