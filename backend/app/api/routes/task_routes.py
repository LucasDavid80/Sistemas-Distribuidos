from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.permissions import current_user
from app.database.session import get_db
from app.models.user import User as UserModel
from app.schemas.task_schema import (
    ProjectCreate,
    ProjectResponse,
    TaskCreate,
    TaskMetricsResponse,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskStatusUpdate,
    TaskUpdate,
)
from app.services import task_service
from app.services.user_service import get_user

task_router = APIRouter(prefix="/tasks", tags=["tasks"])
project_router = APIRouter(prefix="/projects", tags=["projects"])

CurrentUser = Annotated[UserModel, Depends(current_user)]
DbSession = Annotated[Session, Depends(get_db)]


def resolve_user(
    db: Session, x_user_id: int | None = None, fallback_id: int = 1
) -> UserModel:
    user_id = x_user_id or fallback_id
    user = get_user(db, user_id)
    if user is None:
        user = get_user(db, 1)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado",
        )
    return user


@task_router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    db: DbSession,
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
) -> TaskResponse:
    user = resolve_user(db, x_user_id)
    try:
        return task_service.create_task(db, data, user.id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@task_router.get("/metrics", response_model=TaskMetricsResponse)
def get_task_metrics(db: DbSession) -> TaskMetricsResponse:
    return task_service.get_task_metrics(db)


@task_router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: DbSession,
    status_filter: Annotated[
        TaskStatus | None, Query(alias="status", description="Filtrar por status")
    ] = None,
    priority_filter: Annotated[
        TaskPriority | None,
        Query(alias="prioridade", description="Filtrar por prioridade"),
    ] = None,
    search: Annotated[
        str | None, Query(description="Buscar no título ou descrição")
    ] = None,
) -> list[TaskResponse]:
    status_val = status_filter.value if status_filter else None
    priority_val = priority_filter.value if priority_filter else None
    return task_service.list_tasks(
        db, status=status_val, prioridade=priority_val, search=search
    )


@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: DbSession) -> TaskResponse:
    task = task_service.get_task(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada"
        )
    return task


@task_router.put("/{task_id}", response_model=TaskResponse)
@task_router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: DbSession,
) -> TaskResponse:
    try:
        updated = task_service.update_task(db, task_id, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)
        ) from exc

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada"
        )
    return updated


@task_router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    data: TaskStatusUpdate,
    db: DbSession,
) -> TaskResponse:
    updated = task_service.update_task_status(db, task_id, data)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada"
        )
    return updated


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: DbSession,
) -> Response:
    deleted = task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@project_router.post(
    "/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED
)
def create_project(
    data: ProjectCreate,
    db: DbSession,
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
) -> ProjectResponse:
    user = resolve_user(db, x_user_id)
    return task_service.create_project(db, data, user.id)


@project_router.get("/", response_model=list[ProjectResponse])
def list_projects(db: DbSession) -> list[ProjectResponse]:
    return task_service.list_projects(db)


@project_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: DbSession,
) -> Response:
    deleted = task_service.delete_project(db, project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
