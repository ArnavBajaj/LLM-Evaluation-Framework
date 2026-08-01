from fastapi import APIRouter, status

from app.schemas.catalog import ReportCreate
from app.services.catalog_store import store

router = APIRouter()


@router.get("/")
def list_reports() -> dict[str, list[dict[str, object]]]:
    return {"items": store.list_reports()}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_report(payload: ReportCreate) -> dict[str, object]:
    return store.create_report(payload.model_dump())
