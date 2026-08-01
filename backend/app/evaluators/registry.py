from __future__ import annotations

from app.evaluators.base import BaseEvaluator
from app.evaluators.bias.evaluator import BiasEvaluator
from app.evaluators.formatting.evaluator import FormattingEvaluator
from app.evaluators.hallucination.evaluator import HallucinationEvaluator
from app.evaluators.reasoning.evaluator import ReasoningEvaluator
from app.evaluators.toxicity.evaluator import ToxicityEvaluator


def build_default_evaluators() -> list[BaseEvaluator]:
    return [
        HallucinationEvaluator(),
        FormattingEvaluator(),
        ReasoningEvaluator(),
        BiasEvaluator(),
        ToxicityEvaluator(),
    ]