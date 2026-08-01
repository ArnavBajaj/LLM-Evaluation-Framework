from __future__ import annotations

import json
import re

from app.evaluators.base import BaseEvaluator, EvaluationResult, FailureCategory


_CODE_FENCE_PATTERN = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.IGNORECASE | re.DOTALL)


def _unwrap_code_fence(text: str) -> str:
    match = _CODE_FENCE_PATTERN.match(text.strip())
    if match is None:
        return text.strip()
    return match.group(1).strip()


class FormattingEvaluator(BaseEvaluator):
    def evaluate(self, prompt: str, response: str, *, context: dict[str, object] | None = None) -> EvaluationResult:
        del context
        response_text = response.strip()
        if not response_text:
            return EvaluationResult(
                score=0.0,
                confidence=1.0,
                explanation="Empty responses do not satisfy formatting constraints.",
                failure_category=FailureCategory.formatting_failure,
            )

        prompt_lower = prompt.lower()
        requires_json = "json" in prompt_lower or response_text.startswith("{") or response_text.startswith("[")
        candidate = _unwrap_code_fence(response_text)
        parsed_json = None
        if candidate.startswith("{") or candidate.startswith("["):
            try:
                parsed_json = json.loads(candidate)
            except json.JSONDecodeError:
                parsed_json = None

        if requires_json and parsed_json is None:
            return EvaluationResult(
                score=0.15,
                confidence=0.9,
                explanation="Response does not preserve JSON structure requested by the prompt.",
                failure_category=FailureCategory.formatting_failure,
            )

        if requires_json and parsed_json is not None:
            return EvaluationResult(
                score=0.95,
                confidence=0.95,
                explanation="Response is valid JSON and matches the requested structured format.",
                failure_category=None,
            )

        if response_text.startswith("```"):
            return EvaluationResult(
                score=0.75,
                confidence=0.7,
                explanation="Response uses a code fence and remains structurally readable.",
                failure_category=None,
            )

        return EvaluationResult(
            score=0.8,
            confidence=0.65,
            explanation="Response is plain text and does not show obvious formatting drift.",
            failure_category=None,
        )