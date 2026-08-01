# Failure Taxonomy

This framework normalizes evaluation failures into canonical categories so that scores, reports, and regressions remain comparable across providers and prompt suites.

## Canonical Failure Categories

- Hallucination: model fabricates facts or unsupported claims.
- Unsafe Advice: model provides harmful operational guidance.
- Prompt Injection: model follows malicious instructions embedded in input/context.
- Jailbreak: model violates policy or safety constraints under adversarial prompting.
- Logical Error: response contains internal contradiction or invalid deduction.
- Reasoning Failure: model cannot solve a task that requires multi-step inference.
- Formatting Failure: output violates expected structure or schema.
- Toxic Output: response contains abusive, hateful, or harassing language.
- Bias: output exhibits unfair or discriminatory behavior.
- Refusal Failure: model fails to refuse when it should, or refuses when it should comply.

## Evaluator Output Contract

Each evaluator should return:

- score: normalized numeric result
- confidence: evaluator confidence estimate
- explanation: short human-readable justification
- failure_category: one of the canonical categories above or null

## Notes

- Multiple evaluators may map to the same failure category.
- A run item may have more than one failure category.
- The dashboard should aggregate both evaluator-level scores and category-level failure rates.