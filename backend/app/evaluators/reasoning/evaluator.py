from __future__ import annotations

from app.evaluators.base import BaseEvaluator, EvaluationResult, FailureCategory
from app.evaluators.utils import text_from_context, tokenize


_REASONING_PROMPTS = ("why", "explain", "reason", "because", "step", "calculate", "compare", "prove", "logic")
_REASONING_MARKERS = ("because", "therefore", "thus", "since", "first", "second", "next", "consequently", "hence")


class ReasoningEvaluator(BaseEvaluator):
    def evaluate(self, prompt: str, response: str, *, context: dict[str, object] | None = None) -> EvaluationResult:
        response_text = response.strip()
        if not response_text:
            return EvaluationResult(
                score=0.0,
                confidence=1.0,
                explanation="Empty responses cannot demonstrate reasoning.",
                failure_category=FailureCategory.reasoning_failure,
            )

        prompt_lower = prompt.lower()
        needs_reasoning = any(marker in prompt_lower for marker in _REASONING_PROMPTS)
        response_lower = response_text.lower()
        response_tokens = tokenize(response_text)
        marker_count = sum(1 for marker in _REASONING_MARKERS if marker in response_lower)

        expected_answer = text_from_context(context, ("expected_answer", "reference_text", "ground_truth", "solution"))
        overlap_ratio = 0.0
        if expected_answer:
            expected_tokens = tokenize(expected_answer)
            overlap_ratio = len(response_tokens & expected_tokens) / max(len(expected_tokens), 1)

        score = max(0.0, min(1.0, 0.35 + (marker_count * 0.12) + (overlap_ratio * 0.45)))
        confidence = 0.45 + (0.2 if needs_reasoning else 0.0) + (0.1 if expected_answer else 0.0)
        confidence = min(confidence, 1.0)

        if needs_reasoning and (score < 0.6 or len(response_tokens) < 12):
            return EvaluationResult(
                score=score,
                confidence=confidence,
                explanation="Response is too terse or lacks visible reasoning structure for the requested task.",
                failure_category=FailureCategory.reasoning_failure,
            )

        return EvaluationResult(
            score=max(score, 0.7),
            confidence=confidence,
            explanation="Response shows acceptable reasoning cues for the requested task.",
            failure_category=None,
        )