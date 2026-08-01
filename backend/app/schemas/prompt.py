from pydantic import BaseModel, Field


class PromptTemplateCreate(BaseModel):
    title: str
    category: str
    difficulty: str
    tags: list[str] = Field(default_factory=list)
    prompt_text: str
    expected_answer: str | None = None
    ground_truth: dict | None = None
    dataset_source: str | None = None
    version: str = "v1"
