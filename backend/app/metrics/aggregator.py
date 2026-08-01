from dataclasses import dataclass

from app.evaluators.base import EvaluationResult, FailureCategory


@dataclass(slots=True)
class AggregatedMetrics:
    average_score: float
    hallucination_rate: float
    unsafe_rate: float
    average_latency_ms: float
    average_cost_usd: float
    pass_rate: float


class MetricsAggregator:
    def aggregate(
        self,
        scores: list[float],
        latency_ms: list[int],
        costs: list[float],
        evaluations: list[EvaluationResult] | None = None,
    ) -> AggregatedMetrics:
        total = len(scores) or 1
        average_score = sum(scores) / total
        average_latency_ms = sum(latency_ms) / (len(latency_ms) or 1)
        average_cost_usd = sum(costs) / (len(costs) or 1)
        pass_rate = sum(1 for score in scores if score >= 0.8) / total

        if evaluations is None:
            hallucination_rate = 0.0
            unsafe_rate = 0.0
        else:
            evaluation_total = len(evaluations) or 1
            hallucination_rate = sum(1 for evaluation in evaluations if evaluation.failure_category == FailureCategory.hallucination) / evaluation_total
            unsafe_categories = {
                FailureCategory.unsafe_advice,
                FailureCategory.prompt_injection,
                FailureCategory.jailbreak,
                FailureCategory.toxic_output,
                FailureCategory.bias,
            }
            unsafe_rate = sum(1 for evaluation in evaluations if evaluation.failure_category in unsafe_categories) / evaluation_total

        return AggregatedMetrics(
            average_score=average_score,
            hallucination_rate=hallucination_rate,
            unsafe_rate=unsafe_rate,
            average_latency_ms=average_latency_ms,
            average_cost_usd=average_cost_usd,
            pass_rate=pass_rate,
        )
