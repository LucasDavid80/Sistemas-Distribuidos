from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserPatch


def create_user(db: Session, user: UserCreate) -> UserModel:
    repository = UserRepository(db)
    new_user = UserModel(**user.model_dump())
    repository.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def list_users(db: Session) -> list[UserModel]:
    return UserRepository(db).list()


def get_user(db: Session, user_id: int) -> UserModel | None:
    return UserRepository(db).get(user_id)


def update_user(
    db: Session, user_id: int, user: UserCreate
) -> UserModel | None:
    repository = UserRepository(db)
    current_user = repository.get(user_id)
    if current_user is None:
        return None

    for field, value in user.model_dump().items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


def patch_user(
    db: Session, user_id: int, user: UserPatch
) -> UserModel | None:
    repository = UserRepository(db)
    current_user = repository.get(user_id)
    if current_user is None:
        return None

    for field, value in user.model_dump(exclude_none=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


def add_balance(db: Session, user_id: int, amount: float) -> UserModel | None:
    repository = UserRepository(db)
    user = repository.get(user_id)
    if user is None:
        return None

    user.saldo += amount
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    repository = UserRepository(db)
    user = repository.get(user_id)
    if user is None:
        return False

    repository.delete(user)
    db.commit()
    return True
