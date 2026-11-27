from __future__ import annotations

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.task import Task


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, task: Task) -> Task:
        self.session.add(task)
        self.session.flush()
        return task

    def get(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def list(
        self,
        status: str | None = None,
        prioridade: str | None = None,
        search: str | None = None,
        user_id: int | None = None,
    ) -> list[Task]:
        statement = select(Task)
        if user_id is not None:
            statement = statement.where(Task.user_id == user_id)
        if status:
            statement = statement.where(Task.status == status)
        if prioridade:
            statement = statement.where(Task.prioridade == prioridade)
        if search:
            like_expr = f"%{search}%"
            statement = statement.where(
                or_(
                    Task.titulo.ilike(like_expr),
                    Task.descricao.ilike(like_expr),
                    Task.categoria.ilike(like_expr),
                )
            )
        statement = statement.order_by(Task.id.desc())
        return list(self.session.scalars(statement))

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.flush()

    def get_metrics(self, user_id: int | None = None) -> dict[str, int | float]:
        base_query = select(Task.status, func.count(Task.id)).group_by(Task.status)
        if user_id is not None:
            base_query = base_query.where(Task.user_id == user_id)

        rows = self.session.execute(base_query).all()
        status_counts = {status: count for status, count in rows}

        pendentes = status_counts.get("PENDENTE", 0)
        em_progresso = status_counts.get("EM_PROGRESSO", 0)
        concluidas = status_counts.get("CONCLUIDA", 0)
        total = pendentes + em_progresso + concluidas

        taxa_conclusao = round((concluidas / total * 100), 1) if total > 0 else 0.0

        return {
            "total": total,
            "pendentes": pendentes,
            "em_progresso": em_progresso,
            "concluidas": concluidas,
            "taxa_conclusao": taxa_conclusao,
        }


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, project: Project) -> Project:
        self.session.add(project)
        self.session.flush()
        return project

    def get(self, project_id: int) -> Project | None:
        return self.session.get(Project, project_id)

    def list(self, owner_id: int | None = None) -> list[Project]:
        statement = select(Project)
        if owner_id is not None:
            statement = statement.where(Project.owner_id == owner_id)
        statement = statement.order_by(Project.id.desc())
        return list(self.session.scalars(statement))

    def delete(self, project: Project) -> None:
        self.session.delete(project)
        self.session.flush()
