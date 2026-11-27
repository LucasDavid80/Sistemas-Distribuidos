from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserRole
from app.services import user_service

router = APIRouter(prefix="/clientes", tags=["clientes"])

DbSession = Annotated[Session, Depends(get_db)]


class ClienteBase(BaseModel):
    nome: str
    email: str
    idade: int


class Cliente(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


def _to_cliente(user: object) -> Cliente:
    return Cliente.model_validate(user)


def _get_client(db: Session, cliente_id: int):
    user = user_service.get_user(db, cliente_id)
    if user is None or user.role != UserRole.CLIENT:
        return None
    return user


@router.post("/", response_model=Cliente, status_code=201)
def criar_cliente(cliente: ClienteBase, db: DbSession) -> Cliente:
    if UserRepository(db).get_by_email(cliente.email) is not None:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    user = user_service.create_user(
        db, UserCreate(**cliente.model_dump(), role=UserRole.CLIENT)
    )
    return _to_cliente(user)


@router.get("/", response_model=list[Cliente])
def listar_clientes(db: DbSession) -> list[Cliente]:
    users = [
        user for user in user_service.list_users(db) if user.role == UserRole.CLIENT
    ]
    return [_to_cliente(user) for user in users]


@router.get("/{cliente_id}", response_model=Cliente)
def buscar_cliente(cliente_id: int, db: DbSession) -> Cliente:
    user = _get_client(db, cliente_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return _to_cliente(user)


@router.put("/{cliente_id}", response_model=Cliente)
def atualizar_cliente(cliente_id: int, data: ClienteBase, db: DbSession) -> Cliente:
    user = _get_client(db, cliente_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    existing = UserRepository(db).get_by_email(data.email)
    if existing is not None and existing.id != cliente_id:
        raise HTTPException(
            status_code=400, detail="Email já cadastrado por outro cliente"
        )
    updated = user_service.update_user(
        db, cliente_id, UserCreate(**data.model_dump(), role=UserRole.CLIENT)
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return _to_cliente(updated)


@router.delete("/{cliente_id}", status_code=204)
def deletar_cliente(cliente_id: int, db: DbSession) -> None:
    if _get_client(db, cliente_id) is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    user_service.delete_user(db, cliente_id)
