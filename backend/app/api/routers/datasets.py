from fastapi import APIRouter, status

from app.schemas.catalog import DatasetCreate
from app.services.catalog_store import store

router = APIRouter()


@router.get("/")
def list_datasets() -> dict[str, list[dict[str, object]]]:
    return {"items": store.list_datasets()}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_dataset(payload: DatasetCreate) -> dict[str, object]:
    return store.create_dataset(payload.model_dump())
