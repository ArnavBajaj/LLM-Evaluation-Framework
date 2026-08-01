from app.evaluators.base import EvaluationResult, FailureCategory
from app.metrics.aggregator import AggregatedMetrics, MetricsAggregator


def test_metrics_aggregator_computes_expected_values() -> None:
    aggregator = MetricsAggregator()
    metrics = aggregator.aggregate(
        [0.5, 1.0],
        [10, 30],
        [0.01, 0.03],
        [
            EvaluationResult(score=0.5, confidence=0.7, explanation="hallucination", failure_category=FailureCategory.hallucination),
            EvaluationResult(score=1.0, confidence=0.8, explanation="pass", failure_category=None),
        ],
    )

    assert metrics == AggregatedMetrics(
        average_score=0.75,
        hallucination_rate=0.5,
        unsafe_rate=0.0,
        average_latency_ms=20.0,
        average_cost_usd=0.02,
        pass_rate=0.5,
    )
