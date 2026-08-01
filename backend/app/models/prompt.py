from sqlalchemy import JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common import TimestampedUUIDModel


class PromptTemplate(TimestampedUUIDModel):
    __tablename__ = "prompt_templates"
    __table_args__ = (UniqueConstraint("title", "version", name="uq_prompt_templates_title_version"),)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    expected_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    ground_truth: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    dataset_source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1")
