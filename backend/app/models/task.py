from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.user import User


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "prioridade IN ('BAIXA', 'MEDIA', 'ALTA')",
            name="ck_tasks_prioridade_valid",
        ),
        CheckConstraint(
            "status IN ('PENDENTE', 'EM_PROGRESSO', 'CONCLUIDA')",
            name="ck_tasks_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    prioridade: Mapped[str] = mapped_column(String(20), nullable=False, default="MEDIA")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDENTE")
    categoria: Mapped[str] = mapped_column(String(60), nullable=False, default="Geral")
    prazo: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    project: Mapped["Project | None"] = relationship(back_populates="tasks")
    user: Mapped["User"] = relationship(back_populates="tasks")
