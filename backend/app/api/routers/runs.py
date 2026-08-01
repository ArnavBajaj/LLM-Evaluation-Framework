from fastapi import APIRouter, status

from app.schemas.catalog import RunCreate
from app.services.catalog_store import store

router = APIRouter()


@router.get("/")
def list_runs() -> dict[str, list[dict[str, object]]]:
    return {"items": store.list_runs()}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_run(payload: RunCreate) -> dict[str, object]:
    return store.create_run(payload.model_dump())
