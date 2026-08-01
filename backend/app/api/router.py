from fastapi import APIRouter

from app.api.routers import datasets, health, metrics, models, prompts, reports, runs

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
