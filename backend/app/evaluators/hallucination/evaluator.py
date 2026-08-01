from __future__ import annotations

import re
from collections.abc import Iterable

from app.evaluators.base import BaseEvaluator, EvaluationResult, FailureCategory


_TOKEN_PATTERN = re.compile(r"[a-z0-9']+")
_CITATION_PATTERN = re.compile(r"\b(?:https?://|www\.|source|sources|citation|cite|according to)\b", re.IGNORECASE)
_HEDGING_PATTERN = re.compile(r"\b(?:i (?:cannot|can't|don't know|am not sure)|unsure|not enough information|cannot verify)\b", re.IGNORECASE)


def _tokenize(text: str) -> set[str]:
    return {
        token
        for token in _TOKEN_PATTERN.findall(text.lower())
        if len(token) > 2 and token not in {"the", "and", "for", "with", "that", "this", "from", "are", "was", "were", "have", "has", "had"}
    }


def _flatten_context_values(value: object) -> Iterable[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        pieces: list[str] = []
        for item in value.values():
            pieces.extend(_flatten_context_values(item))
        return pieces
    if isinstance(value, Iterable):
        pieces = []
        for item in value:
            pieces.extend(_flatten_context_values(item))
        return pieces
    return [str(value)]


def _collect_evidence(prompt: str, context: dict[str, object] | None) -> set[str]:
    evidence_tokens = _tokenize(prompt)
    if not context:
        return evidence_tokens

    for key in ("ground_truth", "expected_answer", "reference_text", "retrieved_context", "sources", "evidence", "context"):
        evidence_tokens.update(_tokenize(str(context.get(key, ""))))

    for key in ("ground_truth", "expected_answer", "reference_text", "retrieved_context", "sources", "evidence", "context"):
        evidence_tokens.update(_tokenize(" ".join(_flatten_context_values(context.get(key)))))

    return evidence_tokens


class HallucinationEvaluator(BaseEvaluator):
    def evaluate(self, prompt: str, response: str, *, context: dict[str, object] | None = None) -> EvaluationResult:
        response_text = response.strip()
        if not response_text:
            return EvaluationResult(
                score=0.0,
                confidence=1.0,
                explanation="Empty responses cannot be supported by evidence and are treated as hallucination failures.",
                failure_category=FailureCategory.hallucination,
            )

        response_tokens = _tokenize(response_text)
        evidence_tokens = _collect_evidence(prompt, context)
        unsupported_tokens = response_tokens - evidence_tokens

        if response_tokens:
            supported_ratio = 1.0 - (len(unsupported_tokens) / len(response_tokens))
        else:
            supported_ratio = 0.0

        citation_bonus = 0.08 if _CITATION_PATTERN.search(response_text) else 0.0
        hedging_bonus = 0.06 if _HEDGING_PATTERN.search(response_text) else 0.0
        evidence_bonus = 0.12 if evidence_tokens else 0.0
        score = max(0.0, min(1.0, 0.1 + (supported_ratio * 0.72) + citation_bonus + hedging_bonus + evidence_bonus))

        confidence = max(0.2, min(1.0, 0.35 + min(len(evidence_tokens), 40) / 80 + (0.15 if context else 0.0)))
        unsupported_preview = ", ".join(sorted(unsupported_tokens)[:4]) or "none"
        if score < 0.6:
            explanation = (
                "Response contains unsupported claims relative to the prompt/evidence context; "
                f"sample unsupported terms: {unsupported_preview}."
            )
            failure_category = FailureCategory.hallucination
        else:
            explanation = "Response remains broadly aligned with the available prompt/evidence context."
            failure_category = None

        return EvaluationResult(
            score=score,
            confidence=confidence,
            explanation=explanation,
            failure_category=failure_category,
        )
