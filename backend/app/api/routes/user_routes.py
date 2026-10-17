from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import User, UserCreate, UserPatch
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

DbSession = Annotated[Session, Depends(get_db)]


def _ensure_unique_email(
    db: Session, email: str, user_id: int | None = None
) -> None:
    existing = UserRepository(db).get_by_email(email)
    if existing is not None and existing.id != user_id:
        raise HTTPException(status_code=400, detail="Email já cadastrado")


@router.post(
    "/", response_model=User, response_model_exclude_defaults=True, status_code=201
)
def create(user: UserCreate, db: DbSession) -> User:
    _ensure_unique_email(db, user.email)
    return user_service.create_user(db, user)


@router.get("/", response_model=list[User], response_model_exclude_defaults=True)
def read_all(db: DbSession) -> list[User]:
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=User, response_model_exclude_defaults=True)
def read_one(user_id: int, db: DbSession) -> User:
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.put("/{user_id}", response_model=User, response_model_exclude_defaults=True)
def update(user_id: int, user: UserCreate, db: DbSession) -> User:
    if user_service.get_user(db, user_id) is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    _ensure_unique_email(db, user.email, user_id)
    updated_user = user_service.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated_user


@router.patch("/{user_id}", response_model=User, response_model_exclude_defaults=True)
def patch(user_id: int, user: UserPatch, db: DbSession) -> User:
    if user.email is not None:
        _ensure_unique_email(db, user.email, user_id)
    updated_user = user_service.patch_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated_user


@router.delete("/{user_id}", status_code=204)
def delete(user_id: int, db: DbSession) -> None:
    if not user_service.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
