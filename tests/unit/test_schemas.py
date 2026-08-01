import json
from pathlib import Path

from app.schemas.prompt import PromptTemplateCreate
from app.schemas.run import EvaluationRunCreate


def test_prompt_template_schema_defaults_and_payload_alignment() -> None:
    root = Path(__file__).resolve().parents[1]
    payload = json.loads((root / "fixtures" / "prompt_template.json").read_text())

    schema = PromptTemplateCreate(**payload)

    assert schema.tags == ["jailbreak", "policy"]
    assert schema.version == "v3"
    assert schema.expected_answer == "Refuse and explain policy boundaries."


def test_evaluation_run_schema_defaults_and_payload_alignment() -> None:
    root = Path(__file__).resolve().parents[1]
    payload = json.loads((root / "fixtures" / "evaluation_run.json").read_text())

    schema = EvaluationRunCreate(**payload)

    assert schema.model_name == "gpt-5"
    assert schema.provider_name == "openai"
    assert schema.temperature == 0.2
    assert schema.seed == 42
    assert schema.metadata == {"suite": "regression", "owner": "platform"}
