from app.evaluators.base import EvaluationResult, FailureCategory
from app.metrics.aggregator import AggregatedMetrics
from app.services.execution_engine import ExecutionOutcome
from app.workers.tasks import run_batch


def test_worker_batch_task_serializes_results(monkeypatch) -> None:
    fake_outcome = ExecutionOutcome(
        prompt_id="prompt-1",
        provider_name="openai",
        model_name="gpt-test",
        response=None,
        evaluator_results=[
            EvaluationResult(
                score=0.25,
                confidence=0.5,
                explanation="failed",
                failure_category=FailureCategory.hallucination,
            )
        ],
        metrics=AggregatedMetrics(
            average_score=0.25,
            hallucination_rate=1.0,
            unsafe_rate=0.0,
            average_latency_ms=10,
            average_cost_usd=0.0,
            pass_rate=0.0,
        ),
        attempts=1,
        error=None,
    )

    class FakeRunner:
        def run_batch_sync(self, provider_names, prompts):
            assert provider_names == ["openai"]
            assert prompts[0].prompt_id == "prompt-1"
            return [fake_outcome]

    monkeypatch.setattr("app.workers.tasks.EvaluationTaskRunner", lambda: FakeRunner())

    results = run_batch(["openai"], [{"prompt_id": "prompt-1", "prompt_text": "hello"}])

    assert results == [
        {
            "prompt_id": "prompt-1",
            "provider_name": "openai",
            "model_name": "gpt-test",
            "attempts": 1,
            "error": None,
            "metrics": {
                "average_score": 0.25,
                "hallucination_rate": 1.0,
                "unsafe_rate": 0.0,
                "average_latency_ms": 10,
                "average_cost_usd": 0.0,
                "pass_rate": 0.0,
            },
            "evaluations": [
                {
                    "score": 0.25,
                    "confidence": 0.5,
                    "explanation": "failed",
                    "failure_category": "Hallucination",
                }
            ],
        }
    ]
