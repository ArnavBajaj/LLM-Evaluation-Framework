# LLM Evaluation Framework

Production-grade LLM evaluation and red-teaming platform for comparing providers, running adversarial prompt suites, tracking regressions, and generating auditable experiment reports.

## Current State

This repository now contains a working architecture, backend scaffold, evaluation engine, dashboard shell, container setup, and a passing test suite.

## What Has Been Built

- FastAPI backend with versioned routers and core runtime configuration
- SQLAlchemy models and Alembic migration for prompts, datasets, runs, scores, traces, providers, and models
- Multi-provider LLM adapter layer for OpenAI, Anthropic, Gemini, Mistral, and Ollama
- Execution engine with retries, concurrency control, evaluator fan-out, and metrics aggregation
- Report generation for Markdown, HTML, CSV, and PDF artifacts
- React + TypeScript dashboard with leaderboard, failure explorer, filters, and charts
- Dockerized local stack with PostgreSQL, Redis, backend, worker, and frontend services
- Backend and frontend tests, including API contracts and regression fixtures

## Tech Direction

- Backend: Python + FastAPI
- Frontend: React + TypeScript
- Database: PostgreSQL
- Queue: Celery + Redis
- ORM: SQLAlchemy
- Evaluation: DeepEval, Ragas, OpenAI Evals, LangSmith
- Visualization: Plotly, Chart.js
- Deployment: Docker + Docker Compose

## Next Step

Review [docs/ACHIEVEMENTS.md](docs/ACHIEVEMENTS.md) for the current delivery status, then continue with provider telemetry hardening and production deployment work.