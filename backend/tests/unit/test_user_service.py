from app.schemas.user_schema import UserCreate, UserPatch, UserRole
from app.services import user_service


def test_create_and_list_users(db):
    user = user_service.create_user(
        db, UserCreate(nome="Alice", email="alice@email.com", idade=25)
    )

    assert user.id == 1
    assert user_service.list_users(db) == [user]


def test_get_existing_and_missing_user(db):
    user = user_service.create_user(
        db, UserCreate(nome="Bob", email="bob@email.com", idade=30)
    )

    assert user_service.get_user(db, user.id) == user
    assert user_service.get_user(db, 999) is None


def test_update_user(db):
    user = user_service.create_user(
        db, UserCreate(nome="Carol", email="carol@email.com", idade=28)
    )

    updated = user_service.update_user(
        db,
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
            db, 999, UserCreate(nome="Ghost", email="ghost@email.com", idade=99)
        )
        is None
    )


def test_patch_user_and_add_balance(db):
    user = user_service.create_user(
        db, UserCreate(nome="Dave", email="dave@email.com", idade=35)
    )

    patched = user_service.patch_user(
        db, user.id, UserPatch(nome="Dave Updated", role=UserRole.ADMIN)
    )
    credited = user_service.add_balance(db, user.id, 50)

    assert patched is not None
    assert patched.nome == "Dave Updated"
    assert patched.email == "dave@email.com"
    assert credited is not None
    assert credited.saldo == 50
    assert user_service.patch_user(db, 999, UserPatch(nome="Ghost")) is None
    assert user_service.add_balance(db, 999, 50) is None


def test_delete_user(db):
    user = user_service.create_user(
        db, UserCreate(nome="Eve", email="eve@email.com", idade=22)
    )

    assert user_service.delete_user(db, user.id) is True
    assert user_service.get_user(db, user.id) is None
    assert user_service.delete_user(db, user.id) is False
