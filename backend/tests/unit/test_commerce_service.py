import pytest

from app.schemas.commerce_schema import ProductCreate, ProductPatch
from app.schemas.user_schema import UserCreate
from app.services import commerce_service, user_service


def create_user(db, **data):
    return user_service.create_user(
        db,
        UserCreate(
            nome=data.get("nome", "Alice"),
            email=data.get("email", "alice@email.com"),
            idade=data.get("idade", 25),
        ),
    )


def test_create_and_update_product(db):
    product = commerce_service.create_product(
        db, ProductCreate(nome="Produto", preco=10, estoque=3), seller_id=1
    )

    updated = commerce_service.update_product(
        db, product.id, ProductPatch(nome="Produto atualizado", estoque=5)
    )

    assert product.id == 1
    assert product.seller_id == 1
    assert updated is not None
    assert updated.nome == "Produto atualizado"
    assert updated.estoque == 5
    assert (
        commerce_service.update_product(db, 999, ProductPatch(nome="Inexistente"))
        is None
    )


def test_purchase_product_decreases_stock_and_balance(db):
    client = create_user(db)
    user_service.add_balance(db, client.id, 100)
    product = commerce_service.create_product(
        db, ProductCreate(nome="Produto", preco=25, estoque=4), seller_id=2
    )

    purchase = commerce_service.purchase_product(db, product.id, client.id, 2)

    assert purchase is not None
    assert purchase.total == 50
    assert commerce_service.get_product(db, product.id).estoque == 2
    assert user_service.get_user(db, client.id).saldo == 50


def test_purchase_product_rolls_back_on_insufficient_balance(db):
    client = create_user(db)
    product = commerce_service.create_product(
        db, ProductCreate(nome="Produto", preco=25, estoque=1), seller_id=2
    )

    with pytest.raises(ValueError, match="Saldo insuficiente"):
        commerce_service.purchase_product(db, product.id, client.id, 1)

    assert commerce_service.get_product(db, product.id).estoque == 1
    assert user_service.get_user(db, client.id).saldo == 0
    assert commerce_service.list_purchases_by_client(db, client.id) == []


def test_purchase_product_rejects_missing_records_and_stock(db):
    client = create_user(db)
    product = commerce_service.create_product(
        db, ProductCreate(nome="Produto", preco=25, estoque=1), seller_id=2
    )

    with pytest.raises(ValueError, match="Estoque insuficiente"):
        commerce_service.purchase_product(db, product.id, client.id, 2)

    assert commerce_service.purchase_product(db, 999, client.id, 1) is None
    assert commerce_service.purchase_product(db, product.id, 999, 1) is None
