from app.schemas.user_schema import User, UserBase

users_db: dict[int, User] = {}
next_id = 1


def create_user(user: UserBase) -> User:
    global next_id

    new_user = User(id=next_id, **user.model_dump())
    users_db[next_id] = new_user
    next_id += 1
    return new_user


def list_users() -> list[User]:
    return list(users_db.values())


def get_user(user_id: int) -> User | None:
    return users_db.get(user_id)


def update_user(user_id: int, user: UserBase) -> User | None:
    if user_id not in users_db:
        return None

    updated_user = User(id=user_id, **user.model_dump())
    users_db[user_id] = updated_user
    return updated_user


def delete_user(user_id: int) -> bool:
    if user_id not in users_db:
        return False

    del users_db[user_id]
    return True
