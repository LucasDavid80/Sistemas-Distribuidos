from fastapi import APIRouter, HTTPException

from app.schemas.user_schema import User, UserBase
from app.services.user_service import (
    create_user,
    delete_user,
    get_user,
    list_users,
    update_user,
    users_db,
)

router = APIRouter(prefix="/users", tags=["users"])


def _ensure_unique_email(email: str, user_id: int | None = None) -> None:
    if any(user.email == email and user.id != user_id for user in users_db.values()):
        raise HTTPException(status_code=400, detail="Email já cadastrado")


@router.post("/", response_model=User, status_code=201)
def create(user: UserBase) -> User:
    _ensure_unique_email(user.email)
    return create_user(user)


@router.get("/", response_model=list[User])
def read_all() -> list[User]:
    return list_users()


@router.get("/{user_id}", response_model=User)
def read_one(user_id: int) -> User:
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.put("/{user_id}", response_model=User)
def update(user_id: int, user: UserBase) -> User:
    if get_user(user_id) is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    _ensure_unique_email(user.email, user_id)
    updated_user = update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated_user


@router.delete("/{user_id}", status_code=204)
def delete(user_id: int) -> None:
    if not delete_user(user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
