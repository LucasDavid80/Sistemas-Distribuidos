from fastapi import Header, HTTPException

from app.schemas.user_schema import User, UserRole
from app.services.user_service import get_user


def current_user(x_user_id: int | None = Header(None, alias="X-User-Id")) -> User:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    user = get_user(x_user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return user


def require_role(user: User, *roles: UserRole) -> User:
    if user.role not in roles:
        raise HTTPException(status_code=403, detail="Permissão insuficiente")
    return user
