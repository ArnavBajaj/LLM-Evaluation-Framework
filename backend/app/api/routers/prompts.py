from fastapi import APIRouter, status

from app.schemas.catalog import PromptCreate
from app.services.catalog_store import store

router = APIRouter()


@router.get("/")
def list_prompts() -> dict[str, list[dict[str, object]]]:
    return {"items": store.list_prompts()}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_prompt(payload: PromptCreate) -> dict[str, object]:
    return store.create_prompt(payload.model_dump())
