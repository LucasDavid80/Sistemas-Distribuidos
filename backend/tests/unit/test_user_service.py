import pytest

from app.schemas.user_schema import UserCreate, UserPatch, UserRole
from app.services import user_service


@pytest.fixture(autouse=True)
def reset_users():
    user_service.users_db.clear()
    user_service.next_id = 1


def test_create_and_list_users():
    user = user_service.create_user(
        UserCreate(nome="Alice", email="alice@email.com", idade=25)
    )

    assert user.id == 1
    assert user_service.list_users() == [user]


def test_get_existing_and_missing_user():
    user = user_service.create_user(
        UserCreate(nome="Bob", email="bob@email.com", idade=30)
    )

    assert user_service.get_user(user.id) == user
    assert user_service.get_user(999) is None


def test_update_user():
    user = user_service.create_user(
        UserCreate(nome="Carol", email="carol@email.com", idade=28)
    )

    updated = user_service.update_user(
        user.id,
        UserCreate(
            nome="Carol Updated",
            email="carol.updated@email.com",
            idade=29,
            role=UserRole.SELLER,
        ),
    )

    assert updated is not None
    assert updated.nome == "Carol Updated"
    assert updated.role == UserRole.SELLER
    assert (
        user_service.update_user(
            999, UserCreate(nome="Ghost", email="ghost@email.com", idade=99)
        )
        is None
    )


def test_patch_user_and_add_balance():
    user = user_service.create_user(
        UserCreate(nome="Dave", email="dave@email.com", idade=35)
    )

    patched = user_service.patch_user(
        user.id, UserPatch(nome="Dave Updated", role=UserRole.ADMIN)
    )
    credited = user_service.add_balance(user.id, 50)

    assert patched is not None
    assert patched.nome == "Dave Updated"
    assert patched.email == "dave@email.com"
    assert credited is not None
    assert credited.saldo == 50
    assert user_service.patch_user(999, UserPatch(nome="Ghost")) is None
    assert user_service.add_balance(999, 50) is None


def test_delete_user():
    user = user_service.create_user(
        UserCreate(nome="Eve", email="eve@email.com", idade=22)
    )

    assert user_service.delete_user(user.id) is True
    assert user_service.get_user(user.id) is None
    assert user_service.delete_user(user.id) is False
