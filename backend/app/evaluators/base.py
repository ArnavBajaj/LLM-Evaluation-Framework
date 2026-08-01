from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class FailureCategory(str, Enum):
    hallucination = "Hallucination"
    unsafe_advice = "Unsafe Advice"
    prompt_injection = "Prompt Injection"
    jailbreak = "Jailbreak"
    logical_error = "Logical Error"
    reasoning_failure = "Reasoning Failure"
    formatting_failure = "Formatting Failure"
    toxic_output = "Toxic Output"
    bias = "Bias"
    refusal_failure = "Refusal Failure"


@dataclass(slots=True)
class EvaluationResult:
    score: float
    confidence: float
    explanation: str
    failure_category: FailureCategory | None


class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self, prompt: str, response: str, *, context: dict[str, object] | None = None) -> EvaluationResult:
        raise NotImplementedError
