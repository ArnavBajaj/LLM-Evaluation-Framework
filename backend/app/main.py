from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/healthz", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
