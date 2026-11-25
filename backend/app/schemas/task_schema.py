from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TaskPriority(StrEnum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"


class TaskStatus(StrEnum):
    PENDENTE = "PENDENTE"
    EM_PROGRESSO = "EM_PROGRESSO"
    CONCLUIDA = "CONCLUIDA"


class TaskBase(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    descricao: str = Field(default="", max_length=1000)
    prioridade: TaskPriority = TaskPriority.MEDIA
    status: TaskStatus = TaskStatus.PENDENTE
    categoria: str = Field(default="Geral", max_length=60)
    prazo: datetime | None = None
    project_id: int | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=150)
    descricao: str | None = Field(default=None, max_length=1000)
    prioridade: TaskPriority | None = None
    status: TaskStatus | None = None
    categoria: str | None = Field(default=None, max_length=60)
    prazo: datetime | None = None
    project_id: int | None = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class TaskMetricsResponse(BaseModel):
    total: int
    pendentes: int
    em_progresso: int
    concluidas: int
    taxa_conclusao: float


class ProjectBase(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    descricao: str = Field(default="", max_length=500)


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime
