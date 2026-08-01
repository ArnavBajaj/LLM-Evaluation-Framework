from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="API health check")
def api_health() -> dict[str, str]:
    return {"status": "ok"}
