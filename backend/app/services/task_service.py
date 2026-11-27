from sqlalchemy.orm import Session

from app.models.project import Project as ProjectModel
from app.models.task import Task as TaskModel
from app.repositories.task_repository import ProjectRepository, TaskRepository
from app.schemas.task_schema import (
    ProjectCreate,
    TaskCreate,
    TaskStatusUpdate,
    TaskUpdate,
)


def create_task(db: Session, data: TaskCreate, user_id: int) -> TaskModel:
    if data.project_id is not None:
        project = ProjectRepository(db).get(data.project_id)
        if project is None:
            raise ValueError("Projeto associado não encontrado")

    task = TaskModel(
        titulo=data.titulo.strip(),
        descricao=data.descricao.strip(),
        prioridade=data.prioridade.value,
        status=data.status.value,
        categoria=data.categoria.strip() or "Geral",
        prazo=data.prazo,
        project_id=data.project_id,
        user_id=user_id,
    )
    TaskRepository(db).add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(
    db: Session,
    status: str | None = None,
    prioridade: str | None = None,
    search: str | None = None,
    user_id: int | None = None,
) -> list[TaskModel]:
    return TaskRepository(db).list(
        status=status, prioridade=prioridade, search=search, user_id=user_id
    )


def get_task(db: Session, task_id: int) -> TaskModel | None:
    return TaskRepository(db).get(task_id)


def update_task(
    db: Session, task_id: int, data: TaskUpdate, user_id: int | None = None
) -> TaskModel | None:
    repo = TaskRepository(db)
    task = repo.get(task_id)
    if task is None:
        return None

    if user_id is not None and task.user_id != user_id:
        raise PermissionError("Você não tem permissão para alterar esta tarefa")

    if data.project_id is not None:
        project = ProjectRepository(db).get(data.project_id)
        if project is None:
            raise ValueError("Projeto associado não encontrado")

    update_dict = data.model_dump(exclude_unset=True, exclude_none=True)
    if "prioridade" in update_dict:
        update_dict["prioridade"] = update_dict["prioridade"].value
    if "status" in update_dict:
        update_dict["status"] = update_dict["status"].value
    if "titulo" in update_dict:
        update_dict["titulo"] = update_dict["titulo"].strip()
    if "descricao" in update_dict:
        update_dict["descricao"] = update_dict["descricao"].strip()
    if "categoria" in update_dict:
        update_dict["categoria"] = update_dict["categoria"].strip() or "Geral"

    for field, value in update_dict.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def update_task_status(
    db: Session, task_id: int, data: TaskStatusUpdate, user_id: int | None = None
) -> TaskModel | None:
    repo = TaskRepository(db)
    task = repo.get(task_id)
    if task is None:
        return None

    if user_id is not None and task.user_id != user_id:
        raise PermissionError("Você não tem permissão para alterar esta tarefa")

    task.status = data.status.value
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int | None = None) -> bool:
    repo = TaskRepository(db)
    task = repo.get(task_id)
    if task is None:
        return False

    if user_id is not None and task.user_id != user_id:
        raise PermissionError("Você não tem permissão para remover esta tarefa")

    repo.delete(task)
    db.commit()
    return True


def get_task_metrics(db: Session, user_id: int | None = None) -> dict[str, int | float]:
    return TaskRepository(db).get_metrics(user_id=user_id)


def create_project(db: Session, data: ProjectCreate, owner_id: int) -> ProjectModel:
    project = ProjectModel(
        nome=data.nome.strip(),
        descricao=data.descricao.strip(),
        owner_id=owner_id,
    )
    ProjectRepository(db).add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session, owner_id: int | None = None) -> list[ProjectModel]:
    return ProjectRepository(db).list(owner_id=owner_id)


def delete_project(db: Session, project_id: int, owner_id: int | None = None) -> bool:
    repo = ProjectRepository(db)
    project = repo.get(project_id)
    if project is None:
        return False

    if owner_id is not None and project.owner_id != owner_id:
        raise PermissionError("Você não tem permissão para remover este projeto")

    repo.delete(project)
    db.commit()
    return True
