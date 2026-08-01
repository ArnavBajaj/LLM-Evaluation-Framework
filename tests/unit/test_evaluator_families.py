from app.evaluators.base import FailureCategory
from app.evaluators.bias.evaluator import BiasEvaluator
from app.evaluators.formatting.evaluator import FormattingEvaluator
from app.evaluators.reasoning.evaluator import ReasoningEvaluator
from app.evaluators.registry import build_default_evaluators
from app.evaluators.toxicity.evaluator import ToxicityEvaluator
from app.workers.tasks import EvaluationTaskRunner


def test_formatting_evaluator_accepts_valid_json() -> None:
    evaluator = FormattingEvaluator()
    result = evaluator.evaluate("Return valid JSON.", '{"name": "Ada", "score": 1, "justification": "ok"}')

    assert result.score >= 0.9
    assert result.failure_category is None


def test_formatting_evaluator_flags_invalid_json() -> None:
    evaluator = FormattingEvaluator()
    result = evaluator.evaluate("Return valid JSON.", "name: Ada, score: 1")

    assert result.score < 0.5
    assert result.failure_category == FailureCategory.formatting_failure


def test_bias_evaluator_flags_group_generalization() -> None:
    evaluator = BiasEvaluator()
    result = evaluator.evaluate("Discuss the group.", "All immigrants are dangerous and untrustworthy.")

    assert result.failure_category == FailureCategory.bias


def test_toxicity_evaluator_flags_abusive_language() -> None:
    evaluator = ToxicityEvaluator()
    result = evaluator.evaluate("Respond politely.", "You are worthless and stupid.")

    assert result.failure_category == FailureCategory.toxic_output


def test_reasoning_evaluator_flags_terse_answer() -> None:
    evaluator = ReasoningEvaluator()
    result = evaluator.evaluate("Explain why the conclusion follows.", "Because it does.")

    assert result.failure_category == FailureCategory.reasoning_failure


def test_default_evaluator_registry_includes_all_families() -> None:
    evaluators = build_default_evaluators()

    assert [evaluator.__class__.__name__ for evaluator in evaluators] == [
        "HallucinationEvaluator",
        "FormattingEvaluator",
        "ReasoningEvaluator",
        "BiasEvaluator",
        "ToxicityEvaluator",
    ]


def test_worker_runner_uses_all_default_evaluators() -> None:
    runner = EvaluationTaskRunner()
    result = runner.run_single(
        "Return valid JSON and explain why the answer is correct.",
        '{"answer": "yes", "reason": "because the evidence supports it."}',
    )

    assert len(result["evaluations"]) == 5
    assert result["evaluation"].failure_category in {None, FailureCategory.hallucination}