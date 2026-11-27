import pytest

from app.schemas.task_schema import (
    ProjectCreate,
    TaskCreate,
    TaskPriority,
    TaskStatus,
    TaskStatusUpdate,
    TaskUpdate,
)
from app.schemas.user_schema import UserCreate
from app.services import task_service, user_service


def create_user(db, **data):
    return user_service.create_user(
        db,
        UserCreate(
            nome=data.get("nome", "Lucas"),
            email=data.get("email", "lucas@email.com"),
            idade=data.get("idade", 22),
        ),
    )


def test_create_and_list_tasks(db):
    user = create_user(db)
    task = task_service.create_task(
        db,
        TaskCreate(
            titulo="Configurar CI",
            descricao="Adicionar GitHub Actions",
            prioridade=TaskPriority.ALTA,
            status=TaskStatus.PENDENTE,
            categoria="DevOps",
        ),
        user_id=user.id,
    )

    assert task.id is not None
    assert task.titulo == "Configurar CI"
    assert task.prioridade == "ALTA"
    assert task.status == "PENDENTE"
    assert task.categoria == "DevOps"
    assert task.user_id == user.id

    tasks = task_service.list_tasks(db)
    assert len(tasks) == 1
    assert tasks[0].id == task.id


def test_update_task_and_status(db):
    user = create_user(db)
    task = task_service.create_task(
        db,
        TaskCreate(titulo="Tarefa Inicial", prioridade=TaskPriority.MEDIA),
        user_id=user.id,
    )

    updated = task_service.update_task(
        db,
        task.id,
        TaskUpdate(
            titulo="Tarefa Atualizada",
            descricao="Nova descrição",
            prioridade=TaskPriority.ALTA,
        ),
    )
    assert updated is not None
    assert updated.titulo == "Tarefa Atualizada"
    assert updated.prioridade == "ALTA"

    status_updated = task_service.update_task_status(
        db, task.id, TaskStatusUpdate(status=TaskStatus.CONCLUIDA)
    )
    assert status_updated is not None
    assert status_updated.status == "CONCLUIDA"


def test_delete_task(db):
    user = create_user(db)
    task = task_service.create_task(
        db,
        TaskCreate(titulo="Para deletar"),
        user_id=user.id,
    )

    assert task_service.get_task(db, task.id) is not None
    deleted = task_service.delete_task(db, task.id)
    assert deleted is True
    assert task_service.get_task(db, task.id) is None
    assert task_service.delete_task(db, 999) is False


def test_task_metrics_calculation(db):
    user = create_user(db)

    # 1 Pendente, 1 Em Progresso, 2 Concluídas -> Total 4, Conclusão 50.0%
    task_service.create_task(
        db,
        TaskCreate(titulo="T1", status=TaskStatus.PENDENTE),
        user_id=user.id,
    )
    task_service.create_task(
        db,
        TaskCreate(titulo="T2", status=TaskStatus.EM_PROGRESSO),
        user_id=user.id,
    )
    task_service.create_task(
        db,
        TaskCreate(titulo="T3", status=TaskStatus.CONCLUIDA),
        user_id=user.id,
    )
    task_service.create_task(
        db,
        TaskCreate(titulo="T4", status=TaskStatus.CONCLUIDA),
        user_id=user.id,
    )

    metrics = task_service.get_task_metrics(db)
    assert metrics["total"] == 4
    assert metrics["pendentes"] == 1
    assert metrics["em_progresso"] == 1
    assert metrics["concluidas"] == 2
    assert metrics["taxa_conclusao"] == 50.0


def test_create_task_with_invalid_project(db):
    user = create_user(db)
    with pytest.raises(ValueError, match="Projeto associado não encontrado"):
        task_service.create_task(
            db,
            TaskCreate(titulo="Tarefa órfã", project_id=9999),
            user_id=user.id,
        )


def test_project_crud(db):
    user = create_user(db)
    project = task_service.create_project(
        db,
        ProjectCreate(nome="Projeto C216", descricao="Trabalho final"),
        owner_id=user.id,
    )
    assert project.id is not None
    assert project.nome == "Projeto C216"

    projects = task_service.list_projects(db)
    assert len(projects) == 1

    deleted = task_service.delete_project(db, project.id)
    assert deleted is True
