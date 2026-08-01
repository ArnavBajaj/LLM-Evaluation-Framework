# Backend

FastAPI-based control plane and execution layer for the evaluation framework.

## Planned structure

- app/api: versioned routes and request/response schemas
- app/core: settings, logging, security, shared runtime concerns
- app/db: database base classes and session management
- app/models: SQLAlchemy models
- app/services: orchestration and domain services
- app/llm: provider abstraction and adapters
- app/evaluators: independent scoring modules
- app/metrics: aggregation and scoring normalization
- app/workers: Celery tasks and async execution
- app/reports: report generation
- app/auth: login and RBAC