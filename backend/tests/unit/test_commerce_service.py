import pytest

from app.schemas.commerce_schema import ProductCreate, ProductPatch
from app.schemas.user_schema import UserCreate
from app.services import commerce_service, user_service


@pytest.fixture(autouse=True)
def reset_commerce():
    commerce_service.products_db.clear()
    commerce_service.purchases_db.clear()
    commerce_service.next_product_id = 1
    commerce_service.next_purchase_id = 1
    user_service.users_db.clear()
    user_service.next_id = 1


def create_user(**data):
    return user_service.create_user(
        UserCreate(
            nome=data.get("nome", "Alice"),
            email=data.get("email", "alice@email.com"),
            idade=data.get("idade", 25),
        )
    )


def test_create_and_update_product():
    product = commerce_service.create_product(
        ProductCreate(nome="Produto", preco=10, estoque=3), seller_id=1
    )

    updated = commerce_service.update_product(
        product.id, ProductPatch(nome="Produto atualizado", estoque=5)
    )

    assert product.id == 1
    assert product.seller_id == 1
    assert updated is not None
    assert updated.nome == "Produto atualizado"
    assert updated.estoque == 5
    assert (
        commerce_service.update_product(999, ProductPatch(nome="Inexistente")) is None
    )


def test_purchase_product_decreases_stock_and_balance():
    client = create_user()
    user_service.add_balance(client.id, 100)
    product = commerce_service.create_product(
        ProductCreate(nome="Produto", preco=25, estoque=4), seller_id=2
    )

    purchase = commerce_service.purchase_product(product.id, client.id, 2)

    assert purchase is not None
    assert purchase.total == 50
    assert commerce_service.products_db[product.id].estoque == 2
    assert user_service.users_db[client.id].saldo == 50


def test_purchase_product_rejects_invalid_conditions():
    client = create_user()
    product = commerce_service.create_product(
        ProductCreate(nome="Produto", preco=25, estoque=1), seller_id=2
    )

    with pytest.raises(ValueError, match="Estoque insuficiente"):
        commerce_service.purchase_product(product.id, client.id, 2)

    with pytest.raises(ValueError, match="Saldo insuficiente"):
        commerce_service.purchase_product(product.id, client.id, 1)

    assert commerce_service.purchase_product(999, client.id, 1) is None
    assert commerce_service.purchase_product(product.id, 999, 1) is None
