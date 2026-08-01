from pydantic import BaseModel


class EvaluationRunCreate(BaseModel):
    model_name: str
    provider_name: str
    prompt_version: str
    dataset_version: str
    temperature: float = 0.0
    seed: int | None = None
    metadata: dict | None = None
