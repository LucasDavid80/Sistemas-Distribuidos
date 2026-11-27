from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schemas.user_schema import UserRole
from app.services.user_service import get_user


def current_user(
    db: Annotated[Session, Depends(get_db)],
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
) -> User:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    user = get_user(db, x_user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return user


def require_role(user: User, *roles: UserRole) -> User:
    if user.role not in roles:
        raise HTTPException(status_code=403, detail="Permissão insuficiente")
    return user
