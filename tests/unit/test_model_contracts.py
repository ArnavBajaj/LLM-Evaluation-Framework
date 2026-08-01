from app.models.dataset import Dataset
from app.models.evaluation import EvaluationReport, EvaluationScore
from app.models.prompt import PromptTemplate
from app.models.provider import LLMModel, LLMProvider
from app.models.run import EvaluationRun, RunItem
from app.models.trace import LangSmithTrace


def test_model_tables_are_registered() -> None:
    tables = {
        Dataset.__tablename__,
        EvaluationReport.__tablename__,
        EvaluationRun.__tablename__,
        EvaluationScore.__tablename__,
        LangSmithTrace.__tablename__,
        LLMModel.__tablename__,
        LLMProvider.__tablename__,
        PromptTemplate.__tablename__,
        RunItem.__tablename__,
    }

    assert tables == {
        "datasets",
        "evaluation_reports",
        "evaluation_runs",
        "evaluation_scores",
        "langsmith_traces",
        "llm_models",
        "llm_providers",
        "prompt_templates",
        "run_items",
    }
