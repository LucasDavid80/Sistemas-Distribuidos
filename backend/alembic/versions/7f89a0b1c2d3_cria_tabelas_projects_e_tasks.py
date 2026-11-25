"""cria tabelas projects e tasks

Revision ID: 7f89a0b1c2d3
Revises: de75d645dc30
Create Date: 2026-11-24 22:15:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7f89a0b1c2d3"
down_revision: str | Sequence[str] | None = "de75d645dc30"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column(
            "descricao", sa.String(length=500), nullable=False, server_default=""
        ),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=150), nullable=False),
        sa.Column(
            "descricao", sa.String(length=1000), nullable=False, server_default=""
        ),
        sa.Column(
            "prioridade", sa.String(length=20), nullable=False, server_default="MEDIA"
        ),
        sa.Column(
            "status", sa.String(length=20), nullable=False, server_default="PENDENTE"
        ),
        sa.Column(
            "categoria", sa.String(length=60), nullable=False, server_default="Geral"
        ),
        sa.Column("prazo", sa.DateTime(timezone=True), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "prioridade IN ('BAIXA', 'MEDIA', 'ALTA')",
            name="ck_tasks_prioridade_valid",
        ),
        sa.CheckConstraint(
            "status IN ('PENDENTE', 'EM_PROGRESSO', 'CONCLUIDA')",
            name="ck_tasks_status_valid",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("tasks")
    op.drop_table("projects")
