from fastapi import APIRouter

from app.services.catalog_store import store

router = APIRouter()


@router.get("/")
def list_models() -> dict[str, list[dict[str, object]]]:
    return {"items": store.list_models()}
