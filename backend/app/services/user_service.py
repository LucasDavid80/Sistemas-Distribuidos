from app.schemas.user_schema import User, UserCreate, UserPatch

users_db: dict[int, User] = {}
next_id = 1


def create_user(user: UserCreate) -> User:
    global next_id

    new_user = User(id=next_id, **user.model_dump())
    users_db[next_id] = new_user
    next_id += 1
    return new_user


def list_users() -> list[User]:
    return list(users_db.values())


def get_user(user_id: int) -> User | None:
    return users_db.get(user_id)


def update_user(user_id: int, user: UserCreate) -> User | None:
    if user_id not in users_db:
        return None

    updated_user = User(id=user_id, **user.model_dump())
    users_db[user_id] = updated_user
    return updated_user


def patch_user(user_id: int, user: UserPatch) -> User | None:
    current_user = users_db.get(user_id)
    if current_user is None:
        return None

    changes = user.model_dump(exclude_none=True)
    updated_user = current_user.model_copy(update=changes)
    users_db[user_id] = updated_user
    return updated_user


def add_balance(user_id: int, amount: float) -> User | None:
    user = users_db.get(user_id)
    if user is None:
        return None

    updated_user = user.model_copy(update={"saldo": user.saldo + amount})
    users_db[user_id] = updated_user
    return updated_user


def delete_user(user_id: int) -> bool:
    if user_id not in users_db:
        return False

    del users_db[user_id]
    return True
