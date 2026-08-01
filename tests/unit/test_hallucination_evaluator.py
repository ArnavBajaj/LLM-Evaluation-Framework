from app.evaluators.base import FailureCategory
from app.evaluators.hallucination.evaluator import HallucinationEvaluator


def test_hallucination_evaluator_flags_unsupported_response() -> None:
    evaluator = HallucinationEvaluator()
    result = evaluator.evaluate(
        "What is X?",
        "Fabricated answer",
        context={"reference_text": "X is a constrained benchmark term that should be answered from evidence."},
    )

    assert result.score < 0.6
    assert result.confidence > 0.5
    assert result.failure_category == FailureCategory.hallucination


def test_hallucination_evaluator_accepts_supported_response() -> None:
    evaluator = HallucinationEvaluator()
    result = evaluator.evaluate(
        "Summarize the evidence.",
        "The evidence says the model performed well and stayed within the expected scope.",
        context={"reference_text": "The evidence says the model performed well and stayed within the expected scope."},
    )

    assert result.score >= 0.6
    assert result.failure_category is None
