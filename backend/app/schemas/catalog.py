from pydantic import BaseModel, Field


class PromptCreate(BaseModel):
    title: str
    category: str
    difficulty: str
    tags: list[str] = Field(default_factory=list)
    prompt_text: str
    expected_answer: str | None = None
    ground_truth: dict | None = None
    dataset_source: str | None = None
    version: str = "v1"


class DatasetCreate(BaseModel):
    name: str
    version: str
    source: str | None = None
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    ground_truth: dict | None = None


class RunCreate(BaseModel):
    model: str
    provider: str
    prompt_version: str
    dataset_version: str
    temperature: float = 0.0
    seed: int | None = None
    status: str = "queued"
    average_score: float | None = None
    cost_usd: float | None = None
    latency_ms: int | None = None
    failure_category: str | None = None


class ReportCreate(BaseModel):
    run_id: str
    report_format: str
    storage_path: str
    summary: dict | None = None
