import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import TimestampedUUIDModel


class LangSmithTrace(TimestampedUUIDModel):
    __tablename__ = "langsmith_traces"

    run_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("run_items.id"), nullable=False)
    trace_id: Mapped[str] = mapped_column(String(255), nullable=False)
    trace_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    span_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
