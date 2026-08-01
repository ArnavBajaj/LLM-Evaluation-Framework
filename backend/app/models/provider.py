import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import TimestampedUUIDModel


class LLMProvider(TimestampedUUIDModel):
    __tablename__ = "llm_providers"
    __table_args__ = (UniqueConstraint("name", name="uq_llm_providers_name"),)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    base_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    auth_header_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    docs_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)


class LLMModel(TimestampedUUIDModel):
    __tablename__ = "llm_models"
    __table_args__ = (UniqueConstraint("provider_id", "name", name="uq_llm_models_provider_name"),)

    provider_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("llm_providers.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    context_window: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pricing: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    capabilities: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
