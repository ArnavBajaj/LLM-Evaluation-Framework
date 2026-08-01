from fastapi import APIRouter

from app.services.catalog_store import store

router = APIRouter()


@router.get("/")
def get_metrics() -> dict[str, object]:
    return store.summary_metrics()
