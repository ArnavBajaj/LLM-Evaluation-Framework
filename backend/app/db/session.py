from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def _build_engine(database_url: str):
    engine_kwargs = {"pool_pre_ping": True}
    if database_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(database_url, **engine_kwargs)


def _sqlite_fallback_url() -> str:
    database_path = Path(__file__).resolve().parents[3] / "llm_eval.db"
    return f"sqlite:///{database_path}"


@lru_cache
def get_engine():
    primary_engine = _build_engine(settings.database_url)
    try:
        with primary_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return primary_engine
    except SQLAlchemyError:
        return _build_engine(_sqlite_fallback_url())


@lru_cache
def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, expire_on_commit=False)


def get_db():
    db = get_session_factory()()
    try:
        yield db
    finally:
        db.close()
